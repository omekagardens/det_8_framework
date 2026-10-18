# RI175 — intercept derivative and the retained quadratic-sign route

30 September 2026. Manual author derivation, submitted for independent
review. The unchanged-law intercept is strictly increasing on its full
formal interval, using an explicitly permitted, historically certified
quadratic-sign premise. The new calculus implication is not a fresh
evaluation of that sign or a proof from general DET axioms alone.

## 1. Exact derivative with the complete actual quadratic

Keep RI145/RI173's unchanged actual functions and positive constants:

    I(x)=-1+12lambda*[G_*x^2/q(x)+j_0*x/((1-x)v)],
    q(x)=q0+q1*x+q2*x^2>0,       0<x<=R<1/4,
    lambda>0,       G_*>0,       j_0>0,       v>0.       (1)

The q coefficients are aliases of the fixed canonical-corrected expression,
not free coefficients chosen for a counterexample. In particular, with
Delta=record1 minus record0, the complete identity is

    q(x)=(1-theta*x^2)v
       +(2-theta-2theta*x+theta^2*x^2)Delta h
       +(3-2theta-2x+theta*x^2)Delta j
       +(x-2)Delta N+2Delta(N*omega)
       -theta*x^2*Delta(N*omega^2),                     (2)

where N_i is the full RI151 canonical positive-part expression, not a
selected branch or independently tuned quantity. All three product
contrasts remain. The companion proof gives their complete coefficient
substitution and original source identities.

