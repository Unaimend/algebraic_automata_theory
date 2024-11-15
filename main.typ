











= Chapter 1

== 1.6 Exercises

=== 1.1

=== 1.3 Products
Semigroups can be combined to create more semi groups

==== Direct product of S and T

Let $S, T$ be semigroups. Consider the set $S times T$ with a multiplication defined as follows
#align[
  $(a,x) * (b,y) = (\a\b, \x\y)$
] where $a,b in S$ and $x,y in T$.
The result is a semigroup $(S times T, *)$.

===== Lema 1.3.

$(S times T) times W$ is isomorphic to $S times (T times W)$.

==== Semidirect Product
Let $S, T$ be a semigroup and $Theta: T arrow.r "End"(S)$ a semigroup homomorphism. Consider the set $S times T$ with a multiplication defined as follows
#align[
  $(s, t) ast.circle (s', t')= (s theta (t)(s'), t\t')$
] where $s,s' in S$, $t,t' in T$, $Theta (t): S arrow.r S$ and so $Theta (t) (s) in S$

Denoted by $S times_Theta T$. We have that $(S times T, times_Theta)$ is a semigroup.

==== Wreath product (TO BE CONTINUED)

Let $S^T$ denote the set of al functions from the monoid $T$ to the semigroup $S$.

We define a multiplication $circle.stroked.tiny$ on $S^T times T$ by $(f, t) circle.stroked.tiny (g', t') = (f circle.stroked.tiny g', t t')$

== Chapter 2: Machines and semigroups


