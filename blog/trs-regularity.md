---
bibliography: main.bib
csl: https://www.zotero.org/styles/acm-sig-proceedings-long-author-list
geometry: margin=2cm
title: The Termination Problem of Equality Saturation is Undecidable
author: Yihong Zhang
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
 corresponds to a trace of the Turing machine.
As a result, the Turing machine halts
 iff its trace is finite
 iff the corresponding equivalence class in $R$ is finite
 iff EqSat terminates.

In this proof, we consider a degenerate form of EqSat that works with *string* rewriting systems
 instead of term rewriting systems.
Every string corresponds to a term, and every string rewrite rule corresponds to a rewrite rule.
For example, the string $uvw$ corresponds to a term $u(v(w(\epsilon)))$, where $u(\cdot), v(\cdot), w(\cdot)$
 are unary functions and $\epsilon$ is a constant,
 and a string rewrite rule $uvw\rightarrow vuw$ corresponds to a (linear) term rewriting rule $u(v(w(x)))\rightarrow v(u(w(x)))$
 where $x$ is a variable.


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
We say $w_1\vdash_M w_2$ if configuration $w_1$ can transit to configuration $w_2$ in a Turing machine $M$, and we omit $M$ when it's clear from the context.

It is useful to define several sets of symbols for our construction.
For each Turing machine $M$, we define $\overline K=\{\overline q\mid q\in K\}$.
We also define $\overline \Sigma$, $\overline \Pi$ in a similar way. 
In our encoding, we use $\overline K$ to denote states 
 where the symbol being scanned is to the left of the state,
 and we use $\overline \Sigma$ and $\overline \Pi$ to denote
 alphabets that are to the left of the states.
Moreover, we introduce two sets of "dummy" symbols $L_z$ and $R_z$
 for $z$ ranges over $K\times (\{\lhd\}\cup \Pi)$
 and $(\{\rhd\}\cup \overline\Pi)\times \overline K$.
Let $D_L$ and $D_R$ be the set of all $L_z$ and $R_z$ respectively.
We use these dummy symbols to make the string rewriting system that we will later define Church-Rosser.

The rewriting system we are going to define works over the set of strings 
 $\textit{CONFIG}=\rhd (\overline\Pi\cup D_L)^*(K\cup \overline K)(\Pi\cup D_R)^*\lhd$.
 Strings in *CONFIG* is in a many-to-one mapping, denoted as $\pi$, to configurations of a Turing machine.
$\pi(w)$ converts each $\overline a\overline q_i$ to $q_ia$, removes dummy symbols $L_z$ and $R_z$, and replace $\overline a$ with $a$.
For example $\pi(\rhd L_{q_0,a}\overline{b} L_{q_1,b} \overline{cq_3}dR_{q_i,\lhd}\lhd)=\rhd bq_3cd\lhd$

Now, the  transitions in $M$, we define our string rewriting system $R$ as follows.

| transitions in $M$ | rewrites in $R$ |
|--------------------|----------------|
| $q_iabRq_j$        | $q_ia\rightarrow_R L_{q_ia}\overline bq_j$      |
|                    | $\overline a\overline q_i\rightarrow_R L_{\overline aq_i}\overline bq_j$      |
| $q_i\beta bRq_j$   | $q_i\lhd\rightarrow_R L_{q_i\lhd}\overline b q_j\lhd$      |
|                    | $\rhd \overline q_i\rightarrow_R \rhd L_{\rhd\overline q_i}\overline bq_j$      |
| $q_iabLq_j$        | $q_ia\rightarrow_R \overline q_j b R_{q_ia}$      |
|                    | $\overline a\overline q_i\rightarrow_R \overline q_j b R_{\overline a\overline q_i}$      |
| $q_i\beta bLq_j$    |  $q_i\lhd\rightarrow_R \overline q_jbR_{q_i\lhd}\lhd$      |
|                    | $\rhd \overline q_i\rightarrow_R \rhd\overline q_j b R_{\rhd\overline q_i}$      |

Moreover, for each $z$, we have the following two additional (sets of) auxiliary rewrite rules
\begin{align*}
q_iR_z&\rightarrow_R L_zL_zq_i\\
L_z\overline q_i&\rightarrow_R \overline q_iR_zR_z
\end{align*}
for any $z$.

To explain what these two rules do, let us define two types of strings. Type-A strings are strings where the symbol being scanned
 is to the immediate right of $q_i$ or to the immediate left of $\overline {q_i}$. 
In other words, 
 we call a string $s$ a type-A string if $s$ contains $q_ia$ or $\overline{aq_i}$.
Type-B strings are strings that are not type-A: 
 they are strings where there are dummy symbols in between the state and 
 the symbol being scanned.
