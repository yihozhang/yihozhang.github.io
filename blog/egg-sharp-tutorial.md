---
title: A tutorial on the imaginary Gogi language
author: Yihong Zhang
---

Welcome to the tutorial on Gogi (short for eg**g**l**ogi**sh), a made-up language that attempts to generalize
 both [Datalog](https://en.wikipedia.org/wiki/Datalog) 
 and [egg](https://egraphs-good.github.io).
This is a [trick](https://github.com/nikomatsakis/plmw-2022) I learned from Nicholas Matsakis at PLMW 2022:
 To write a tutorial for a non-existing language.
By doing this, I can get a sense of what I want from this new language as well as early feedbacks from others.

Why Gogi? 
The motivation behind Gogi is to find a good model 
 for relational e-graphs that can take full advantage of 
 (1) performance of relational e-matching and 
 (2) expressiveness of Datalog, 
 while (3) being compatiable with egg as well as (4) efficient. 
This is the first approach I described 
 at the beginning of the previous [post](blog/ematch-trick.html). 
I'm actually more excited about this approach, 
 because I believe this is _the right way_ in long term.

Gogi is Datalog, so it supports various reasoning expressible in Datalog. 
A rule has the form `head1, ..., headn :- atom1, ..., atomn`.
For example, below is a valid egg# program:

```Prolog
rel link(string, string) from "./link.csv".
rel tc(string, string).

tc(a, b) :- link(a, b).
tc(a, b) :- link(a, c), tc(c, b).
```

However, Datalog by itself is not that interesting.
So for the first part of the post,
 I will instead focus on the extensions 
 that make Gogi interesting.
Next, I'll give some examples and show why Gogi generalizes egg
I will also try to develop the operational and model semantics of Gogi.
<!-- Finally, I'll discuss some thoughts on Gogi. -->


# Introduction to Gogi

## Ext 1: User-defined sorts and lattices

In Gogi, every value is either a (semi)lattice value or a sort value.
Lattices in Gogi are algebraic structures 
 with a binary join operator ($\lor$)
 that is associative, commutative, and idempotent
 and a default top $\top$ where $\top\lor e=\top$ for all $e$.
For example, 
 `string` in Gogi is in fact 
 a trivial lattice with $s_1\lor s_2 =\top$ for all $s_1\neq s_2$.
In Gogi, $\top$ means unresolvable errors.
Users can define their own lattices by
 providing a definition for lattice join.

Similarly, users can define sorts. 
Unlike lattices, sorts are uninterpreted.
As a result, sort values can only be created implicitly 
 via functional dependency.
We will go back to this point later.

## Ext 2: Relation declaration with Functional Dependencies

Relations can be declared using the `rel` keyword. 
Moreover, it is possible to specify a functional dependency 
 between columns in Gogi.
For example,
```prolog
sort expr.
rel num(i64) -> expr.
```
declares a sort called `expr`,
 a `num` relation with two columns `(i64, expr)`,
 and each `i64` uniquely determines the remaining column
 (i.e., `num(x, e1)` and `num(x, e2)` implies `e1 = e2`).

Similarly,
```prolog
rel add(expr, expr) -> expr.
```
declares a relation with three columns, 
and the first two columns together 
uniquely determines the third column.

Moreover, users can introduce new sort values with functional dependencies.
Example:
```
num(1, _).
num(2, _).
add(c, d, _) :- num(1, c), num(2, d).
```



## Ext 3: Functional Dependency Repair