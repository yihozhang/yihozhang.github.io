---
title: "Computing Half the Points: An Optimization to Parallel Matrix Scan for LTV Recurrences"
author: Yihong Zhang
date: Mar 9, 2026
---

In the [previous post](ltv-recurrences.html), I described two algorithms for vectorizing linear time-varying (LTV) recurrences: the classical matrix prefix scan and a new $d_k/f_k$ decomposition. The background section on matrix prefix scans noted that a work multiplier of roughly $1 + 6\log k \approx 19$ for $k=16$ makes the approach likely impractical — but also that an optimization was being left on the table. This post fills in that gap.

# The Key Observation

Recall from the previous post that the matrix prefix scan computes, for each output position $x$, the combined matrix $M_{16}(x) = M(x)\cdot M(x-1)\cdots M(x-15)$. Applying it to the boundary gives:

$$ \begin{pmatrix} f(x) \\ f(x-1) \\ 1 \end{pmatrix} = M_{16}(x) \begin{pmatrix} f(x-16) \\ f(x-17) \\ 1 \end{pmatrix}$$

This means $M_{16}(x)$ simultaneously encodes two consecutive outputs: $f(x)$ in its first row, and $f(x-1)$ in its second row. The previous algorithm discards the second row and uses only the first to compute $f(x)$.

We can do better. Instead of computing $M_{16}(x)$ for each of the $k = 16$ positions in a block, we compute every *other* position of $M_{32}(x)$. As in the previous post, each $k$-lane vector still holds $k = 16$ outputs, but we are covering a twice as large window (32 vs 16). Specifically, since

$$ \begin{pmatrix} f(x) \\ f(x-1) \\ 1 \end{pmatrix} = M_{32}(x) \begin{pmatrix} f(x-32) \\ f(x-33) \\ 1 \end{pmatrix}, $$

$M_{32}(x)$ gives us $f(x)$ from its first row and $f(x-1)$ from its second row. Computing $M_{32}(x)$ for odd positions $x+1, x+3, x+5, \ldots, x+2k-1$ (with $k = 16$) recovers all 32 outputs $f(x), f(x+1), \ldots, f(x+31)$.

# The Algorithm

The computation is somewhat more involved than before, since each layer now processes a different number of matrix elements. Here we give a sketch of how the algorithm works.

We process the output in blocks of $2k$. The computation at each block proceeds in three phases.

**Phase 1: Compute $M_2$ at even positions.**

Define $M_2'(x) = M_2(2x+1) = M(2x-1)\cdot M(2x)$. For each even position $2x$ in the block, this is the product of two consecutive matrices. Working out the matrix product:

$$M_2'(x) = \begin{pmatrix} a(2x+1)\cdot a(2x) + b(2x+1) & a(2x+1)\cdot b(2x) & a(2x+1)\cdot g(2x) + g(2x+1) \\ a(2x) & b(2x) & g(2x) \\ 0 & 0 & 1 \end{pmatrix}$$

To compute these $k$ values of $M_2'$ using $k$-wide SIMD, we load two vectors of length $k$ for each of $a$, $b$, $g$ (covering 32 elements total), then unzip them so that each vector only holds values from even or odd positions.

The second row of $M_2'(x)$ is just $[a(2x),\, b(2x),\, g(2x)]$ — the input values at the odd position, which are already available from the input. So like the previous algorithm, at the base layer we only need to compute three new arrays.

**Phase 2: Parallel prefix scan over $M_2'$.**

Next, define $M_4'(x) = M_4(2x+1) = M_2'(x)\cdot M_2'(x-1)$, $M_8'(x) = M_4'(x)\cdot M_4'(x-2)$, and similarly for other $M'$s all the way to $M'_{2k}$, which is $M'_{32}$ if we assume AVX-512 with floats.

