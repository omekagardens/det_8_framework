# A post-residual displacement register breaks a native diamond

The accepted GDM057 counterexample rejects one precise attachment to the finite native active-residual law: shifting a supplied position register according to the residual state after each birth. Two incomparable births give different joint-map coefficients even though their original native maps agree. This does not reject the native law or every possible coupling to a position-like register.

## Fixed question and source

Use the complete [active residual-to-structure law through four births](../track_b/native_active_residual_v1.md), with the original fair structural probabilities in [Part A of the marked-law specification](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix). Part B's changed-mark family is not used. For every actual ideal \(S\) and newborn bit \(b\),

\[
B^A_{C,S,b}=\frac{q_C(S)}2M(r_C(S)),\qquad
M(r)=\frac12\begin{pmatrix}1+r+t&1-r-t\\1+r-t&1-r+t\end{pmatrix},\quad t=1/2.
\]

The original native domain contains every binary-marked strict order through four births. Old marks and order are immutable; actual ideal occurrences and both newborn bits are retained. The fixed source coefficients are

\[
r_C(S)=\theta2^{|C|}\chi(C)
\left[a_{|C|+1}\mathbf1_{S=\varnothing}-a_{|C|}\right],
\quad\theta=1/32,
\]

where \(\chi(C)=1\) for an antichain and zero otherwise. The linked source fixes every \(a_n\); this witness uses only \(a_1=1/264\) and \(a_2=1/176\).

The proposed attachment supplies \(x\in\mathbb Z/11\mathbb Z\), residual basis index \(s\in\{0,1\}\), and increments \(\sigma(0)=+1\), \(\sigma(1)=-1\):

\[
\widetilde B^J_{C,S,b}(s',x'\mid s,x)
=B^J_{C,S,b}(s'\mid s)
\mathbf1\{x'=x+\sigma(s')\pmod {11}\}.
\]

Here \(J=A\) is the active source. The stipulated comparator is the source's forward-only \(B^F=qM(0)/2\); the counterexample below occurs for \(A\), so no later certification of the \(F\) lift is made.

The compatibility requirement is equality of full unnormalized maps on the entire 22-state nonnegative cone, including correlated inputs, across every required marked incomparable-birth diamond and transported suffix. Vertex relabeling acts trivially on \((s,x)\). The requirement is not merely agreement on a uniform preparation or after forgetting \(x\).

## An admitted diamond with equal native weights

Start with one vertex \(v\), marked zero, and its actual ideals \(S=\varnothing\), \(T=\{v\}\). Birth \(a\) over \(S\) and birth \(d\) over \(T\), each with newborn mark zero, are incomparable. Compare:

| Route | First birth | Intermediate parent | Second birth |
|---|---|---|---|
| Left | \(a\) over empty \(S\) | Antichain \(\{v,a\}\) | \(d\) over actual singleton \(\{v\}\), excluding \(a\) |
| Right | \(d\) over full \(T\) | Chain \(v<d\) | \(a\) over empty, excluding \(d\) |

Both routes end at the same marked three-vertex order: edge \(v<d\) and isolated \(a\). Endpoint transport matches these named vertices and their marks; natural birth labels swap for the two new vertices, while the residual and register coordinates stay fixed. The source explicitly permits this full-to-proper ideal transport. The terminal size is three, within its original domain; the empty suffix already requires equality.

The original Part-A rows give

\[
q_C(S)=2/3,\quad q_{C+a}(T)=1/10,\quad
q_C(T)=1/3,\quad q_{C+d}(S)=1/5.
\]

The value \(1/10\) is for one actual antichain singleton, not their sum. Including both fair newborn-bit factors, each two-birth scalar is

\[
\frac{(2/3)(1/10)}4=\frac{(1/3)(1/5)}4=\frac1{60}.
\]

Put \(\epsilon=1/8448\), an abbreviation for the inherited coefficient. The fixed rule yields, in the same route order,

