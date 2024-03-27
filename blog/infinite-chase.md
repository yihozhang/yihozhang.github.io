---
title: Semantics of the infinite chase
author: Yihong Zhang
date: Mar 25, 2024
---

I was trying to grasp the deep chase literature these days and 
 I noticed there are two "folklore" claims in the literature that I cannot find proofs of.
Not all of these claims are trivial to prove,
 so in this blog post we will prove them.

**Theorem 1.** Given a set of dependencies $\Sigma$ and a database instance $I$, 
 it is R.E.-complete whether all chase sequences of $I$ with $\Sigma$ terminate.

While Deutsch et al. (2008) proved that this problem is undecidable,
 some follow-up papers (e.g. [Grahne and Onet](https://content.iospress.com/articles/fundamenta-informaticae/fi1627)) 
 claimed that this paper is R.E.-complete by referring to this paper.
At first it is unclear to me why this problem is in R.E.
After all, we are considering all chase sequences here,
 so one would expect some unbounded forall quantifiers here.
To state this problem in a more existential-oriented way, 
 a natural idea is to say there is no infinite path iff the lengths of all chase sequences are bounded ($\exists$ a bound of chase lengths such that ...).
But does this equivalence of conditions hold? 
It might be the case that all paths are finite, but the lengths of their paths are just unbounded.
For example, all natural numbers are finite, but there is no upper bound of natural numbers.

This is when I start to finally understand König's lemma.
The lemma states that every infinite tree either has a vertex of infinite degrees
 or an infinite path.
With this lemma the above equivalence is straightforward:
Consider the derivation tree of chase sequences.
Since at each step the number of possible firings is finite,
 the derivation tree is infinite if and only if it has an infinite path.
Moreover, the length of all chase sequences are unbounded if and only if the derivation tree is infinite.

**Theorem 2.** Given a set $\Sigma$ of TGDs and EGDs and a (possibly infinite) chase sequence $\mathcal{S}: I_0, I_1,\ldots$,
let $I_{\infty}=\bigcup_{i\geq 0}\bigcap_{j\geq i} I_j$. $I_{\infty}$ is a universal model of $\Sigma$.

In the original paper by [Fagin et al.](https://www.sciencedirect.com/science/article/pii/S030439750400725X),
 the universal model is only shown for the finite case: when the chase sequence is finite, the last database instance
 is a finite universal model. But Fagin et al. and many follow-up papers don't consider infinite universal models,
 so the semantics of a non-terminating chase sequence is unclear.
In [*Benchmarking the Chase*](https://dl.acm.org/doi/10.1145/3034786.3034796) by Benedikt et al., it was claimed that
 the semantics of chase sequences, terminating or not, is $I_{\infty}=\bigcup_{i\geq 0}\bigcap_{j\geq i} I_j$,
 but this claim is not proved in the paper.
 It is highly likely that this claim has been proved but I was just not able to find them. 
 But anyway, this is a fun exercise and thanks [Dan](https://homes.cs.washington.edu/~suciu) and [Remy](https://remy.wang) for teaching me how to prove it.

There are two things to prove here:
 (1) $I_{\infty}$ is a model and (2) For any model $K$, there is a homomorphism from $I_{\infty}$ to $K$.
Since this semantic coincides with that of Fagin et al. in the finite case, we will only consider cases where the chase sequence is infinite.
We will starting by proving (2). To do this, we need a basic lemma from [Fagin et al.](https://www.sciencedirect.com/science/article/pii/S030439750400725X): 
 If $I\xrightarrow{d,h} J$ is a chase step with trigger $h$ on dependency $d$,
 let $K$ be an instance such that $K\models d$ and there exists a homomorphism $h:I\rightarrow K$, then
 there exists a homomorphism $h':J\rightarrow K$.
Crucially, it can also be observed that $h|_{I\cap J}=h'|_{I\cap J}$ (the homomorphisms before and after agree on values that are not changed).

Let $K$ be a model, by repeatedly applying the above lemma, there are homomorphisms $h_i:I_i\rightarrow K$.
Define $J_i=\bigcap_{j\geq i} I_j$ and it is obvious $J_i\subseteq J_{i+1}$ and $J_i\subseteq I_i$.
We claim that there exists a sequence of $g_i: J_i\rightarrow K$, defined by $g_i=h_i|_{J_i}$,
 that satisfies $g_i\subseteq g_{i+1}$ (alternatively, $g_i=g_{i+1}|_{J_i}$).

Consider an arbitrary chase step $I_i\xrightarrow{d,h}I_{i+1}$.
We have 
$$\begin{align*}
g_{i+1}|_{J_i}
&=h_{i+1}|_{J_{i+1}\cup J_i}\quad \text{by dfn. of $g_{i+1}$}\\
&=h_{i+1}|_{J_i}\quad \text{since $J_i\subseteq J_{i+1}$}\\
&=h_{i+1}|_{I_i\cap I_{i+1}\cap J_{i+2}}\quad \text{by dfn. of $J_i$}\\
&=h_{i}|_{I_i\cap I_{i+1}\cap J_{i+2}}\quad\text{since $h_i|_{I_i\cap I_{i+1}}=h_{i+1}|_{I_i\cap I_{i+1}}$}\\
&=h_{i}|_{J_i}\quad\text{by dfn. of $J_i$}\\
&=g_i\quad\text{by dfn. of $g_i$}
\end{align*}
$$

Take $h_\infty=\bigcup_{i\geq 0} h_i$ and it is obvious that $h_\infty$ is a homomorphism from $I_\infty=\bigcup_{i\geq 0} J_i$ to $K$. This finishes (2).

<!-- Now we prove that $I_\infty$ is a model of $\Sigma$. Suppose for the sake of contradiction that 
 there exists a dependency $d\in \Sigma:\lambda(\vec{x})\rightarrow \phi(\vec{x})$ (where $\vec{x}$ are
 variables shared in both the head and the body),
 an active trigger (substitution) $h:\vec{x}\rightarrow \text{dom}(I_\infty)$
 such that $I_{\infty}\models \lambda(h(\vec{x}))$ and $I_{\infty}\not\models \phi(h(\vec{x}))$.
Since $\vec{x}$ is finite, there exists some $n$ such that the image of $h$ is included in $\text{dom}(J_n)$.
Suppose $d$ is a TGD and $\phi(\vec{x})=\exists \vec{z} \bigwedge_i R_i(\ldots)$.

Since the chase sequence is fair, there must exists some $i$ such that $I_i\xrightarrow{d, h} I_{i+1}$
 that fires $d$ with active trigger $h$ of $d$. -->
