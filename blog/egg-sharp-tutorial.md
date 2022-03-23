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
A rule has the form `head1, ..., headn :- body1, ..., bodyn`.
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
 standard types like `string`, `i64`, and `u64` in Gogi are in fact 
 trivial lattices with $s_1\lor s_2 =\top$ for all $s_1\neq s_2$.
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
The `num` relation can be read as a function from `i64` to values in `expr`.
Similar declarations are ubiquitous in Gogi to represent sort constructors.

As another example,
```prolog
rel add(expr, expr) -> expr.
```
declares a relation with three columns, 
and the first two columns together 
uniquely determines the third column.
This represents a constructor that takes two `expr`s.

Moreover, users can introduce new sort values with functional dependencies.
Example:
```
num(1, c). % equivalently, num(1, _).
num(2, d).
add(c, d, e) :- num(1, c), num(2, d).
```

This program is interesting and 
 its semantics deviates from the one in standard Datalog.
In standard Datalog, this program will not compile 
 because variable `c` in the first rule, 
 `d` in the second rule,
 and `e` in the third rule are not bound.
However, this is a valid program in Gogi.
Thanks to functional dependency, 
 variables associated to head atoms do not necessarily 
 have to be bound in the bodies.
The above Gogi program is roughly equivalent to the following Datalog program:
```Prolog
num(1, c) :- !num(1, _), c = new_expr().
num(2, d) :- !num(2, _), d = new_expr().
add(c, d, e) :- num(1, c), num(2, d), !add(c, d, _), e = new_expr()
```
Negated atoms like `!num(1, _)` is necessary here 
 because otherwise it will inserts more than one atoms matching `num(1, _)`,
 which violates the functional dependency associated to the relation.

The example Gogi program can also be written into one single rule with multiple heads:
```Prolog
add(c, d, e), num(1, c), num(2, d).
% roughly equivalent to 
% add(c, d, e), num(1, c), num(2, d) :- !num(1, _), !num(2, _), 
%                                       c = new_expr(), d = new_expr(),
%                                       !add(c, d, _),
%                                       e = new_expr().
```

Gogi also supports the bracket syntax, so it can be further simplified to:

```Prolog
add[num[1], num[2]].
```

The bracket syntax will implicitly fill the omitted column(s) 
 with newly generated variable(s).
If the atom is in nested inside another term,
 the nested atom will be lifted to the top-level,
 and the generated variable(s) will take the original position of the atom.
Another silly example of the bracket syntax:

```Prolog
ans(x) :- xor[xor[x]].
% expands to
% ans(x) :- xor[y, z], xor(x, y, z)
% which expands to
% ans(x) :- xor(y, z, _), xor(x, y, z)
% this rule can be thought as
%   for any expr x, y where `y xor (x xor y)`
%   is present in the database, collect x as the result.
```

Finally, in equational reasoning a la egg, 
 it is common to write rules like 
 "for every `(a + b) + c`, 
 populate `a + (b + c)` on the right
 and make them equivalent".
This rule will look like the following in Gogi:
```prolog
add(a, add[b, c], id) :- add(add[a, b], c, id)
```

Gogi further has the `:=` syntactic sugar.

## Ext 3: Functional Dependency Repair