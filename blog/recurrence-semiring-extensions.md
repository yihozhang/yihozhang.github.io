---
title: "Dilation-like identities for recurrences over semirings: three extensions"
author: Yihong Zhang
date: July 25, 2026
---

In our paper submission, we considered recurrences over semirings and how to vectorize them.
In particular, we developed two transformations that we collectively call "dilation":
one works with rings, and the other works with idempotent semirings.
In both cases, we use algebraic identities to transform an input recurrence into one
whose recurrence kernel has a larger stride.
A larger stride allows more values of a recurrence to be computed in parallel, enabling vectorization.

However, a broader class of dilation-like identities can be derived from other properties of the semiring.
In this post, I will show three extensions of the dilation-like identities from the paper.
Each one assumes an additional property of the semiring:

1. The semiring is a zero-divisor-free ring with a primitive $m$-th root of unity. This generalizes the paper's ring dilation.
2. The semiring is a ring of prime characteristic $p$. This specializes the ring setting.
3. The semiring is $c$-saturating. An example of a $c$-saturating semiring is saturating arithmetic. This also generalizes the paper's dilation for idempotent semirings.

## What is a dilation-like identity?

Let us first define what a dilation-like identity is. Consider a recurrence of the form

$$
F=\operatorname{Rec}(K,G),
\tag{1}
$$

for a causal, time-invariant kernel $K$ and a signal $G$. This recurrence computes the fixed-point solution
to $F=K\otimes F\oplus G$.
Throughout this post, we only consider commutative semirings, so that kernels commute under convolution.

Suppose all nonzero taps of $K$ occur at offsets divisible by $s$. We say
that $K$ has stride $s$. A dilation-like identity has the form

$$
\boxed{
\operatorname{Rec}(K,G)
=
\operatorname{Rec}(L,P\otimes G)
}
\tag{2}
$$

If the stride of $L$ is $ms$, we say that Equation (2)
is a factor-$m$ **dilation**, and we call $P$ the **prefilter**.

It is helpful to consider dilation-like identities over rings.
For rings, the above identity is equivalent to the following:

$$
\begin{aligned}
I\ominus L
&=
P\otimes(I\ominus K)\\
L
&=
I\ominus P\otimes(I\ominus K)\\
\end{aligned}
\tag{3}
$$

To see this, note that convolution with $I\ominus K$ is the inverse operation of
the recurrence $\operatorname{Rec}(K,\cdot)$. All kernels in this discussion are
time-invariant, so convolutions and recurrences commute.

Therefore, finding a dilation-like identity over a ring largely reduces to finding
an appropriate prefilter $P$ for which $L$ is causal and has a larger stride.

In the paper, we used two dilation-like identities. 

* When the semiring is a ring, write a kernel with stride $s$ as $A\oplus B$,
   where $A$ contains the taps at offsets divisible by $2s$ and $B$ contains the taps at offsets congruent to $s$ modulo $2s$. We have 
  $$
  \operatorname{Rec}(A\oplus B,G)
  =
  \operatorname{Rec}\!\left(
    A\oplus A\ominus A^2\oplus B^2,\,
    (I\ominus A\oplus B)\otimes G
  \right).
  \tag{4}
  $$
  Every term in the new recurrence kernel, $A$, $A^2$, and $B^2$, has taps
  only at multiples of $2s$, so the new kernel has stride $2s$.
* When the recurrence is over an idempotent semiring, also known as a dioid, we have
  $$
  \operatorname{Rec}(A\oplus B,G)
  =
  \operatorname{Rec}\!\left(
    A\oplus B^2,\,
    (I\oplus B)\otimes G
  \right).
  \tag{5}
  $$
  With a slight generalization,
  $$
  \operatorname{Rec}(\bigoplus_{i=1}^{n}A_i,G)
  =
  \operatorname{Rec}\!\left(
    \bigoplus_{i=1}^{n}A_i^m,\,
    \bigotimes_{i=1}^{n}\left(\bigoplus_{j=0}^{m-1}A_i^j\right)\otimes G
  \right).
  \tag{6}
  $$
  
  Let each $A_i$ be a singleton kernel containing one tap of
  $\bigoplus_{i=1}^{n}A_i$. Replacing $A_i$ by $A_i^m$ multiplies its
  offset by $m$, while the prefilter accounts for the intermediate powers
  $I,A_i,\ldots,A_i^{m-1}$.
  
