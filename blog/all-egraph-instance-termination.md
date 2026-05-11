In my paper Semantic Foundations of Equality Saturation, I left an open problem: what is the complexity upper bound of all-egraph-instance-termination.

In that paper, I only proved that its lower bound is undecidable, which is a fairly trivial result. But I have long wanted to know what its precise upper bound is — whether it is RE, or whether the problem is Π₂-complete.

Recently I got a Claude Max subscription, and I found that I really cannot use up all those tokens, so I started throwing at it some problems I have been thinking about over the years (among other things to burn through Claude Max tokens). One of these problems was exactly this question: what is the complexity upper bound.

Claude tried for a while, and it did not solve the problem, but it pointed me to a new paper published at PODS 2025 about the termination complexity of different Chases. I had previously seen "Anatomy of the Chase," but that paper had some minor errors, so I had not read it carefully, and therefore I was not sure what the precise complexity was.

But I saw in this 2025 paper that it mentions that the earlier paper proved that the All Instance Termination of Core Chase is Π₂-complete. And we know that Equality Saturation is essentially a Core Chase, because:
1. Each of its steps is deterministic.
2. Each of its steps computes a Core. Although the specific method for computing the Core is different (Equality Saturation uses rebuilding).

But this gave me hope: since we can prove that Core Chase is Π₂-complete, can we use a similar proof technique to prove the same for Equality Saturation? So I told Claude about this idea. Claude thought for a while and proposed an approach (I did not read the Anatomy paper carefully, so I am not sure whether this is the proof approach from that paper), but it was missing a step.

First, Claude proposed that we can split e-graphs into Cyclic and Acyclic e-graphs and handle them separately:

1. For Acyclic e-graphs
   We know it represents finitely many elements, so we can think of it as a set of finitely many elements.

2. For the Cyclic case
   Claude ran into some difficulty. It asked me whether there exists a technique that, if an e-graph is Cyclic, can make it saturate quickly (or, equivalently, flood).

For this flooding problem, I thought about it briefly and realized it is actually quite simple.

So I told Claude my idea, and Claude said: "You are absolutely right."

Then it ran into another small problem, which I also solved. And with that, we solved this problem that had been on my mind for a long time.

I will replicate my proof below.

I believe that the proof of this theorem could not have been completed by Claude alone or by me alone:

