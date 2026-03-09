---
title: "Computing Half the Points: An Optimization to Parallel Matrix Scan for LTV Recurrences"
author: Yihong Zhang
date: Mar 9, 2026
---

In the [previous post](ltv-recurrences.html), I described two algorithms for vectorizing linear time-varying (LTV) recurrences: the classical matrix prefix scan and a new $d_k/f_k$ decomposition. The background section on matrix prefix scans noted that a work multiplier of roughly $1 + 6\log k \approx 19$ for $k=16$ makes the approach marginal in practice — but also that an optimization was being left on the table. This post fills in that gap.

# The Key Observation

Recall from the previous post that the matrix prefix scan computes, for each output position $x$, the combined matrix $M_{16}(x) = M(x)\cdot M(x-1)\cdots M(x-15)$. Applying it to the boundary gives:

$$M_{16}(x) \begin{pmatrix} f(x-16) \\ f(x-17) \\ 1 \end{pmatrix} = \begin{pmatrix} f(x) \\ f(x-1) \\ 1 \end{pmatrix}$$

This means $M_{16}(x)$ simultaneously encodes two consecutive outputs: $f(x)$ in its first row, and $f(x-1)$ in its second row. In the standard algorithm, we throw away the second row.

We can do better. Instead of computing $M_{16}(x)$ for each of the $k = 16$ positions in a block (getting 16 outputs), we compute $M_{32}(x)$ for every *other* position in a block of 32 (getting 32 outputs). Specifically:

$$M_{32}(x) \begin{pmatrix} f(x-32) \\ f(x-33) \\ 1 \end{pmatrix} = \begin{pmatrix} f(x) \\ f(x-1) \\ 1 \end{pmatrix}$$

So $M_{32}(x)$ gives us $f(x)$ from its first row and $f(x-1)$ from its second row. Computing $M_{32}(x)$ for even positions $x = 2, 4, \ldots, 2k$ (with $k = 16$) recovers all 32 outputs $f(1), f(2), \ldots, f(32)$.

The key insight is that we only need to compute these matrices at *half* the positions — hence the name.

# The Algorithm

We process the output in blocks of $2k$. The computation at each block proceeds in three phases.

**Phase 1: Compute $M_2$ at even positions.**

Define $M_2'(x) = M_2(2x) = M(2x)\cdot M(2x-1)$. For each even position $2x$ in the block, this is the product of two consecutive matrices. Working out the matrix product:

$$M_2'(x) = \begin{pmatrix} a(2x)\cdot a(2x-1) + b(2x) & a(2x)\cdot b(2x-1) & a(2x)\cdot g(2x-1) + g(2x) \\ a(2x-1) & b(2x-1) & g(2x-1) \\ 0 & 0 & 1 \end{pmatrix}$$

The second row of $M_2'(x)$ is just $[a(2x-1),\, b(2x-1),\, g(2x-1)]$ — the input values at the odd position, which we already hold. So forming $M_2'(x)$ costs only **3 multiplications** per lane (for the first row).

To compute these $k$ values of $M_2'$ using $k$-wide SIMD, we load two vectors of length $k$ for each of $a$, $b$, $g$ (covering 32 elements total), then interleave/zip them so that even and odd elements pair up within the same lanes.

**Phase 2: Parallel prefix scan over $M_2'$.**

Next, define $M_4'(x) = M_4(2x) = M_2'(x)\cdot M_2'(x-1)$, and similarly:

$$M_8'(x) = M_4'(x)\cdot M_4'(x-2), \quad M_{16}'(x) = M_8'(x)\cdot M_8'(x-4), \quad M_{32}'(x) = M_{16}'(x)\cdot M_{16}'(x-8)$$

Each step doubles the window, so $\log_2 k = 4$ layers suffice to compute $M_{32}'(x) = M_{32}(2x)$ at all $k = 16$ positions. Each layer combines pairs of $3\times 3$ matrices (restricted to the two nontrivial rows, 6 values), costing **6 multiplications** per lane.

**Phase 3: Extract both rows.**

Finally, for each position $x = 1, \ldots, k$:

$$M_{32}'(x) \begin{pmatrix} f(2x-32) \\ f(2x-33) \\ 1 \end{pmatrix} = \begin{pmatrix} f(2x) \\ f(2x-1) \\ 1 \end{pmatrix}$$

- Row 1 of $M_{32}'(x)$ dotted with $[f(2x-32),\, f(2x-33),\, 1]$ → $f(2x)$ (even output)
- Row 2 of $M_{32}'(x)$ dotted with $[f(2x-32),\, f(2x-33),\, 1]$ → $f(2x-1)$ (odd output)

where $f(2x-32)$ and $f(2x-33)$ are the boundary values carried in from the previous block. We then unzip the even and odd outputs into two consecutive $k$-element vectors and store.

**Pseudocode.**