The following sections show a broader class of identities that generalize
these two identities.

## Extension 1: Zero-divisor-free rings with primitive $m$-th roots of unity

Let us consider the case in which the algebraic structure is a ring with a primitive $m$-th root of unity.
We say a value $\omega$ is an $m$-th root of unity if
$\omega^m=1_\tau$.
A ring has $\ominus_\tau1_\tau$ as a second root of unity, since $(\ominus_\tau1_\tau)^2=1_\tau$.
An $m$-th root of unity $\omega$ is *primitive* if $\omega^r\neq1_\tau$ for every integer $r$ with $1\leq r<m$.
An example is the ring of complex numbers, where, for every $m$,
$$
\omega=e^{2\pi i/m}
$$
is a primitive $m$-th root of unity: raising it to the $m$-th power gives $1$.
Note that the second root of unity $\ominus_\tau1_\tau$ is not necessarily primitive,
because some rings satisfy $\ominus_\tau1_\tau=1_\tau$.

Let $K$ be a causal, time-invariant kernel with stride $s$. Define a transformation
$\rho$ on such kernels by

$$
\rho(K)[ns]
=
\omega^{n}K[ns].
\tag{7}
$$

In other words, $\rho(K)$ multiplies every tap of $K$ at offset $ns$ by $\omega^{n}$.
We have $\rho(K_1\oplus K_2)=\rho(K_1)\oplus\rho(K_2)$ and $\rho(K_1\otimes K_2)=\rho(K_1)\otimes\rho(K_2)$.
Denote $j$ repeated applications of $\rho$ by $\rho^j$; then
$\rho^j(K)[ns]=\omega^{jn}K[ns]$.
Because $\omega^m=1_\tau$, the $m$-th application of $\rho$ returns the original kernel: $\rho^m=\textsf{id}$.

Suppose the ring satisfies the implication
$a\otimes_\tau b=0_\tau\Rightarrow a=0_\tau\text{ or }b=0_\tau$; such a
ring is called **zero-divisor-free**. Then $K$ is a fixed point of $\rho$
(that is, $\rho(K)=K$) if and only if every nonzero tap of $K$ occurs at an
offset divisible by $ms$.
The backward direction follows from $\omega^m=1_\tau$.
For the forward direction, suppose $\rho(K)=K$. Then for every $n$,

$$
\begin{aligned}
K[ns] &= \omega^{n}K[ns]\\
(1_\tau\ominus_\tau\omega^{n})\otimes_\tau K[ns] &= 0_\tau.
\end{aligned}
$$

Together, the zero-divisor-free assumption and the primitivity of $\omega$
imply that either $n$ is divisible by $m$ or $K[ns]=0_\tau$.


We can now define two finite kernels:

$$
P_m(K)
=
\bigotimes_{j=1}^{m-1}
  \left(I\ominus \rho^j(K)\right)
\tag{8}
$$

and

$$
L_m(K)
=
I\ominus
\bigotimes_{j=0}^{m-1}
  \left(I\ominus \rho^j(K)\right).
\tag{9}
$$

Because the kernels are time-invariant, their convolutions commute,
so Equations (8) and (9) give

$$
\begin{aligned}
I\ominus L_m(K)
&=
\bigotimes_{j=0}^{m-1}
  \left(I\ominus \rho^j(K)\right)\\
&=
P_m(K)\otimes(I\ominus K).
\end{aligned}
$$