The rewrite rules above convert any type-B strings into type-A in a finite number of steps.

Now, we observe that $R$ has several properties:

1. Reverse convergence: the critical pair lemma implies that
   if a rewriting system is terminating and all its critical pairs are convergent,
   it is convergent.
   Define $\leftarrow_R=\left(\rightarrow_R\right)^{-1}$.
   $\leftarrow_R$ is terminating since rewrite rules in $\leftarrow_R$
   decreases the sizes of terms (that is, rewrite rules in $\rightarrow_R$ increases the sizes of terms), and $\leftarrow_R$ has no critical pairs.
   Therefore, $\leftarrow_R$ is convergent.
2. For each type-A string $w$, then either
   * there exists no $w'$ with $w\rightarrow_R w'$ and $\pi(w)$ is a halting configuration;
   * there exists a unique $w'$ such that $w\rightarrow_R w'$ and $\pi(w)\vdash \pi(w')$.
3. For each type-B string $w$, there exists a unique $w'$ such that $w\rightarrow_R w'$,
   and $\pi(w)=\pi(w')$.
   Moreover, 
   if $w_0\rightarrow_R w_1\rightarrow_R\ldots$ is a sequence of type-B strings,
   the sequence must be bounded in length,
   since the state symbols $q_i$ and $\overline q_i$ move towards one end according to the auxillary rules above.
4. By 2 and 3, $w\rightarrow_R w_1$ and $w\rightarrow_R w_2$ implies $w_1=w_2$. In other words, $\rightarrow_R$ is a function.

These observations allows us to prove the following lemma

**Lemma 2.** Let $w_0=\rhd q_0s\lhd$ be an initial configuration.
$w_0$ is obviously in *CONFIG*. 
Moreover, given a Turing machine $M$, construct a string rewriting system $R$ as above.
$M$ halts on $w_0$ if and only if $[w_0]_R$, the equivalence class of $w_0$ in $R$, is finite.


**Proof.**
Consider
 $S: w_0\rightarrow_R w_1\rightarrow_R \ldots$,
 a sequence of *CONFIG* starting with $w_0$.
By the above observations,
 $S$ must have a subsequence of type-A strings
 $w_0\rightarrow_R^* w_{a_1}\rightarrow_R^* w_{a_2}\rightarrow_R^*\ldots$ with 
 $$\pi(w_0)=\ldots =\pi(w_{a_1-1})\vdash \pi(w_{a_1})=\ldots=\pi(w_{a_2-1})\vdash \pi(w_{a_2})= \ldots.$$
 <!-- IS THIS TRUE? -->
 <!-- Moreover, if the original sequence is bounded, the subsequence is bounded. -->

An overview of the trace $w_0,w_{a_1},w_{a_2},\ldots$ and its properties is shown below:

|        |                     |                |                                                                             |                |                         |                                                                                   |                |                         |          |
|:-:|:-:|:-:|:------------:|:-:|:-:|:---------------:|:-:|:-:|:-:|
|   Rw   |    ${w_0}$   | $\rightarrow_R$ | $\underbrace{w_1\rightarrow_R\ldots \rightarrow_R w_{a_1-1}}_{\text{finite}}$ | $\rightarrow_R$ |    ${w_{a_1}}$   | $\underbrace{w_{a_1+1}\rightarrow_R\ldots \rightarrow_R w_{a_2-1}}_{\text{finite}}$ | $\rightarrow_R$ |    ${w_{a_2}}$   | $\ldots$ |
|  Type  |          A          |                |                                 B $\ldots$ B                                |                |            A            |                                    B $\ldots$ B                                   |                |            A            |          |
| Config | ${\pi(w_0)}$ |       $=$      |                      $\pi(w_1)=\ldots =\pi(w_{a_1-1})$                      |    $\vdash_M$    | ${\pi(w_{a_1})}$ |                      $\pi(w_{a_1+1})=\ldots =\pi(w_{a_2-1})$                      |    $\vdash_M$    | ${\pi(w_{a_2})}$ | $\ldots$ |

Now we prove the claim:

* $\Leftarrow$:
  Suppose $[w_0]_R$ is finite.
  We show that there exists a *finite* sequence $S$ of $w_0\rightarrow_R w_1\rightarrow_R \ldots \rightarrow_R w_n$ such that
  there is no $w'$ such that $w_n\rightarrow_R w'$.
  If this is not the case, then an infinite rewriting sequence $w_0\rightarrow_R w_1\rightarrow\ldots$ must exist.
  Because $[w_0]_R$ is finite, for the sequence to be infinite, there must exist distinct $i,j$ such that $w_i=w_j$ in the sequence.
  However, this is impossible, because $\rightarrow_R$ always increases the sizes of terms.

  By our observation above, if there is no such $w'$ that $w_n\rightarrow_R w'$ in sequence $S$,
  it has to be the case that $w_n$ is type-A and $\pi(w)$ is a halting configuration.
  
  Now, take the subsequence of $S$ that contains every type-A string: $$w_0\rightarrow_R^* w_{a_1}\rightarrow_R^*\ldots \rightarrow_R^*w_{a_k}=w_n.$$
  We have $\pi(w_{a_i})\vdash\pi(w_{a_{i+1}})$ for all $i$ and $\pi(w_{a_k})$ is a halting configuration.
  This implies a finite trace of the Turing machine: $$w_0\vdash \pi(w_{a_1})\vdash\ldots\vdash \pi(w_{a_n}).$$
  Since we only consider deterministic Turing machines, the Turing machine halts on $w_0$.
* $\Rightarrow$:
  Suppose otherwise $M$ halts on $w_0$ and $[w_0]_R$ is infinite.

  By definition, $w_0$ is a normal form with respect to $\leftarrow_R$,
  and because $\leftarrow_R$ is convergent,
  if there exists a $w$ such that $w\approx_Rw_0$,
  then $w_0\rightarrow_R^* w$.
  The fact that $[w_0]_R$ is infinite implies $w_0$ can be rewritten
  to infinitely many strings $w$.
  Because $\rightarrow_R$ satisfies the functional dependency,
  it has to be the case that there exists an infinite rewriting sequence: $S:w_0\rightarrow_R w_1\rightarrow_R \ldots$.
  Taking the subsequence of $S$ consisting of every type-A strings: $$w_0\rightarrow_R^* w_{a_1}\rightarrow_R^* \ldots.$$ This implies an infinite trace of the Turing machine: $$w_0\vdash \pi(w_{a_1})\vdash\ldots,$$
  which is a contradiction.

We are ready to prove the undecidability of the termination problem of EqSat:

Given a Turing machine $M$. We construct the following two-tape Turing machine $M'$:

```
M' alternates between the following two steps:
1. Simulate one transition of M on its first tape.
2. Read the string on its second tape as a number, compute the next prime number, 
  and write it to the second tape.
M' halts when the simulation of M reaches an accepting state.
```
It is known that a two-tape Turing machine can be simulated using a standard Turing machine,
 so we assume $M'$ is a standard Turing machine and takes input string $(s_1,s_2)$, 
 where $s_1$ is the input on its first tape and $s_2$ is the input on its second tape.
Let $R'$ be the string rewriting system derived from $M'$ using the encoding we introduced in the lemma.

Given a string $s$,
 let $w$ be the initial configuration $\rhd q_0(s, 2)\lhd$.
The following conditions are equivalent to each other:

1. $M$ halts on input $s$.
2. $M'$ halts on input $(s, 2)$.
3. $[w]_{R'}$ is finite.
4. $[w]_{R'}$ is regular.

Note that (3) implies (4) trivially, and (4) implies (3) because if $[w]_{R'}$ is infinite, it must not be regular since the trace of $M'$ computes every prime number.

Now run EqSat with initial string $w$ and rewriting system $\leftrightarrow_{R'}$.
EqSat terminates if and only if $M$ halts on $s$:

* $\Rightarrow$:
  Suppose EqSat terminates with output E-graph $G$. 
  Strings equivalent to $w$ in $G$ is exactly 
   the equivalence class of $w$, i.e.,  $[w]_G=[w]_{R'}$.
  Moreover, 
   every e-class in an E-graph represents a regular language,
   so $[w]_G$ is regular.
  Therefore, $[w]_G$ is finite.
* $\Leftarrow$:
  Suppose $M$ halts on $s$.
  This implies $[w]_{R'}$ is finite.
  Because EqSat monotonically enlarges the set of represented terms, it has to stop in a finite number of iterations.

Because the halting problem of a Turing machine is undecidable, the termination problem of EqSat is undecidable as well. $\blacksquare$

**Theorem 3.** The following problem is undecidable.

    Instance: a set of rewrite rules R, a term w.
    Problem: Is [w]_R regular?

**Proof.**

To show the undecidability, 
 we reduce the halting problem of Turing machines to this problem.
As shown in Theorem 1, given a Turing machine $M$,
$M$ halts on an input $s$ if and only
 if $[w]_{R'}$ is regular for $w=\rhd q_0(s, 2)\lhd$.
$\blacksquare$

For a particular kind of rewrite systems, we show this regularity problem is R.E.-complete.
We call a term rewriting system left-linear if variables in the left-hand side of each rewrite rule occur only once.
For example, $R_1=\{f(x,y)\rightarrow g(x)\}$ is left-linear, while $R_2=\{f(x,x)\rightarrow g(x)\}$ is not left-linear.

**Theorem 4.** The following problem is R.E.-complete.

    Instance: a set of left-linear, convergent rewrite rules R, a term w.
    Problem: Is [w]_R regular?

**Proof.**

As we show in Theorem 1, the regularity of $\leftarrow_R$ is undecidable.
Note that $\leftarrow_R$, the inverse of $\rightarrow_R$ defined in Theorem 1, is convergent.
Moreover, because every string rewriting system is a linear term rewriting system 
 and therefore a left-linear term rewriting system, 
 $\leftarrow_R$ is left-linear.
Therefore,
 the regularity of left-linear, convergent term rewriting systems is undecidable.
Additionally, we show the regularity problem is in R.E. by showing a semi-decision procedure for it.

Let $\mathcal{A}_\ast$ be a tree automaton that accepts any term. 
More explicitly, $$\mathcal{A}_\ast=(q_\ast, \{f(q_\ast|_{i=1\ldots n})\rightarrow q_\ast\mid \text{for every }n\text{-ary symbol } f \})$$ for a fresh state $q_\ast$.


> **Procedure** $\textit{termsMatchingPattern}(p)$
> 
> **Input:** A linear pattern $p$.
>
> **Output:** An FTA $\mathcal{A}$ satisfying $\mathcal{L(A)}$
> contains all terms matching the given pattern.
>
> 1. **begin**
> 
> 2. $\quad$ $q_f\gets \textit{mkFreshState}()$;
>
> 3. $\quad$ **case** $p$ **of**
> 
> 4. $\quad$ $\quad$ $f(p_1,\ldots, p_k)\Rightarrow$
> 
> 5. $\quad$ $\quad$ $\quad$ $(q_i, \Delta_i) \gets \textit{termsMatchingPattern}(p_i)$ **for** $i=1,\ldots, k$;
> 
> 6. $\quad$ $\quad$ $\quad$ $q\gets \textit{mkFreshState}()$;
>
> 7. $\quad$ $\quad$ $\quad$ $\Delta \gets \{f(q_1,\ldots, q_k)\rightarrow q\}\cup \bigcup_{i=1,\ldots, k} \Delta_i$;
>
> 8. $\quad$ $\quad$ $\quad$ **return** $(q, \Delta)$;
> 
> 9. $\quad$ $\quad$ $x\Rightarrow$ **return** $A_\ast$;
> 
> 10. **end**

> **Procedure** $\textit{termsContainingPattern}(p)$
> 
> **Input:** A linear pattern $p$.
>
> **Output:** An FTA $\mathcal{A}$ satisfying $\mathcal{L(A)}$
> contains all terms containing the given pattern.
>
> **begin**
>
> 2. $\quad$ $q_f\gets \textit{mkFreshState}()$;
> 
> 3. $\quad$ $(q_p, \Delta)\gets \textit{termsMatchingPattern}(p)$;
>
> 4. $\quad$ $\Delta\gets \Delta\cup \{q_p\rightarrow q_f\}$;
> 
> 5. $\quad$ **for each** $n$-ary symbol $f$ **where** $n > 0$ **do**
> 
> 6. $\quad$ $\quad$ **for** $i = 1,\ldots,n$ **do**
> 
> 7. $\quad$ $\quad$ $\quad$ $\Delta \gets \Delta \cup \{ f(q_\ast|_{j=1,\ldots,i-1}, q_f, q_\ast|_{j=i+1,\ldots,n}) \rightarrow q_f \}$;
>
> 8. $\quad$ **return** $(q_f, \Delta)$;
> 
> **end**

> **Procedure** $\textit{Reg}$($R$, $w$)
>
> **Input:** a left-linear, convergent term rewriting system $R$, a term $w$.
>
> **Output:** an E-graph that represents $[w]_R$ if exists.
>
> 1. **for each** E-graph $G$ such that $w\in L(G)$ **do**
> 
> 2. $\quad$ **if** $G\neq \textit{runEqSatOneIter}(G, R)$ **then continue**;
>
> 3. $\quad$ $\mathcal{A}\gets \bigcup_{\textit{lhs}\rightarrow \textit{rhs}\;\in\; R} \textit{termsContainingPattern}(\textit{lhs})$;
>
> 4. $\quad$ **if** $\mathcal{L}(G)\cap\overline{\mathcal{L(A)}}=\{w\}$ **then** **return** $G$;
<!-- 
We enumerate E-graphs and for each  E-graph $G$,
 we check the following three conditions:

* $w\in L(G)$.
* $[w]_R \subseteq [w]_G$: to check this, we can check if $[w]_G$ is saturated with respect to $\leftrightarrow_R$.
* $[w]_G\subseteq [w]_R$: to check this, we can check if $[w]_G$ has only one normal form. -->



# References