```python
def half_points_scan(a, b, g, f_prev1, f_prev2):
    """
    Computes f[0..2k-1] given boundary f[-1]=f_prev1, f[-2]=f_prev2.
    All variables are k-element vectors (k = SIMD width).
    a/b/g each have 2k input values, loaded as two k-vectors.
    """
    # Interleave: a_even[j] = a[2j], a_odd[j] = a[2j-1]
    a_even, a_odd = zip(a[0::2], a[1::2])
    b_even, b_odd = zip(b[0::2], b[1::2])
    g_even, g_odd = zip(g[0::2], g[1::2])

    # Phase 1: compute M2'(x) = M2(2x), first row only
    # Row 1: [a_even*a_odd + b_even, a_even*b_odd, a_even*g_odd + g_even]
    # Row 2: [a_odd, b_odd, g_odd]  (free from input)
    r1 = a_even * a_odd + b_even
    r2 = a_even * b_odd
    r3 = a_even * g_odd + g_even
    # s1, s2, s3 = a_odd, b_odd, g_odd  (Row 2, no computation)

    # Phase 2: log2(k) layers of parallel prefix scan
    # At layer l, stride = 2^(l-1): M_{2^(l+1)}'[j] = M_{2^l}'[j] * M_{2^l}'[j-stride]
    for stride in [1, 2, 4, ..., k//2]:
        r1, r2, r3, a_odd, b_odd, g_odd = matrix_combine(
            (r1, r2, r3), (a_odd, b_odd, g_odd),   # M'[j]
            shift((r1, r2, r3), stride),             # M'[j-stride], row 1
            shift((a_odd, b_odd, g_odd), stride),    # M'[j-stride], row 2
        )

    # Phase 3: apply both rows to boundary [f_prev1, f_prev2, 1]
    f_even = r1 * f_prev1 + r2 * f_prev2 + r3           # Row 1 -> f(2x)
    f_odd  = a_odd * f_prev1 + b_odd * f_prev2 + g_odd  # Row 2 -> f(2x-1)

    # Unzip interleaved outputs into two consecutive vectors
    return unzip(f_even, f_odd)   # returns f[0..2k-1] in order
```

where `matrix_combine(A, B)` computes the two-row matrix product $A \cdot B$ (6 multiply-accumulates per entry), and `shift(v, stride)` shifts a vector by `stride` lanes, drawing boundary values from the previous block.

# Work Analysis

The total work per block of $2k$ outputs, measured in multiply-accumulate operations per lane:

| Step | Cost per lane |
|------|--------------|
| Phase 1: $M_2'$ (first row only) | 3 |
| Phase 2: $\log_2 k$ scan layers (6 per layer) | $6\log k$ |
| Phase 3: two row dot products | 2 |
| **Total** | $5 + 6\log k$ |

For $k = 16$: $5 + 6 \cdot 4 = 29$ operations for $2k = 32$ outputs, a **work multiplier of $29/32 \approx 0.91$ per output element**.

Comparing to the two approaches from the previous post, which each produce $k = 16$ outputs using $k$-wide vectors:

| Algorithm | Work per output ($k=16$) |
|-----------|--------------------------|
| Matrix prefix scan | $19/16 \approx 1.19$ |
| **Half-points scan (this post)** | **$29/32 \approx 0.91$** |
| $d_k/f_k$ decomposition | $14/16 \approx 0.875$ |

The half-points scan is cheaper per output than the matrix scan by about $1.3\times$, and comes close to the $d_k/f_k$ decomposition, though the decomposition remains slightly ahead.

The improvement over the plain matrix scan comes from amortizing the $O(\log k)$ overhead over $2k$ outputs instead of $k$, and from the first layer costing only 3 operations (not 6) because the second row of $M_2'$ is free.

# Why This Doesn't Apply to the $d_k/f_k$ Decomposition

One might wonder whether a similar trick can halve the work of the $d_k/f_k$ decomposition. It cannot. The $d_k/f_k$ formulas at each layer use values at *odd* offsets — for example, $d_{16}(x) = d_8(x)\cdot d_8(x-8) + d_7(x)\cdot b(x-7)\cdot d_7(x-9)$ requires $d_7(x-9)$, an odd-offset value. There is no way to skip odd positions, because those intermediate values are genuinely needed.

The matrix form avoids this by carrying both $f(x)$ and $f(x-1)$ in the same matrix, so the odd-position output falls out of the second row for free. The $d_k/f_k$ decomposition does not have this structure.

# Closing Thoughts

The half-points trick brings the matrix prefix scan's work per output below 1× scalar, making it competitive with the $d_k/f_k$ decomposition. One practical consideration: the algorithm processes blocks of $2k$ elements and requires zip/unzip (interleave/deinterleave) operations, which are cheap but not free on most architectures. The block size is also twice as large, which doubles the latency before the first output of each block is available — though this is generally not a concern for bulk image-processing workloads.