This is exactly the identity in Equation (3), so

$$
\boxed{
\operatorname{Rec}(K,G)
=
\operatorname{Rec}\!\left(
  L_m(K),P_m(K)\otimes G
\right).
}
\tag{10}
$$

The new recurrence kernel $L_m(K)$ is causal: expanding the product in
Equation (9) gives $I$ plus terms supported on positive offsets, so $L_m(K)$
has no tap at offset $0$.
Moreover, $L_m(K)$ is a fixed point of $\rho$, because
$$
\begin{aligned}
\rho(L_m(K))
&= \rho\left(I\ominus
\bigotimes_{j=0}^{m-1}
  \left(I\ominus \rho^j(K)\right)\right)\\
&= I\ominus
\bigotimes_{j=0}^{m-1}
  \rho\left(I\ominus \rho^j(K)\right)\\
&= I\ominus
\bigotimes_{j=1}^{m}
  \left(I\ominus \rho^j(K)\right)\\
&= L_m(K).
\end{aligned}
$$
Therefore, if the ring is zero-divisor-free,
$L_m(K)$ has stride $ms$.

(Side note suggested by ChatGPT and Claude: in algebraic language, $\rho$ is the automorphism of the
offset-graded kernel algebra induced by the $\mathbb Z/m$ grading, and
$\bigotimes_{j=0}^{m-1}\rho^j(\cdot)$ is the norm of the cyclic group
generated by $\rho$. The norm is $\rho$-invariant, which is exactly the
argument above.)

### Recovering the paper's ring dilation

Take $m=2$, so $\omega=\ominus_\tau1_\tau$ is a second root of unity. Write $K=A\oplus B$, where $A$ contains
the even-offset taps and $B$ the odd-offset taps. Then

$$
\rho(K)=A\ominus B.
$$

Equations (8) and (9) become

$$
P_2(K)=I\ominus A\oplus B
$$

and

$$
\begin{aligned}
L_2(K)
&=
I\ominus
(I\ominus A\ominus B)
\otimes
(I\ominus A\oplus B)\\
&=
A\oplus A\ominus A^2\oplus B^2.
\end{aligned}
$$

This recovers the paper's dilation for recurrences over rings.
Note that deriving the paper's binary ring dilation requires neither the
zero-divisor-free assumption nor the primitivity of $\ominus_\tau1_\tau$.
Those assumptions were only used to establish the implication that
$\rho(K)=K$ forces $K$ to have stride $ms$.

### Example: tripling the stride of a real recurrence

Take $m=3$ and $\omega=e^{2\pi i/3}$, and let $K=[0,a,b]$ be a kernel with
stride $s=1$ and real taps. Then $\rho(K)=[0,\omega a,\omega^2b]$ and
$\rho^2(K)=[0,\omega^2a,\omega b]$, and Equations (8) and (9) give

$$
\begin{aligned}
P_3(K)&=[1,\;a,\;a^2+b,\;-ab,\;b^2],\\
L_3(K)&=[0,0,0,\;a^3+3ab,\;0,0,\;b^3].
\end{aligned}
$$

The new recurrence kernel has taps only at offsets $3$ and $6$, as promised.
Note also that both results are real, even though $\rho(K)$ has complex taps.
This is not luck: for every $m$, if all taps of $K$ are reals, then so do $P_m(K)$ and
$L_m(K)$.
To see this, write $\bar X$ for the kernel obtained by replacing every tap
of $X$ with its complex conjugate, so that $X$ has real taps exactly when
$\bar X=X$, and note that conjugation respects $\oplus$ and $\otimes$.
Because $\bar\omega=\omega^{m-1}$, a kernel $K$ with real taps satisfies
$\overline{\rho^j(K)}=\rho^{m-j}(K)$, so conjugation only permutes the factors
of the products in Equations (8) and (9).
Hence $\overline{P_m(K)}=P_m(K)$ and $\overline{L_m(K)}=L_m(K)$: their taps are
real for every $m$, and the root of unity is only used as a device for the derivation.

