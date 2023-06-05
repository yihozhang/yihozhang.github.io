---
bibliography: main.bib
csl: https://www.zotero.org/styles/acm-sig-proceedings-long-author-list
---

# Termination of Equality Saturation

**Theorem 1.** The following problem is R.E.-complete:

    Instance: a set of rewrite rules R, a term t.
    Question: does EqSat terminate with R and t?

**Proof.**
First, this problem is in R.E. since we can simply run EqSat with $R$ and $t$
 to test whether it terminates.
To show this problem is R.E.-hard, we reduce the termination problem of Turing machines to the termination of EqSat.
We use the technique by [@NARENDRAN1985343].
In particular, for each Turing machine $M$, 
 we produce a string rewriting system $R$ such that the equivalence closure of $R$, $(\approx_R)=\left(R\cup R^{-1}\right)^*$, satisfies that each equivalence class of $\approx_R$ 
 corresponds to a trace of of running the Turing machine on certain input.
As a result, the Turing machine halts if and only if the trace is finite if and only if
 EqSat terminates.

A Turing machine $M=(K,\Sigma, \Pi,\mu,q_0,\beta)$ consists of a set of states $K$, 
 the input and the tape alphabet $\Sigma$ and $\Pi$ (with $\Sigma\subseteq \Pi$), a set of transitions $\mu$, an initial state $q_0\in K$,
 and a special blanket symbol $\beta\in\Pi$. Each transition in $\mu$ is a quintuple in 
 $K\times \Pi\times \Pi\times \{L,R\} \times K$.
For example, transition $q_iabRq_j$ means if the current state is $q_i$ and the symbol
 being scanned is $a$, then replace $a$ with $b$, move the head to the right, 
 and transit to state $q_j$.
We assume the Turing machine is two-way infinite, so that the head can move in both directions indefinitely.
Each configuration of $M$ can be represented as $\rhd uq_i av \lhd$,
 where $\rhd$,$\lhd$ are left and right end  markers, 
 $u$ is the string to the left of the read/write head, $q_i$ is the current state,
 $a$ is the symbol being scanned, and $v$ is the string to the right.

For each such $M$, we define $\overline K=\{\overline q\mid q\in K\}$.
We also define $\overline \Sigma$, $\overline \Pi$ in a similar way. 
In our encoding, we use $\overline K$ to denote states 
 where the symbol being scanned is to the left of the state,
 and we use $\overline \Sigma$ and $\overline \Pi$ to denote
 alphabets that are to the left of the states.
Moreover, we introduce two sets of "dummy" symbols $L_z$ and $R_z$
 for $z$ ranges over $K\times (\{\lhd\}\cup \Pi)$
 and $(\{\rhd\}\cup \overline\Pi)\times \overline K$.
Let $D_L$ and $D_R$ be the set of all $L_z$ and $R_z$ respectively.

The rewriting system we are going to define works over the set of strings 
 $\textit{CONFIG}=\rhd (\overline\Pi\cup D_L)^*(K\cup \overline K)(\Pi\cup D_R)^*\lhd$.
We define a mapping from strings in the rewriting system to configurations of a Turing machine: 
 $\pi(w)$ converts each $\overline a\overline q_i$ to $q_ia$, removes dummy symbols $L_z$ and $R_z$, and replace $\overline a$ with $a$.


Now, for the given set of transitions, we define our string rewriting system $R$ as follows:

| transitions in $M$ | rewrites in $R$ |
|--------------------|----------------|
| $q_iabRq_j$        | $q_ia\leftarrow_R L_{q_ia}\overline bq_j$      |
|                    | $\overline a\overline q_i\leftarrow_R L_{\overline aq_i}\overline bq_j$      |
| $q_i\beta bRq_j$   | $q_i\lhd\leftarrow_R L_{q_i\lhd}\overline b q_j\lhd$      |
|                    | $\rhd \overline q_i\leftarrow_R \rhd L_{\rhd\overline q_i}\overline bq_j$      |
| $q_iabLq_j$        | $q_ia\leftarrow_R \overline q_j b R_{q_ia}$      |
|                    | $\overline a\overline q_i\leftarrow_R \overline q_j b R_{\overline a\overline q_i}$      |
| $q_i\beta bLq_j$    |  $q_i\lhd\leftarrow_R \overline q_jbR_{q_i\lhd}\lhd$      |
|                    | $\rhd \overline q_i\leftarrow_R \rhd\overline q_j b R_{\rhd\overline q_i}$      |

Moreover, for each $z$, we have the following two additional rewrite rules
\begin{align*}
q_iR_z&\leftarrow_R L_zL_zq_i\\
L_z\overline q_i&\leftarrow_R \overline q_iR_zR_z
\end{align*}

We define two types of strings. Type-A strings are strings where the symbol being scanned
 is to the immediate right of $q_i$ or to the immediate left of $\overline {q_i}$. 