1. If by Claude alone
   Based on my conversations with Claude, I found that it has not really internalized equality saturation well, so much of its language is vague and imprecise, and it sometimes produces seemingly-right answers. It is often hard to take its response seriously^[My experience so far is ChatGPT (where I'm on the free plan) is much better mathematical reasoning than Claude].

2. As for me personally
   On the other hand, without Claude, I might not have thought along the lines of distinguishing the acyclic and cyclic cases.

So from this perspective, the two of us are equally important. We humans have not lost yet.


## The proof

The proof of the complexity of the all-term-instance termination relies on the following tweak of the result from Narendran et al.

> For any Turing machine $M$, there exists a signature $\Sigma$ and a string rewriting system $R_M$ over $\Sigma$ such the Turing machine $M$ halts on all inputs if and only if $\forall t\in \mathcal{T}_{\Sigma}. [t]_{R_M}$ is finite. Moreover, if $M$ does not halt on $t$, then $[t]_{R_M}$ is not regular.

For all-instance termination, we can just throw the rewriting system $\leftrightarrow_{R_M}$ to EqSat, which computes exactly the congruence closure $[t]_{R_M}$ for any input term $t$. EqSat terminates if and only if $[t]_{R_M}$ is finite, thanks to the finite convergence lemma in the paper. Accordingly, $M$ terminates on all all inputs iff $\forall t. [t]_{R_M}$ is finite iff EqSat terminates for all $t$.

Unfortunately, this does not work for all e-graph instance termination, because there could be weird e-graphs with weird equalities between terms. It is hard for me to imagine how these arbitrary equalities an e-graph could introduce can potentially affect the rewriting process. This is where I got stuck.

To make it work, we split input e-graphs into two categories: acyclic e-graphs and cyclic e-graphs. An e-graph is cyclic it represents an equality $s\approx t$ where $s$ is a proper subterm of $t$^[When we talk about the termination problems, we assume the e-graph is finite in size, even though the paper explicitly allow e-graph with infinite number of e-classes/e-nodes.].

If an e-graph $G$ is acyclic, it represents a partial congruence relation $\approx_G$ that (1) has a finite number of equivalence classes and (2) each equivalence class is finite.
$\textit{EqSat}(R_M, G)$ computes a partial congruence relation $\approx_G \lor \approx_{R_M}$ (i.e., the least PCR that's greater than $\approx_G$ and $\approx_{R_M}$).
Moreover, we can prove that, if all equivalence class of $\approx_{R_M}$ is finite, then all equivalence class of $\approx_G \lor \approx_{R_M}$ is also finite.

To handle the cyclic case, our plan is to introduce a set of rules, so that the EqSat will always terminate whenever a cycle is detected in the E-graph.

Our first gadget is a term $\textit{cycle\_detected}$ that, once populated in the E-graph, flood the E-graph to saturate. If has the following rules for each n-ary symbol $f$
$\textit{cycle\_detected}\rightarrow f(\textit{cycle\_detected}, \ldots, \textit{cycle\_detected})$. This will collapse the whole e-graph into a single E-class.

Our second gadget is cycle detection. We add new binary symbols $T$, $E$, $\land$ and nullary symbol $g$ to $\Sigma$, and add the following rules

$$f(\ldots, x_i, \ldots)\rightarrow T(f(\ldots, x_i, \ldots), E(x_i, f(\ldots, x_i, \ldots)))$$

for every non-$T,E,\land,H,g$ symbol $f$ and every position $i$ of $f$.
Then we add the following rule for transitive closure reasoning.

$$E(x, y)\rightarrow g$$
$$g\rightarrow \land(g, g)$$
$$\land(E(x, y), E(y, z))\rightarrow E(x, z)$$
$$E(x, x)\rightarrow \textit{cycle\_detected}$$

The $T$ symbol is used to prevent the congruence over $E$ from merging every term.

With our construction, the equality saturation will always saturate and collapse to a single E-class if it detects a cycle any point during the evaluation.

### Putting it together

I claim that given a Turing machine $M$, letting the term rewriting system $R'_M$ be $R_M$ unioned with our cycle detection rules over $\Sigma' = \Sigma\cup \{\textit{cycle\_detected}, T,E,\land,H,g\}$, EqSat terminates for all E-graphs $G$ over $R'_M$ if and only if $M$ halts on all inputs.

* $\Rightarrow$. Suppose $M$ does not halt on input $w$. By Narendran et al's construction $[w]_{R_M}$ is not regular. Therefore, EqSat must not terminate on $w$ and $R_M$. Additionally, we will show the execution of EqSat on $w$ and $R_M$ must not introduce cycles, so the cycle detection rule won't be fired. Thus EqSat does not terminate on $R'_M$ and $w$. A contradiction.

  Suppose otherwise EqSat introduces a cycle on $w$ and $R_M$. We have $s\approx ts$ for some strings $s$ and $t$.^[Recall we encode strings `xyz` as chains of unary functions $x(y(z(\epsilon)))$, so a cycle means some string is equal to its proper suffix.] Because $w\in \textit{CONFIG}$, $w$ has a unique infinite rewriting sequence $w\rightarrow w_1\rightarrow w_2\rightarrow \ldots$ (Observation 4 on page 26 of the semantic paper). $s$ and $ts$ must be suffixes of $w_i$ and $w_j$ for $i\leq j$.
* $\Leftarrow$. If $M$ halts on all inputs, $[w]_{R_M}$ is finite for all $w$.