## Extension 2: Rings of prime characteristic

Suppose that the sum of $p$ copies of $1_\tau$ is zero:

$$
\underbrace{
1_\tau\oplus_\tau\cdots\oplus_\tau1_\tau
}_{p\text{ copies}}
=0_\tau.
\tag{11}
$$

The least positive number of copies for which this happens is called the
**characteristic**. For example, arithmetic modulo $3$ has characteristic
$3$:

$$
1+1+1=0\pmod 3.
$$

If $p$ copies
of $1_\tau$ add to zero, then for any coefficient $a$,

$$
\underbrace{a\oplus_\tau\cdots\oplus_\tau a}_{p\text{ copies}}
=
\left(
  \underbrace{1_\tau\oplus_\tau\cdots\oplus_\tau1_\tau}_{p\text{ copies}}
\right)\otimes_\tau a
=0_\tau.
$$

Therefore the sum of $p-1$ copies of $a$ is an additive inverse of $a$: every
semiring of finite characteristic is already a ring, so finite characteristic
is a special case of ring arithmetic.

### What changes when the characteristic is prime?

Assume now that the characteristic $p$ is prime. For any time-invariant
kernels $X$ and $Y$ and any exponent $q\geq1$, the binomial theorem gives

$$
(X\oplus Y)^q
=
\bigoplus_{r=0}^{q}
\binom{q}{r}X^r\otimes Y^{q-r}.
$$

Now take $q=p^h$ with $h\geq1$. Every intermediate binomial coefficient
$\binom{q}{r}$, for $0<r<q$, is then divisible by $p$, so Equation (11)
makes every mixed term vanish, leaving

$$
(X\oplus Y)^q=X^q\oplus Y^q.
\tag{12}
$$

This is the **Frobenius identity**.

In the paper, we have the following unrolling identity for any semiring:

$$
\operatorname{Rec}(K,G)
=
\operatorname{Rec}\!\left(
  K^q,\,
  \bigoplus_{i=0}^{q-1} K^i\otimes G
\right).
\tag{13}
$$

Normally, this identity is not useful for dilation because
$K^q$ expands to mixed products of taps of $K$ and does not have a larger stride.

Prime characteristic removes exactly those mixed products. Write the
time-invariant kernel $K$ as a sum of singleton kernels, one for each tap of $K$:

$$
K=\bigoplus_{i=1}^{n} K_i.
$$

Taking $q=p^h$ and applying the Frobenius identity gives

$$
K^q
=
\bigoplus_{i=1}^{n} K_i^q.
$$

Thus, in a ring of prime characteristic $p$, for any $q=p^h$ with $h\geq1$,
$$
\boxed{
\operatorname{Rec}(K,G)
=
\operatorname{Rec}\!\left(
  \bigoplus_{i=1}^{n} K_i^q,\,
  \bigoplus_{i=0}^{q-1} K^i\otimes G
\right)
}
\tag{14}
$$

If $K$ originally has stride $s$, the new feedback kernel has stride
$qs$.

### Example: arithmetic modulo $3$

Consider the ring of integers modulo $3$. It has prime characteristic $p=3$.
Let the kernel be
$K=[0,2,1]$. We have

$$
\begin{aligned}
K^3
&=
[0,0,0, 2^3,0,0, 1]\\
&=
[0,0,0, 2,0,0, 1],\\
I\oplus K\oplus K^2 &= 
[1]\oplus[0,2,1]\oplus[0,0,1,1,1]\\
&=
[1,2,2,1,1].
\end{aligned}
$$

The recurrence can therefore be rewritten as

$$
\operatorname{Rec}(K,G)
=
\operatorname{Rec}\!\left(
  [0,0,0, 2,0,0, 1],\,
  [1,2,2,1,1]\otimes G
\right).
$$
The stride of the feedback kernel has been tripled.

