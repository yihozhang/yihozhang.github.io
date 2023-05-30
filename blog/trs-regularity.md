---
bibliography: main.bib
csl: https://www.zotero.org/styles/acm-sig-proceedings-long-author-list
---

# Termination of Equality Saturation

**Theorem:** The following problem is R.E.-complete:

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
 $K\times \Pi\times \Pi\times \{L,R\} \times K $.
For example, transition $q_iabRq_j$ means if the current state is $q_i$ and the symbol
 being scanned is $a$, then replace $a$ with $b$, move the head to the right, 
 and transit to state $q_j$.
We assume the Turing machine is two-way infinite, so that the head can move in both directions indefinitely.
Each configuration of $M$ can be expressed as $\rhd uq_i av \lhd$,
 where $\rhd$,$\lhd$ are left and right end  markers, 
 $u$ is the string to the left of the read/write head, $q_i$ is the current state,
 $a$ is the symbol being scanned, and $v$ is the string to the right.

We will encode each configuration of $M$ as a string.
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
 $\textit{CONFIG}=\rhd (\overline\Pi\cup D_L)^*(K\cup \overline K)(\Pi\cup D_R)^*\lhd$
Finally, we define a mapping from strings in the rewriting system to configurations of a Turing machine: 
 $\pi(w)$ converts each $\overline a\overline q_i$ to $q_ia$, removes dummy symbols $L_z$ and $R_z$, and replace $\overline a$ with $a$.


Now, for the given set of transitions, we define our string rewriting system $R$ as follows:

| transitions in $M$ | rewrites in $R$ |
|--------------------|----------------|
| $q_iabRq_j$        | $q_ia\leftarrow L_{q_ia}\overline bq_j$      |
|                    | $\overline a\overline q_i\leftarrow L_{\overline aq_i}\overline bq_j$      |
| $q_i\beta bRq_j$   | $q_i\lhd\leftarrow L_{q_i\lhd}\overline b q_j\lhd$      |
|                    | $\rhd \overline q_i\leftarrow \rhd L_{\rhd\overline q_i}\overline bq_j$      |
| $q_iabLq_j$        | $q_ia\leftarrow \overline q_j b R_{q_ia}$      |
|                    | $\overline a\overline q_i\leftarrow \overline q_j b R_{\overline a\overline q_i}$      |
| $q_i\beta bLq_j$    |  $q_i\lhd\leftarrow \overline q_jbR_{q_i\lhd}\lhd$      |
|                    | $\rhd \overline q_i\leftarrow \rhd\overline q_j b R_{\rhd\overline q_i}$      |

Moreover, for each $z$, we add the following two rewrite rules
\begin{align*}
q_iR_z&\leftarrow L_zL_zq_i\\
L_z\overline q_i&\leftarrow \overline q_iR_zR_z
\end{align*}

Now, we define two types of strings. Type-A strings are strings where the symbol being scanned
 is to the immediate right of $q_i$ or to the immediate left of $\overline {q_i}$. 
In other words, 
 we call a string $s$ a type-A string if $s$ contains $q_ia$ or $\overline{aq_i}$.
Type-B strings are strings that are not type-A: 
 they are strings where there are dummy symbols in between the state and 
 the symbol being scanned.

Now, we observe that $R$ has several properties:
* $R$ is convergent: it is obviously terminating since the size of each rule is decreasing.
 $R$ is confluent by noticing that it has no critical pairs and is terminating. 
* For each type-A string $w$, there exists a unique $w'$ such that $w'\rightarrow w$ and $\pi(w)\vdash \pi(w')$, where $\vdash$ denotes one transition in running the Turing machine.
* If $w_0,w_1,\ldots$ is a sequence of type-B strings in \textit{CONFIG}. such that $w_{i+1}\rightarrow_R w_{i}$, then 

# References