Ordinary differentiation, with the same q in both denominator and
derivative, gives

    I'(x)/(12lambda)
      =G_*x*[2q(x)-x*q'(x)]/q(x)^2
       +j_0/[v(1-x)^2]
      =G_*x*(2q0+q1*x)/q(x)^2+j_0/[v(1-x)^2].        (3)

The cancellation of q2 from the numerator is exact, not permission to
remove q2 from q or its same-law correlations. Likewise Delta(N*omega)
has zero derivative only because it is a constant term in x; it remains
in q and in 2q-xq'. No individual sign of a canonical contrast is inferred
from nonnegative N_i or omega_i.

If q'(x)<0 throughout the domain, positivity of q immediately gives

    2q(x)-x*q'(x)>2q(x)>0,
    I'(x)>12lambda*j_0/[v(1-x)^2]>0.                  (4)

Thus a decreasing positive q settles strict intercept monotonicity
without a separate magnitude comparison of its two derivative terms.

## 2. The accepted monic sign settles actual intercept monotonicity

The two already selected readable RI122 reviews state that the same
odd-record polynomial has the form

    Q2_1(x)=c*g(x),       c<0,
    g(x)=g0+g1*x+x^2.                                  (5)

The RI122 final decision explicitly accepts the separately checked signs

    g(1)>0,       g'(1)<0,       0<R<1.                (6)

The RI175 historical-premise scope expressly permits using this bounded
accepted result. RI127's accepted sign review, section 5, separately
links the same Q2_1 to a strictly negative multiple of g on the unchanged
baseline; RI145 fixes q=-Q2_1. Thus multiplication by k=-c>0 gives
q=k*g, not a substitute polynomial. This uses a stated derivative sign,
not an inference that root-freeness alone implies monotonicity. Since g
is monic quadratic,

    g'(x)=g'(1)-2(1-x)<g'(1)<0       for 0<=x<=R<1.   (7)

Accordingly q'(x)=k*g'(x)<0 throughout [0,R]. Since g decreases on
[0,1] and g(1)>0, also q0=k*g(0)>0. Equations (4)--(7) prove strict
monotonicity of the unchanged actual I on its entire formal interval.
No additional v/B regime is required for this derivative claim. The
separate RI173 y-slope theorem remains conditional. The comparison point
x=1 is not an admissible growth scale or a selectable actual value.

The readable historical reviews also report the native Sturm chain
g,g',a positive constant with endpoint signs (+,-,+). That stronger
description motivated the acceptance audit, but (6) alone supplies the
needed sign here. No inference about final acceptance of every native
Sturm field is needed for this derivative argument. The final decision
and current narrow reading permission, rather than a provisional review
alone, supply its historical authority. Neither calculation is rerun.

This is a finite retained-sign theorem, not a derivation of those signs
from general DET axioms, positivity alone, or an arbitrary canonical
positive-part pattern. In particular RI172's variable-coefficient family
does not inherit (5),(6) merely because it preserves size-four margins.

## 3. Lower-end degeneracies under the weaker positivity premise

The assignment asks that q0=0 not be silently excluded when deriving
general calculus implications from q(x)>0 only on (0,R]. The following
cases are therefore checked explicitly. They do not assert that any
degenerate case occurs in the actual law described by (5),(6).

By continuity q0>=0. If q0=0 and q1<0, then q(x)/x=q1+q2*x would be
negative for sufficiently small positive x, contradicting positivity.
Hence q1>=0. There are exactly two possibilities:

- q1>0: 2q0+q1*x=q1*x>0, so both terms of (3) are positive;
  x^2/q(x)=x/(q1+q2*x) tends to zero, and I(0+)=-1.
- q1=0: positivity forces q2>0. Then q=q2*x^2, the G_* term of I
  is constant, and I'(x)=12lambda*j_0/[v(1-x)^2]>0. Its lower limit
  is I(0+)=-1+12lambda*G_*/q2, not necessarily -1.

For q0>0, I(0+)=-1, independently of q1's sign. If q1>=0 then (3)
is strictly positive. More generally, 2q0+q1*R>=0 suffices: the affine
numerator is nonnegative over [0,R] whenever it decreases, and if it
increases its positive starting value suffices. A zero first term at an
endpoint cannot cancel the strictly positive j_0 term.

Another simple sufficient case is q2<=0, because

    2q0+q1*x=q(x)+q0-q2*x^2>0.                         (8)

These facts show exactly where generic positivity alone leaves a possible
derivative competition. It requires q0>0, q1<0 and 2q0+q1*R<0. On that
case put x_h=2q0/(-q1), so 0<x_h<R. The first derivative contribution
is nonnegative through x_h, and the full I' is strictly positive there.
Only the remaining tail can require additional magnitude information.
Under accepted (6), however, (4) proves that this adverse case cannot
describe the unchanged actual quadratic. These generic branches audit
the derivative without division by zero; they do not create an unresolved
actual branch after the fixed-prefix sign has been inherited.

## 4. Relation to the endpoint question

By (4)--(7), the supremum of actual-law I on 0<x<=R is I(R).
Thus a(x)<=0 for all x is equivalent to I(R)<=0,
since a(x)=q(x)(1-x)v*I(x) and the clearing factor is positive. In the
separately proved RI173 regime v<=T_R, b(x)<0 on the whole interval,
so this one intercept comparison then controls the full formal curved
domain. Strictly negative slope and excluded y=0 keep the distinction
between an attained upper x endpoint and a limiting y endpoint.

No value or sign of I(R) is calculated here. In particular, the fixed-law
intercept monotonicity does not establish actual membership in the
conditional slope region. Outside that region, the second y endpoint
remains a separate requirement. Nor does a statement over the formal
domain select rho,s or settle their actual weighted sign, individual
C2/C3 signs, the shared H30 conditions or continuation feasibility.

## 5. Literal evidence, classification caveat and diagnostics

The RI175 assignment and RI173 decision were authenticated and read
completely as `b97f42`,`03245c`,`35c4b8`, all exit 0. The complete
RI173 root proof review was read as `00ceef`. Fresh literal searches
and focused reads located the accepted quadratic-sign ancestry without
opening a scientific certificate or numerical report.

The precise historical readable sources are:

- `/Volumes/AI_DATA/development/det-review-evidence/ri122-saved-math-review-TlZje57F/INTERPRETATION.md`, 11087 bytes, SHA256 `d2fe0a49be13038d1855604bd935f1d4f284ddde124c9d8b6f67477d0deb493a`; complete read `d58fb0`. Section 1 identifies the negative multiplier and monic g; section 2 states both endpoint sign triples and separately explains the short derivative proof. Its original status is provisional, not silently relabeled final.
- `/Volumes/AI_DATA/development/det-review-evidence/ri122-audit-math-addendum-xkE4Xmwp/NONAUTHOR_AUDIT_REVIEW.md`, 13203 bytes, SHA256 `2df52eafb9ccb47ded7148660c3f530b395d9a5e6f4429985ff75f550b54ddd3`; complete read `d0154b`. The mathematical-reading section states the matching native reconstruction's same g,g' chain and (+,-,+) endpoint signs. That review recommended final acceptance after separately accepted custody.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-independent-proof-review-F2Esp0RB/INDEPENDENT_PROOF_REVIEW.md`, 20005 bytes, SHA256 `acbf782f2a331e130750a4a1dac4f7912406b72c4e3a246ffdabeb76da267774`; complete fresh read `885804`, byte/hash checks `26b5d6`,`c2d357`, all exit 0. Section 5 connects the same native Q2_1 to a negative multiple of g under accepted reconstruction and final adjudication; section 8 retains q(0)>0.

The full administrative final decision was also read as `af8563`:
`/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json`, 15477 bytes, SHA256 `162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc`.
Its stated proof accepts full reconstruction and the supplemental derivative
sign; no referenced scientific payload was opened. Fresh byte/hash checks
`113e0f`,`4ee33f` matched all three pins. The inherited manifest marks the
two reviews text-readable but classifies that administrative decision as
opaque historical support with no recursive reference expansion. The
literal administrative read preceded the scope clarification and was
disclosed to the parent, who requested an explicit root decision. It is
not concealed as an unchanged access classification or presented as
independent numerical validation.

The resulting bounded exception is
`/Volumes/AI_DATA/development/det-review-evidence/ri174-root-preparation-review-wm18ymsq/RI175_HISTORICAL_PREMISE_SCOPE.json`, 2159 bytes, SHA256 `bd1a9f4dd1cc2a10a194b620f9acda35d8fcca8750fc4fc767a54d4a9fd42ab4`.
It was authenticated as `fe3486`,`f3fb71` and read completely as `2f60e8`,
all exit 0. It explicitly permits literal historical use of (6), leaves
the inherited opaque classification intact, and forbids recursive
operational traversal, scientific decoding or expanded runtime authority.
It does not itself adjudicate this new derivative or endpoint theorem.

One guessed `INTERPRETATION.md` path under the root-execution directory
did not exist (`917325`, exit 2). The inherited manifest supplied the
correct existing path (`0d9e85`); no file was created by that failed read.
The predecessor q=-Q2_1 identity and same-law statements were crosschecked
as literal text in RI128 INPUT_FORMULAS, RI145 ENDPOINT_REDUCTION and
RI173 CANONICAL_SLOPE. No withdrawal was found in those selected texts;
this is not a claim to search every historical artifact.

Only this assigned external Markdown is authored. No scientific body,
vector, actual polynomial coefficient or scale was decoded or evaluated;
no helper/source import, compile, AST, probe, engine, fixture, runtime,
new agent, repository/index/Git operation or predecessor edit occurred.
Root owns premise-scope adjudication and independent review. RET stays
paused; RI170/RI171 and all P2/P3, Y=1/4, 31/139/20/42, shared T1,
other eight parents, five Di and strict multiplicities remain separate.