In other words, 
 we call a string $s$ a type-A string if $s$ contains $q_ia$ or $\overline{aq_i}$.
Type-B strings are strings that are not type-A: 
 they are strings where there are dummy symbols in between the state and 
 the symbol being scanned.

Now, we observe that $R$ has several properties:

1. $R$ is convergent: it is obviously terminating since the size of each rule is decreasing.
 $R$ is also confluent by noticing that it has no critical pairs and is terminating.
2. For each type-A string $w$, then either
   * there exists no $w'$ with $w'\rightarrow_R w$ and $\pi(w)$ is a halting configuration.
   * there exists a unique $w'$ such that $w'\rightarrow_R w$ and $\pi(w)\vdash \pi(w')$, where $\vdash$ denotes one transition of the Turing machine.
3. If $w_0,w_1,\ldots$ is a sequence of type-B strings in *CONFIG*. such that $w_{i+1}\rightarrow_R w_{i}$,
 then $\pi(w_i)=\pi(w_{i+1})$ and the sequence is bounded in length, 
 since the state symbols $q_i$ and $\overline q_i$ move towards one end.

**Lemma.** Let $w_0=\rhd q_0s\lhd$ be an initial configuration.
$w_0$ is obviously in *CONFIG*. 
Moreover, Turing machine halts on $w_0$ if and only if $[w_0]_R$ is finite.

**Proof.**
Consider a sequence of *CONFIG* starting with $w_0$,
 $w_0\leftarrow_R w_1\leftarrow_R \ldots$.
By the above observations,
 it must have a subsequence of type-A strings
 $w_0\leftarrow_R^* w_{i_1}\leftarrow_R^* w_{i_2}\leftarrow_R^*\ldots$ with 
 $$\pi(w_0)=\ldots =\pi(w_{i_1}-1)\vdash \pi(w_{i_1})=\ldots=\pi(w_{i_2-1})\vdash \pi(w_{i_2})= \ldots.$$
 Moreover, the subsequence is bounded if and only if the original sequence is bounded.

Now we prove the claim:
* $\Leftarrow$:
 If $[w_0]_R$ is finite, then there is a unique finite sequence of $w_0\leftarrow_R w_1\leftarrow_R \ldots\leftarrow_R w_n$, where $\pi(w_i)\vdash\pi(w_{i+1})$ and $\pi(w_n)$ is a halting configuration and there exists no $w'$ with $w'\rightarrow_R w_n$.
 This implies a finite trace $w_0\vdash \pi(w_{i_1})\vdash\ldots\vdash \pi(w_{i_n})$.
 Since we only consider deterministic Turing machines, the Turing machine halts on $w_0$ with the final state $\pi(w_{i_n})$.
* $\Rightarrow$:
 Suppose otherwise $[w_0]_R$ is infinite. 
 Because $R$ is convergent, there must exist an infinite rewriting sequence
 to the unique normal form (that is, $w_0$): $w_0\leftarrow_R w_1 \leftarrow_R\ldots$.
 Therefore, there is an infinite subsequence
 $w_0\vdash \pi(w_{i_1})\vdash\ldots$
 This contradicts the fact that $w_0$ is halting. $\blacksquare$

Now we are ready to prove Theorem 1:

**Proof.**
Given a Turing machine $M$. We construct the following two-tape Turing machine $M'$:

```
M' alternates between the following two steps:
1. Simulate one transition of M on its first tape.
2. Read the string on its second tape as a number, compute the next prime number, 
  and write it to the second tape.
M' halts when M reachs an accepting state.
```
It is known that a two-tape Turing machine can be simulated using a standard Turing machine,
 so we assume $M'$ is a standard Turing machine and takes input string $(s_1,s_2)$, 
 where $s_1$ is the input on its first tape and $s_2$ is the input on its second tape.
Let $R'$ be the term rewriting system derived from $M'$ using the above encoding.
COMMENT: Above we are working with string rewriting system but here 
 it becomes a term rewriting system.
Given a string $s$, 
 $M$ halts on $s$ $\Leftrightarrow$ $[w]_{R'}$ is finite, where $w=q_0(s, 2)$. 
Now running EqSat with initial term $w$ and rewriting system $\leftrightarrow_{R'}$, we show EqSat terminates iff $M$ halts on $s$:

* $\Rightarrow$:
Suppose EqSat terminates with output E-graph $G$. 
We have $[w]_G=[w]_{R'}$.
Moreover, $[w]_G$ is regular, so $[w]_G$ is finite.
* $\Leftarrow$:
Suppose $M$ halts on $s$. This implies $[w]_{R'}$ is finite.
Because EqSat monotonically enlarge the set of represented terms, it has to stop in a finite number of iterations.

Because the halting problem of a Turing machine is undecidable, the termination problem of EqSat is undecidable as well. $\blacksquare$

# References