To compute $M'_{2k}$ requires $\log k$ layers besides the base layer in Phase 1. So $M_{32}'(x)$ requires $\log 16=4$ layers, each layer combining pairs of $3\times 3$ matrices (restricted to the two nontrivial rows and six values).

**Phase 3: Extract both rows.**

Finally, we can compute the even and odd positions of the local $[x, x+2k-1]$ window:

$$\begin{pmatrix} f(2x+1) \\ f(2x) \\ 1 \end{pmatrix} = M_{32}'(x) \begin{pmatrix} f(2x-31) \\ f(2x-32) \\ 1 \end{pmatrix}$$

The dot product of row 1 of $M_{32}'(x)$ and $[f(2x-31),\, f(2x-32),\, 1]$ gives $f(2x)$, and similarly the dot product with row 2 of $M_{32}'(x)$ gives $f(2x-1)$.

To execute this in vectorized fashion, we first load vectors $[f(2(x+i)-32) \mid i\in0,\ldots,k-1]$ and $[f(2(x-i)-31) \mid i\in0,\ldots,k-1]$ from the last local window's output.
They can be loaded from the memory and then interleaved using the same unzipping instruction as in Phase 1, or better, using the output vector from the last local window computation, which is already un-interleaved.

Then, we separately compute $[f(2(x+i)+1) \mid i\in0,\ldots,k-1]$ and $[f(2(x+i))\mid i\in0,\ldots,k-1]$ using  the first row and the second row of $M_{32}'(x)$ and the loaded $f$ vectors.
This gives all the odd and even entries for the current local window, each of which is stored in a $k$-lane vector.

Finally, we zip the odd and even vectors into two consecutive $k$-lane vectors and store to the memory.

**Pseudocode.**

The following pseudocode computes the full $f$ array, processing one block of $2k$ outputs at a time. Auxiliary arrays `M2`, `M4`, `M8`, `M16`, `M32` hold two-row $2\times3$ matrices for the $k$ even positions in the current block. `mat_mul(A, B)` multiplies two such matrices (6 multiply-accumulates).

```python
def half_points_scan(a, b, g, f):
    """
    Computes f[0..N-1] for f[x] = a[x]*f[x-1] + b[x]*f[x-2] + g[x],
    with boundary values f[-1] and f[-2] given.
    N must be a multiple of 2k = 32  (k = 16 SIMD lanes).
    """
    N = len(a)
    k = 16

    M2  = zeros((2, 3, N//2))
    M4  = zeros((2, 3, N//2))
    M8  = zeros((2, 3, N//2))
    M16 = zeros((2, 3, N//2))
    M32 = zeros((2, 3, N//2))

    for base in range(0, N//2, k):
        def load_interleaved(arr, base):
            v0 = arr[2*base:2*base+k]
            v1 = arr[2*base+k:2*base+2*k]
            return unzip(v0, v1)

        a_even, a_odd = load_interleaved(a, base)
        b_even, b_odd = load_interleaved(b, base)
        g_even, g_odd = load_interleaved(g, base)

        # Phase 1
        M2[0:2][0:3][base:base+k] = (
            (a_odd*a_even + b_odd,  a_odd*b_even,  a_odd*g_even + g_odd),
            (a_even,                b_even,         g_even             ),
        )

        # Phase 2
        def combine(M_left, M_right):
            return (
                (
                    M_left[0][0]*M_right[0][0] + M_left[0][1]*M_right[1][0],
                    M_left[0][0]*M_right[0][1] + M_left[0][1]*M_right[1][1],
                    M_left[0][0]*M_right[0][2] + M_left[0][1]*M_right[1][2] + M_left[0][2],
                ),(
                    M_left[1][0]*M_right[0][0] + M_left[1][1]*M_right[1][0],
                    M_left[1][0]*M_right[0][1] + M_left[1][1]*M_right[1][1],
                    M_left[1][0]*M_right[0][2] + M_left[1][1]*M_right[1][2] + M_left[1][2],
                )
            )

        M4[0:2][0:3][base:base+k] = combine(M2[0:2][0:3][base:base+k], M2[0:2][0:3][base-1:base-1+k])
        M8[0:2][0:3][base:base+k] = combine(M4[0:2][0:3][base:base+k], M4[0:2][0:3][base-2:base-2+k])
        M16[0:2][0:3][base:base+k] = combine(M8[0:2][0:3][base:base+k], M8[0:2][0:3][base-4:base-4+k])
        M32[0:2][0:3][base:base+k] = combine(M16[0:2][0:3][base:base+k], M16[0:2][0:3][base-8:base-8+k])

        # Phase 3
        f_prev0, f_prev1 = load_interleaved(f, base-k)
        f_odd = M32[0][0][base:base+k]*f_prev1 + M32[0][1][base:base+k]*f_prev0 + M32[0][2][base:base+k]
        f_even  = M32[1][0][base:base+k]*f_prev1 + M32[1][1][base:base+k]*f_prev0 + M32[1][2][base:base+k]

        f_first, f_second = zip(f_even, f_odd)
        f[2*base:2*base+k] = f_first
        f[2*base+k:2*base+2*k] = f_second
```