This result applies naturally to modular arithmetic and other rings of prime
characteristic. Because finite characteristic already implies the ring
properties, this transformation can be viewed as a refinement of the paper's ring setting.

## Extension 3: $c$-saturating semirings

Fix an integer $c\geq1$. For a nonnegative integer $n$, write

$$
[n]_\tau
=
\underbrace{
1_\tau\oplus_\tau\cdots\oplus_\tau1_\tau
}_{n\text{ copies}},
\qquad [0]_\tau=0_\tau.
$$

We will say that a semiring is *$c$-saturating* if

$$
[c]_\tau=[c+1]_\tau.
\tag{15}
$$

Adding more copies of $1_\tau$ to both sides shows that

$$
[n]_\tau=[c]_\tau
\qquad\text{when }n\geq c.
\tag{16}
$$

Multiplying both sides by any value $a$ gives

$$
\underbrace{a\oplus_\tau\cdots\oplus_\tau a}_{n\text{ copies}}
=
\underbrace{a\oplus_\tau\cdots\oplus_\tau a}_{c\text{ copies}}
\qquad(n\geq c).
\tag{17}
$$

In other words, addition saturates at $c$ copies of any value. A natural example of this is saturation arithmetic capped at $c$.

When $c=1$, Equation (15) says
$1_\tau=1_\tau\oplus_\tau1_\tau$, which is equivalent to $a=a\oplus_\tau a$ for every $a$.
This recovers (additive) idempotence.
Thus $c$-saturation is a generalization of idempotence.

As an aside, the database literature has studied $p$-stability as a
sufficient condition for the convergence of Datalog programs over semirings.
A semiring is said to be **$p$-stable** when
$$
1_\tau\oplus_\tau a\oplus_\tau\cdots\oplus_\tau a^p
=
1_\tau\oplus_\tau a\oplus_\tau\cdots\oplus_\tau a^p\oplus_\tau a^{p+1}
\tag{18}
$$
for every coefficient $a$. Setting $a=1_\tau$ gives the condition for $(p+1)$-saturation.
Thus every $p$-stable semiring is $(p+1)$-saturating. 
The converse, however, does not hold in general.


### Deriving the prefilter

Over an idempotent semiring, a path generated twice counts the same as a path
generated once, so the prefilter in Equation (5) only has to supply the powers
of $B$ that the dilated kernel skips. Over a $c$-saturating semiring,
multiplicities below $c$ are still visible, so the prefilter must repair those
as well.

Let $A$ and $B$ be causal, time-invariant kernels, and fix an integer $m\geq1$.
We look for a dilation-like identity whose dilated form is
$\operatorname{Rec}(A\oplus B^m,P_{m,c}(A,B)\otimes G)$, where the prefilter
$P_{m,c}(A,B)$ is defined in terms of $A$ and $B$. Our goal is to find such a
prefilter. Below, $\langle n\rangle$ denotes the kernel with a single tap of
semiring value $[n]_\tau$ at offset $0$, so that multiplying a kernel by
$\langle n\rangle$ adds $n$ copies of it.

$$
\begin{aligned}
    \operatorname{Rec}(A\oplus B,G) &= \operatorname{Rec}(A\oplus B^m,P_{m,c}(A,B)\otimes G)\\
    \operatorname{Rec}(A\oplus B,G) &=  (A\oplus B^m)\otimes \operatorname{Rec}(A\oplus B^m,P_{m,c}(A,B)\otimes G)\oplus P_{m,c}(A,B)\otimes G\\
    \operatorname{Rec}(A\oplus B,G) &= (A\oplus B^m)\otimes \operatorname{Rec}(A\oplus B,G)\oplus P_{m,c}(A,B)\otimes G\\
    \bigoplus_{i,j\geq 0}   \left\langle\binom{i+j}{j}\right\rangle\otimes A^i\otimes B^j \otimes G &= \left(P_{m,c}(A,B)\oplus \bigoplus_{i,j\geq 0} (A\oplus B^m)\otimes \left\langle\binom{i+j}{j}\right\rangle\otimes A^i\otimes B^j \right)\otimes G
