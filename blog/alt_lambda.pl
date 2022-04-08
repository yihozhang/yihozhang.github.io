sort term.
rel false(term).
rel true(term).
rel num(i32, term).
rel var(string) -> term.
rel add(term, term) -> term.
rel eq(term, term) -> term.
rel lam(string, term) -> term.
rel let(string, term, term) -> term.
rel fix(term, term) -> term.
rel cond(term, term, term) -> term.

rel free(term, string).
rel const_num(term, i32).
rel const_bool(term, bool).
rel is_const(term).

% constant folding
const_num(c, i) :- num(i, c).
const_num[c] := const_num[a] + const_num[b] 
             if c = add[a, b].
const_bool(c, true) :- true(c).
const_bool(c, false) :- false(c).
const_bool(c, true), true(c) :- c = eq[a, a].
const_bool(c, false), false(c) 
              :- c = eq[a, b]
              if const_num[a] != const_num[b].
is_const(c) :- const_num[c].
is_const(c) :- const_bool[c].

% free variable analysis


% if-true
then := cond[true[], then, else].
% if-false
else := cond[false[], then, else].
% if-elim
else := cond[eq[var[x], e], then, else]
     if let[x, e, then] = let[x, e, else]
let[x, e, then] :- cond[eq[var[x], e], then, else]
let[x, e, else] :- cond[eq[var[x], e], then, else]
% add-comm
add[b, a] := add[a, b]
% add-assoc
add[a, add[b, c]] := add[add[a, b], c]
% eq-comm
eq[b, a] := eq[a, b]
% fix
let[v, fix[v, e], e] := fix[v, e]
% beta
let[v, e, body] := app[lam[v, body], e]
% let-app
app[let[v, e, a], let[v, e, b]] := let[v, e, app[a, b]]
% let-add
add[let[v, e, a], let[v, e, b]] := let[v, e, add[a, b]]
% let-eq
eq[let[v, e, a], let[v, e, b]] := let[v, e, eq[a, b]]
% let-const
c:= let[v, e, c] if is_const(c)
% let-if
cond[let[v, e, pred], let[v, e, then], let[v, e, else]] 
    := let[v, e, cond[pred, then, else]]
% let-var-same
e := let[v1, e, var[v1]]
% let-var-diff
var[v2] := let[v1, e, var[v2]] if v1 != v2
% let-lam-same
lam[v1, body] := let[v1, e, lam[v1, body]]
% let-lam-diff
lam[v2, let[v1, e, body]] := let[v1, e, lam[v2, body]] 
                          if v1 != v2, free(e, v2)
% capture-avoiding subst
lam[fresh, 
  let[v1, e, 
    let[v2, var[fresh], 
        body]]] 
  := 
let[v1, e, lam[v2, body]] 
  if v1 != v2, !free(e, v2), fresh = gensym().
free(c, v) :- free(body, v) 
           if c = lam[x, body],
              v != x.
free[c] := free[a]
           if c = let[x, a, b].