# Work Analysis

The total work per block of $2k$ outputs, measured in multiply-accumulate operations per lane:

| Step | Cost per lane |
|------|--------------|
| Phase 1: $M_2'$ (first row only) | 3 |
| Phase 2: $\log_2 k$ scan layers (6 per layer) | $6\log k$ |
| Phase 3: one dot product per row of $M_{32}'$ | 2 |
| **Total** | $5 + 6\log k$ |

For $k = 16$: $5 + 6 \cdot 4 = 29$ operations for $2k = 32$ outputs, a **work multiplier of $29/32 \approx 0.91$ per output element**.

Comparing to the two approaches from the previous post, which each produce $k = 16$ outputs using $k$-wide vectors:

| Algorithm | Work per output ($k=16$) |
|-----------|--------------------------|
| Matrix prefix scan | $19/16 \approx 1.19$ |
| **Half-points scan (this post)** | **$29/32 \approx 0.91$** |
| $d_k/f_k$ decomposition | $14/16 \approx 0.875$ |

The half-points scan is cheaper per output than the matrix scan and comes close to the $d_k/f_k$ decomposition, though the decomposition remains slightly better. However, this assumes floats with AVX-512. In terms of register pressure, the half-points scan requires $6$ arrays per layer to produce $2k$ outputs ($3/16$ arrays per output), while the $d_k/f_k$ decomposition requires $4$ arrays per layer to produce $k$ outputs ($1/4$ arrays per output). The half-points scan is therefore more register-efficient per output element, which can matter in practice.

# Why This Doesn't Apply to the $d_k/f_k$ Decomposition

One might wonder whether a similar trick can halve the work of the $d_k/f_k$ decomposition. It cannot. The $d_k/f_k$ formulas at each layer use values at *odd* offsets — for example, $d_{16}(x) = d_8(x)\cdot d_8(x-8) + d_7(x)\cdot b(x-7)\cdot d_7(x-9)$ requires $d_7(x-9)$, an odd-offset value. There is no way to skip odd positions, because those intermediate values are genuinely needed.

The matrix form avoids this by carrying both $f(x)$ and $f(x-1)$ in the same matrix, so the odd-position output falls out of the second row for free. The $d_k/f_k$ decomposition does not have this structure.

# Closing Thoughts

The half-points trick brings the matrix prefix scan's work per output below 1× scalar, making it competitive with the $d_k/f_k$ decomposition.
There are some practical considerations I did not cover here. The algorithm requires zip/unzip operations at the boundary of each block, which are cheap but not free. The doubled block size also means twice the latency before the first output of each block is available — though this is rarely a concern for bulk image-processing workloads. Register pressure, the exact shuffle instructions generated by LLVM, and alignment of the block size to cache lines all factor into the real-world tradeoff between these approaches.