\end{aligned}
$$

Since we want this to hold for every $G$, it suffices that the two kernels agree:



$$
\begin{aligned}
\bigoplus_{i,j\geq 0}\left\langle\binom{i+j}{j}\right\rangle\otimes A^i\otimes B^j  &=
P_{m,c}(A,B)\oplus \bigoplus_{i,j\geq 0} (A\oplus B^m)\otimes \left\langle\binom{i+j}{j}\right\rangle\otimes A^i\otimes B^j
\\
&= P_{m,c}(A,B)\\
&\quad\quad \oplus\bigoplus_{i,j\geq 0} \left\langle\binom{i+j}{j}\right\rangle\otimes A^{i+1}\otimes B^j \\
&\quad\quad \oplus \bigoplus_{i,j\geq 0}  \left\langle\binom{i+j}{j}\right\rangle\otimes A^i\otimes B^{j+m} \\
    &= P_{m,c}(A,B)\oplus \bigoplus_{i,j\geq 0} 
    \left\langle\mathbf 1_{i>0}\binom{i+j-1}{j}
+
\mathbf 1_{j\geq m}\binom{i+j-m}{j-m}\right\rangle
     \otimes A^i\otimes B^j \\
\end{aligned}
$$

Let $N_{i,j}=\binom{i+j}{j}$ and $R_{m,i,j}=\mathbf 1_{i>0}\binom{i+j-1}{j}+\mathbf 1_{j\geq m}\binom{i+j-m}{j-m}$, so that $N_{i,j}$ and $R_{m,i,j}$ are the multiplicities of $A^i\otimes B^j$ on the left- and right-hand sides of the equation above.
Note that 
$$
\begin{aligned}
N_{i,j}=\binom{i+j}{j} &= \binom{i+j-1}{j} + \binom{i+j-1}{j-1} \\
&\geq \binom{i+j-1}{j} + \binom{i+j-m}{j-m}\geq R_{m,i,j}.
\end{aligned}
$$
The following definition of $P_{m,c}(A, B)$ satisfies the above equation:
$$
\begin{aligned}
P_{m,c}(A,B) &= \bigoplus_{i,j\geq 0} \left\langle D_{m,i,j}\right\rangle\otimes A^i\otimes B^j
\\
&\quad\quad\text{where }D_{m,i,j}=\begin{cases}
    0&\text{ if $R_{m,i,j}\geq c$}\\
    N_{i,j}-R_{m,i,j}&\text{ otherwise}
\end{cases}
\end{aligned}
$$
Essentially, it compensates for the difference between $N_{i,j}$ and $R_{m,i,j}$ when $R_{m,i,j}<c$.
For $P_{m,c}(A,B)$ to be a well-defined kernel, it must have finitely many
nonzero taps. This is true over $c$-saturating semirings, where only finitely many pairs $(i,j)$
have $D_{m,i,j}\neq 0$, because for all sufficiently large $(i,j)$ the
multiplicity $R_{m,i,j}$ either saturates or already equals $N_{i,j}$.

More precisely, we claim that $D_{m,i,j}=0$ whenever $i\geq c$ or $j\geq m+c$.
Throughout, we use the conventions $\binom{n}{k}=0$ for $k<0$ and for
$k>n\geq0$.

Let us first check this claim on the axes (i.e., $i=0$ or $j=0$).
They correspond to paths made of $A$'s only
or of $B$'s only, and the multiplicity is $1$ on both
sides of the equation.
When $j=0$ and $i\geq1$, $R_{m,i,0}=\binom{i-1}{0}=1=N_{i,0}$.
When $i=0$ and $j\geq m$, $R_{m,0,j}=\binom{j-m}{j-m}=1=N_{0,j}$.
Thus $D_{m,i,j}=0$ in both cases.