\[
r_C(S)=\frac1{16}\left(\frac1{176}-\frac1{264}\right)=\epsilon,
\qquad r_{C+a}(T)=-\frac1{8\cdot176}=-6\epsilon,
\]
\[
r_C(T)=-\frac1{16\cdot264}=-2\epsilon,
\qquad r_{C+d}(S)=0.
\]

The last value vanishes because the intermediate parent is a chain. Thus the original native products are \(M(-6\epsilon)M(\epsilon)\) and \(M(0)M(-2\epsilon)\), with the common factor \(1/60\). Their equality is consistent with the accepted source: its triangular representation has two-step coefficient \(r_1+t r_2\), equal to \(-2\epsilon\) on both routes. The original native diamond is preserved.

## A joint-map entry that differs

Use basis input \((s,x)=(0,0)\) at the singleton prefix and inspect output \((s_2,x_2)=(0,2)\). This input belongs to the full-cone contract, independently of any later observation preparation. The final residual zero forces the second increment to be +1. Only intermediate residual \(s_1=0\) gives the other +1 and endpoint two; \(s_1=1\) would give endpoint zero. These endpoints are distinct modulo 11.

Since \(M(r)_{00}=3/4+r/2\), the chosen unnormalized entries are

\[
L=\frac1{60}\left(\frac34-3\epsilon\right)
                 \left(\frac34+\frac\epsilon2\right),
\qquad
R=\frac1{60}\frac34\left(\frac34-\epsilon\right).
\]

The first product inside the factor \(1/60\) expands to \(9/16-15\epsilon/8-3\epsilon^2/2\); the second is \(9/16-6\epsilon/8\). Therefore

\[
\boxed{L-R=-\frac{\epsilon(3+4\epsilon)}{160}<0,
\qquad\epsilon=1/8448.}
\]

This is an entry of a full linear map, not an observation postselected on success. The same transported marked endpoint and identical carrier coordinates are compared. A single unequal entry disproves the required universal joint-map identity.

The added register distinguishes intermediate residual routes that are summed together in the native product. Forgetting that register retains the original native behavior; it does not repair equality of the joint maps. No alternative carrier transport or coordinate identification is part of the fixed question.

## Decision and limits

Reject this exact post-state displacement attachment under the declared full-cone and trivial-carrier-transport requirements. The failed empty-suffix diamond is sufficient. In accordance with the admitted fail-first contract, no terminal observation law, one-birth control, two-birth distance, detector event, repaired shift, retuned source or successor is calculated. Remaining compatibility checks and the forward-only lift are not claimed certified.

The result constrains a proposed native-to-position-record ingredient. It establishes neither an impossibility over all couplings nor a physical position, particle, inertia, mass, native unit, clock, energy, metric, gravity or reciprocal feedback. The cyclic register and residual-to-increment assignment were supplied premises. Option B and Status M remain unchanged; the accepted native law and broader research programme remain open.

## Accepted content and permanent procedure qualification

The coordinator accepted the scientific counterexample while retaining the independent review's heading-only intake over-read. A diagnostic displayed six Part-B subsection titles outside the intended Part-A boundary. No Part-B prose, equations or changed-law reasoning entered the self-contained proof. Perfectly restricted intake is not certified, and publication does not cure that qualification or any earlier process failure.

Exact accepted versions, identified by SHA256:

- Author proof: `6631e16ff98d2ff8071ad138609ef46c66f48a8ef18a072b8ddbc5809ed4ed21`.
- Independent content review: `f0e0f9d978fc1d088be0b4f9bcd7ba8e27d3100835217a820622b775e65a6ade`.
- Coordinator disposition: `beae68bcc3597aaf4d9e14d678bc9993a613a0956f03aec6d01cd45403c668e6`.

These pins identify the accepted finite result and its qualifications; hashes alone do not establish mathematical validity. This note summarizes that result without adding a new scientific case.
