# A fixed source channel fails a reversible Markov interpretation

This note records the accepted conditional GDM053 result. Four exact finite source channels fail a necessary stationarity condition for the specified reversible continuous-time Markov model. This is a counterexample to that compound interpretation, not a claim about every passive realization.

## Exact source and proposed interpretation

Use the [common source/order law, preparation and complete branch table](finite_source_order_return_and_visibility.md#one-common-law-with-retained-reference-information-gdm047). Retain each actual ideal, native bit, source state and reference state. The eight states, in order, are `(00,0),(00,1),(10,0),(10,1),(01,0),(01,1),(11,0),(11,1)`. Source vectors are `Q=(0,1,1,2)` and `r=(0,1,0,1)`.

The interpretation supplies these eight states as a complete set of equally degenerate microstates, even under time reversal, with energy

\[
E(i,n)=\Delta(Q_i+r_i),\quad\Delta>0,\quad\beta\Delta=\log2.
\]

It also supplies a positive duration \(\tau_*\). Thus

\[
Z=15/4,\qquad\gamma=(8,8,2,2,4,4,1,1)^T/30
=\rho_\gamma\otimes u,
\quad\rho_\gamma=(8,2,4,1)^T/15,\quad u=(1,1)^T/2.
\]

For each context and witness/cut choice, the question permits a separate time-homogeneous generator \(L\), with nonnegative off-diagonal entries, zero column sums, no cross-\(Q\) transitions, detailed balance \(L_{yx}\gamma_x=L_{xy}\gamma_y\), and \(\exp(\tau_*L)=G\). Energy, temperature and duration are shared supplied premises. No irreducibility or unique equilibrium across conserved sectors is assumed.

Detailed balance and column normalization imply

\[
(L\gamma)_y=\gamma_y\sum_xL_{xy}=0,
\qquad \exp(\tau_*L)\gamma=\gamma.
\]

A single failure of this necessary condition rules out the proposed generator for that channel.

## Four exact departures

Write

\[
M(x,t)=\tfrac12\begin{pmatrix}1+x+t&1-x-t\\1+x-t&1-x+t\end{pmatrix},
\quad M_0=M(0,1/2),\quad R_*=M(0,1/8).
\]

The branch law gives the following maps on the full eight-state space:

\[
G_a^w=G_a^{cut}=\operatorname{diag}(M(0,7/64),M_0\otimes R_*,M(0,7/64)),
\]
\[
G_c^w=\operatorname{diag}(M(0,1/8),M(0,19/32)\otimes R_*,M(0,1/8)),
\qquad G_c^{cut}=\operatorname{diag}(M(0,1/8),M_0\otimes R_*,M(0,1/8)).
\]

With \(v=(0,0,1,1,-1,-1,0,0)^T\),

\[
G_c^w\gamma-\gamma=13v/960,\qquad
G_a^w\gamma-\gamma=G_a^{cut}\gamma-\gamma=G_c^{cut}\gamma-\gamma=v/60.
\]

For an explicit check, the first output is `(256,256,77,77,115,115,32,32)/960`; each other output is `(16,16,5,5,7,7,2,2)/60`. The middle source block obeys
\(M(0,t)(2,4)^T/15=(3-t,3+t)^T/15\). This establishes every displayed departure, without a numerical approximation or an embeddability algorithm. All four proposed reversible realizations fail.

The input mean of \(r\) is \(1/5\). Its output is \(109/480\) for the chain witness and \(7/30\) for the other three maps: changes \(13/480\) and \(1/30\). Mean \(Q=8/15\) is preserved. Mean assigned energy changes from \(11\Delta/15\) to \(73\Delta/96\) or \(23\Delta/30\). These are energy-label bookkeeping consequences, not identified work or heat. The witness context contrast in \(r\) is \(-1/160\); the cut contrast is zero even though both cut channels fail stationarity.

## Full observation law and controls

For the third branch, the linked complete source table specifies

\[
B_{C,S,b}=\frac{p_C(S)}2\operatorname{diag}(R_0,H\otimes R_1,R_2).
\]

For antichain context \(a\), ideal probabilities are `3/8,1/8,1/8,3/8` for empty, the two distinct singletons, and full. For chain context \(c\), they are `1/4,3/8,3/8` for empty, root and full. Both native bits remain separate. Here \(H=M(0,h)\), with \(h=3/4\) only for the witness chain/full branch and \(h=1/2\) elsewhere, including all cut branches. Reference matrices \(R_i=M(x,t)\) are those of the linked source table; none may be replaced by an invented reset.

For this uniform-reference input, each reference matrix maps \(u\) to \(u\). Define

\[
\rho_h=(8,3-h,3+h,1)^T/15.
\]

Then \(B_{C,S,b}\gamma=(p_C(S)/2)\rho_h\otimes u\). With setting probability \(\lambda_s=1/2\) and each of the two preparation outcomes represented by \(I_8/2\), the complete terminal law is

\[
P(s,k,S,b,j,n)=\frac{p_C(S)}{16}\rho_h(j).
\]

It includes all 224 cells: 96 chain and 128 antichain cells, all positive on this input. Summing them gives one. For a microscopic refinement retaining input state \((i,m)\), the law is

\[
P(s,k,i,m,S,b,j,n)=\frac{\lambda_s}{2}
B_{C,S,b}[j,n;i,m]\gamma[i,m].
\]

This retains all exact cross-\(Q\) zeros; coarse positivity does not remove those zeros. Summing the refinement reproduces the terminal law. The record-only law is \(P(s,k,S,b)=\lambda_s p_C(S)/4\), so the witness and cut have identical such records within each context. This is not equality of chain and antichain record alphabets or full joint laws. The cut's aggregate source/reference coincidence on \(\gamma\) is specific to the uniform reference input; it is not a general operator equality across contexts.

## Interpretation and limits

The conclusion depends on completeness and equal intrinsic degeneracy of the eight microstates, the stated time reversal and energy assignment, and the precise reversible time-homogeneous Markov hypothesis. It does not exclude hidden-state, non-Markovian, driven or differently bounded realizations. It identifies no unique physical resource responsible for failure. The actual preparation, bath, clock, work store, detector, record-writing and reset costs remain unsupplied. Terminal access is a model premise; detector errors could erase the contrast.

No native energy unit, mass, gravity, empirical validation or universal passivity result follows. GDM047/GDM049 retain their own conditional scope. This finite interpretation test is closed; no thermal extension follows automatically.

## Provenance

Scientific source GDM053 report SHA256 `1f30fa30d075dd8d1a2a974ac08d2061e58bbf3df692d5e10327828d779ad2e5`; independent review `d9bfb8514aeeaea27c13fc0c1e1920fe01002822d5515836d64ab655fd762f12`; coordinator disposition `3507979c3c5c7e4fd1715e065570559fa0ebea9078897265cf0fbf29ddb8ec1d`. These identities establish which accepted finite result is summarized. The earlier E37 publication-author attempt ended incomplete without an artifact. This new assembly does not retrospectively qualify that attempt.