Off the axes, the multiplicity reaches the cap. First, when
$i\geq c$ and $j\geq1$, the first summand of $R_{m,i,j}$ already suffices:
$$
\begin{aligned}
\mathbf 1_{i>0}\binom{i+j-1}{j}
+
\mathbf 1_{j\geq m}\binom{i+j-m}{j-m}
&\geq \binom{i+j-1}{j}=\binom{i+j-1}{i-1}\\
&\geq 
\binom{i}{i-1}
\\
&= i\geq c.
\end{aligned}
$$
Second, when $j\geq m+c$ and $i\geq1$, the second summand already suffices:
$$
\begin{aligned}
\mathbf 1_{i>0}\binom{i+j-1}{j}
+
\mathbf 1_{j\geq m}\binom{i+j-m}{j-m}
&\geq
\binom{i+j-m}{j-m}=\binom{i+j-m}{i}\\
&\geq
\binom{j-m+1}{1}\\
&= j-m+1\geq c+1.
\end{aligned}
$$
In both cases $R_{m,i,j}\geq c$, so $D_{m,i,j}=0$ by
definition.

Together, we have shown that $D_{m,i,j}=0$ whenever $i\geq c$ or $j\geq m+c$.
Therefore,
$$
P_{m,c}(A,B) = \bigoplus_{\substack{0\leq i< c\\ 0\leq j< m+c}} \left\langle D_{m,i,j}\right\rangle\otimes A^i\otimes B^j
$$
is a finite kernel.
Substituting this definition into the equation above, we can verify $F=\operatorname{Rec}(A\oplus B,G)$ satisfies
$F=(A\oplus B^m)\otimes F \oplus P_{m,c}(A,B)\otimes G$, and this fixed-point
equation has a unique solution. Therefore
$$
\boxed{
\operatorname{Rec}(A\oplus B,G)
=
\operatorname{Rec}\!\left(
  A\oplus B^m,\,
  P_{m,c}(A,B)\otimes G
\right).
}
\tag{19}
$$


### Two examples

When $c=1$,

$$
\begin{aligned}
P_{m,1}(A,B)
&= \bigoplus_{ 0\leq j< m+1} \left\langle D_{m,0,j}\right\rangle \otimes  B^j\\
&= \bigoplus_{ 0\leq j< m+1} 
\left\langle\begin{cases}
    0&\text{ if $\mathbf 1_{j\geq m}\geq 1$}\\
    1-\mathbf 1_{j\geq m}&\text{ otherwise}
\end{cases}\right\rangle \otimes  B^j\\
&= \bigoplus_{ 0\leq j< m} B^j 
\end{aligned}
$$

and the dilation identity becomes

$$
\operatorname{Rec}(A\oplus B,G)
=
\operatorname{Rec}\!\left(
  A\oplus B^m,\,
  \left(\bigoplus_{0\leq j<m}B^j\right)\otimes G
\right).
\tag{20}
$$

This is exactly the dilation identity for idempotent semirings in the paper.

For $c=2$ and $m=2$, the finite prefilter is

$$
\begin{aligned}
P_{2,2}(A,B)&=\bigoplus_{\substack{0\leq i< 2\\ 0\leq j< 4}} \left\langle D_{2,i,j}\right\rangle\otimes A^i\otimes B^j\\
&=
\bigoplus_{ 0\leq j< 2} B^j \oplus
\bigoplus_{\substack{0\leq j< 4}}
\left\langle\begin{cases}
    0&\text{ if $R_{2,1,j}\geq 2$}\\
    N_{1,j}-R_{2,1,j}&\text{ otherwise}
