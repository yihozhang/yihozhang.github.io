---
title: Ensuring the Termination of EqSat over Terminating Term Rewriting System
author: Yihong Zhang
toc: true
---

Term rewriting is one of the most fundamental techniques in programming languages. 
It is used to define program semantics, to optimize programs, and to check program equivalence.
An issue with using term rewriting to optimize program is that, it is usually not clear 
 which rule should be applied first, among all the possible rules.
Equality saturation (EqSat) is a variant of term rewriting that mitigates this so-called Phase-Ordering Problem.
In EqSat, all the rules are applied at the same time, 
 and the resulting program space is stored compactly in a data structure called E-graph.
EqSat has been shown to be very successful for program optimizations and program equivalence checking,
 even when the given set of rewrite rules are not terminating or even when the theory is not decidable in general.
However, despite the success in practice, there are no formal guarantees about EqSat:
 for example, when does EqSat terminate, and when it's not, how to make it terminate.
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
 there are many interesting, and even surprising, results, about the termination problem of EqSat.

In particular, this post will show (1) how the innocent-looking associativity rule can cause non-termination,
 (2) why a terminating, and even convergent, term rewriting system does not necessarily terminate in EqSat,
 (3) how to fix the above problem by "weakening" EqSat's merge operation, 
 and (4) two potentially promising approaches to ensure the termination of EqSat.
One fascinating thing I found during this journey is that,
  researchers working on tree automata indeed developed a technique almost identical to EqSat,
  known as Tree Automata (TA) completion.
Different from EqSat, TA Completion does not suffer from problem in (2) and is exactly the algorithm we will show in (3).
Moreover, there is a beautiful connection between EqSat and TA completion.

# Ground associative theory does not terminate in EqSat

Associativity is the fundamental law to many algebraic structures like semigroups, monoids, and groups.
It has the following form: $$x\cdot (y\cdot z)\approx (x\cdot y)\cdot z.$$
If written as an (oriented) rewrite rule, it will look like $x\cdot (y\cdot z)\rightarrow (x\cdot y)\cdot z$
 (or $x\cdot (y\cdot z)\rightarrow (x\cdot y)\cdot z$).
In term rewriting, this rule alone is terminating, and it just looks so innocent--what could go wrong if you just permute the order to compute the product?
After all, there are only finitely many ways to permute the order of computation.
This is true in EqSat: if the initial e-graph contains only one term and the rule set contains only associativity, 
 then EqSat will terminate and return the set of terms equivalent to the original term
 under associativity.
However, this is not the case.


 even if you just have one more ground equation, 
 e.g., $a\approx (a\cdot 2)\cdot ½$.





