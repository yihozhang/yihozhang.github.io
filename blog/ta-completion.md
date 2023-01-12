---
title: Ensuring the Termination of EqSat over Terminating Term Rewriting System
author: Yihong Zhang
toc: true
---

Term rewriting is one of the most fundamental techniques in programming languages. 
It is used to define program semantics, to optimize programs, and to check program equivalences.
An issue with using term rewriting to optimize program is that, it is usually not clear 
 which rule should be applied first, among all the possible rules.
Equality saturation (EqSat) is a variant of term rewriting that mitigates this so-called Phase-Ordering Problem.
In EqSat, all the rules are applied at the same time, 
 and the resulting program space is stored compactly in a data structure called E-graph.

EqSat has been shown to be very successful for program optimizations and program equivalence checking,
 even when the given set of rewrite rules are not terminating or even when the theory is not decidable in general.
However, despite its success in practice, there are no formal guarantees about EqSat:
 for example, when does EqSat terminate, and if it does not, how does one make it terminate.
The first problem is known in the term rewriting literature as the termination problem, 
 and the second is known as the completion problem.
Both problems are very hard, and there are a ton of literatures on both problems.
In the setting of EqSat, 
 these problems are not only theoretically interesting,
 both also have practical implications.
For example, in program optimization,
 we may want to get the most "optimized" term with regard to a given set of rules,
 so making sure EqSat terminate is important to such optimality guarantees.
In this post, we will focus on the termination problem of EqSat.
As it turns out,
 there are many interesting, and even surprising, results, about the termination problem with EqSat.

This post will show (1) how the innocent-looking associativity rule can cause non-termination,
 (2) why a terminating, and even canonical, term rewriting system does not necessarily terminate in EqSat,
 (3) how to fix the above problem by "weakening" EqSat's merge operation, 
 and (4) two potentially promising approaches to ensure the termination of EqSat.
One fascinating thing I found during this journey is that,
  researchers working on tree automata indeed developed a technique almost identical to EqSat,
  known as Tree Automata (TA) completion.
Different from EqSat, TA Completion does not suffer from problem in (2) and is exactly the algorithm we will show in (3).
Moreover, there is a beautiful connection between EqSat and TA completion.

# Term rewriting 101: Ground theories are decidable via congruence closure

Before understanding why associativity can cause non-termination,
 let us first briefly review some relevant backgrounds on ground theories and congruence closure.

A ground equational theory is an equational theory induced by a finite set of ground identities of the form $s\approx t$,
 where both $s$ and $t$ are ground terms (i.e., no variables).
For example, below is an example of a ground theory over signature $\Sigma={a,b,c,f,g}$:
\begin{align*}
  a&\approx f(b)\\
  b&\approx g(c)\\
  f(g(c))&\approx f(a)\\
\end{align*}
All the equations that can be implied by the three identities are true in this equational theory.
For example, we have $a\approx f(b)\approx f(g(c))\approx f(a)$. 
Here, $f(b)\approx f(g(c))$ holds 
 because we have $b\approx g(c)$.
In equational theory, 
 a function by definition maps equivalent inputs to equivalent outputs.

A classical result in term rewriting and logic is that
 the word problem of ground equational theory is decidable.
A (ground) word problem asks whether two ground terms $s$ and $t$ are equivalent in a given theory.
In general, this problem is undecidable.
However, if the theory is ground, 
 several algorithms exist that decide its word problem.
The most famous one is probably the $O(n \log n)$ congruence closure algorithm of Downey, Sethi, and Tarjan.
One way to view the congruence closure algorithm is that
 it produces a canonical term rewriting system 
 for each input set of ground identities:
For each input theory $E$, 
 it builds the corresponding E-graph,
 and every E-graph corresponds to a canonical term rewriting system.
For example, the congruence closure algorithm will produce the following e-graph for the theory above:
\begin{align*}
c_a&=\{a, f(c_a), f(c_b)\}\\
c_b&=\{b, g(c_c)\}\\
c_c&=\{c\}
\end{align*}
where $c_a, c_b, c_c$ denote E-classes of the E-graph, and $a,b,c,f(c_a), f(c_b), g(c_c)$ denote E-nodes.
This E-graph naturally gives the following canonical term rewriting system $R$, which rewrite terms to the e-classes they are in from bottom to top:
\begin{align*}
a&\rightarrow_R c_a\\
f(c_a)&\rightarrow_R c_a\\
f(c_b)&\rightarrow_R c_a\\
b&\rightarrow_R c_b\\
g(c_c)&\rightarrow_R c_b\\
c&\rightarrow_R c_c\\
\end{align*}
Now, checking $s\approx t$ 
 can be simply done by checking if there exists some normal form $u$ such that
 $s\rightarrow^*_R u \leftarrow^*_Rt$ holds. For example, $g(f(a))\approx g(f(g(c)))$ because
\begin{align*}
g(f(a))&\rightarrow_Rg(f(c_a))\\
&\rightarrow_Rg(c_a)\\
&\leftarrow_R g(f(c_b)) \\
&\leftarrow_Rg(f(g(c_c))\\
&\leftarrow_Rg(f(g(c))))
\end{align*}

This is sound and always terminates, because the term rewriting system produced by an E-graph is canonical--meaning every term will have exactly one normal form and term rewriting always terminates.

# Ground associative theory does not terminate in EqSat

Associativity is the fundamental law to many algebraic structures like semigroups, monoids, and groups.
It has the following form: 
$$x\cdot (y\cdot z)\approx (x\cdot y)\cdot z.$$
This rule can be oriented as $x\cdot (y\cdot z)\rightarrow (x\cdot y)\cdot z$
 (or $x\cdot (y\cdot z)\rightarrow (x\cdot y)\cdot z$).
This rule must be terminating, you may think, 
 so we can just apply the rule until saturation in EqSat,
 which will decide ground theories with associativity!
Unfortunately, ground associative theories are not decidable in general.
The book *Term Rewriting and All That* gives an example (we write $xy$ for $x\cdot y$ and $x\cdots x$ for $x^n$ for brevity and associativity allows us to drop brackets):
\begin{align*}
(xy)z&\approx x(yz)\\
aba^2b^2&\approx b^2a^2ba\\
a^2bab^2a&\approx b^2a^3ba\\
aba^3b^2&\approx ab^2aba^2\\
b^3a^2b^2a^2ba&\approx b^3a^2b^2a^4\\
a^4b^2a^2ba&\approx b^2a^4
\end{align*}
There is another way to state this proposition that appeals to math-minded persons: 
 the word problem for finitely presented semigroups are not decidable.

Because of this, associative rules do not terminate in EqSat in general.
To show this,
 suppose otherwise it is terminating, 
 given a set of ground identities $E$, we run the congruence closure algorithm over $E$ to get E-graph, and run both directions of the associativity.
When it reaches the fixed point and terminates, this gives us a way to decide ground associative theories, which is a contradiction to the fact that such theories are not decidable.

To better understand why associativity does not terminate in EqSat,
 here is an example:
 suppose $\cdot$ is associative and satisfy the ground identity 
 $(a\cdot b)\cdot b^{-1}\approx a$ for constants $a,b,b^{-1}$. 
Now suppose we orient the identity into rewrite rule $(a\cdot b)\cdot b^{-1}\rightarrow a$ while having the associative rule $(x\cdot y)\cdot z\rightarrow x\cdot(y\cdot z)$.
This is a terminating term-rewriting system (although not confluent,
 because the term $(a\cdot b)\cdot b^{-1}$ has two normal forms $a$
 and $a\cdot(b\cdot b^{-1})$).