\end{cases}\right\rangle\otimes A\otimes B^j\\
&=
\bigoplus_{ 0\leq j< 2} B^j \oplus
\bigoplus_{\substack{0\leq j< 4}}
\left\langle\begin{cases}
    0&\text{ if $\mathbf 1_{j\geq 2}\binom{j-1}{j-2}\geq 1$}\\
    N_{1,j}-1-\mathbf 1_{j\geq 2}\binom{j-1}{j-2}&\text{ otherwise}
\end{cases}\right\rangle\otimes A\otimes B^j
\\
&=
\bigoplus_{ 0\leq j< 2} B^j \oplus
\bigoplus_{\substack{0\leq j< 2}}
\left\langle
    N_{1,j}-1
\right\rangle\otimes A\otimes B^j
\\
&=
I\oplus B\oplus A\otimes B
% &=
% \bigoplus_{ 0\leq j< m} B^j 
% &=
% \bigoplus_{\substack{0\leq i< 2\\ 0\leq j< 4}}
% \left[\left.\begin{cases}
%     0&\text{ if $R_{m,i,j}\geq c$}\\
%     N_{i,j}-R_{m,i,j}&\text{ otherwise}
% \end{cases}\right\}
% \right]_\tau\otimes A^i\otimes B^j\\
\end{aligned}
$$

so

$$
\operatorname{Rec}(A\oplus B,G)
=
\operatorname{Rec}\!\left(
  A\oplus B^2,\,
  (I\oplus B\oplus A\otimes B)\otimes G
\right).
\tag{21}
$$

The extra $A\otimes B$ term is necessary because both paths $A\otimes B$ and
$B\otimes A$ must be accounted for, and a $2$-saturating
semiring still distinguishes one copy from two. 
For longer mixed paths, once the new recurrence operator produces at least
two copies, additional copies arising from different orderings no longer
matter.

### Example: arithmetic that counts only up to $c$

For $c\geq1$, consider the values

$$
\mathbb N_{\leq c}=\{0,1,\ldots,c\}
$$

with

$$
x\oplus_\tau y=\min(c,x+y),
\qquad
x\otimes_\tau y=\min(c,xy).
$$

This is a semiring, and it is
$c$-saturating because adding one more copy after reaching $c$ changes
nothing. It is useful for problems that care how many paths exist but do not
need the exact count once it reaches $c$.

The prefilter $P_{m,c}(A,B)$ grows with both $c$ and $m$: the (rather
conservative) bound above leaves at most $c\cdot(m+c)$ candidate pairs $(i,j)$,
hence at most that many $A^i\otimes B^j$ terms. The transformation is therefore
most attractive for small saturation caps, and is unlikely to be practical
with, for example, saturating arithmetic over 32-bit integers.


## Conclusion

To summarize, we have introduced three extensions of the dilation-like identities from the paper:

* When the recurrence is over a ring with an $m$-th root of unity, we have
  $$
  \boxed{
  \operatorname{Rec}(K,G)
  =
  \operatorname{Rec}\!\left(
    L_m(K),P_m(K)\otimes G
  \right).
  }
  $$
  If the ring is moreover zero-divisor-free and the root is primitive, then
  $L_m(K)$ has stride $ms$, so this is a factor-$m$ dilation.
* When the recurrence is over a ring of prime characteristic $p$, then, for
  any $q=p^h$ with $h\geq1$, writing $K=\bigoplus_{i=1}^{n}K_i$ as a sum of
  singleton kernels, one for each tap of $K$, we have
  $$
  \boxed{
  \operatorname{Rec}(K,G)
  =
  \operatorname{Rec}\!\left(
    \bigoplus_{i=1}^{n} K_i^q,\,
    \bigoplus_{i=0}^{q-1} K^i\otimes G
  \right)
  }
  $$
* When the recurrence is over a $c$-saturating semiring, we have
  $$
  \boxed{
  \operatorname{Rec}(A\oplus B,G)
  =
  \operatorname{Rec}\!\left(
    A\oplus B^m,\,
    P_{m,c}(A,B)\otimes G
  \right).
  }
  $$
