# Five pulse arrivals in a circular binary

**Decision.** A compatible record with nonzero symmetric curvature determines the inclination and the companion mass even when the phase-aligned lag is unknown. A calibrated lag also determines the emitter mass. With a free lag the emitter mass spans a whole interval bounded above by the supplied orbital-speed limit. For a face-on orbit even the companion mass is undetermined.

## Registered state and observations

Let $M=M_e+M_c$, with the emitter labelled and both masses strictly positive. The circular separation obeys $n^2a^3=GM$, where $n=2\pi/P>0$. The physical state retains these masses, the separation, inclination and phase. Phase advances by $n\Delta t$ between registrations. Starting with an empty record, each observation appends its predeclared phase and one signed clock residual, preserving all previous entries. In time order the phases are $0,\pi/6,\pi/2,7\pi/6,3\pi/2$, with sine labels $0,1/2,1,-1/2,-1$. The fifth reading occurs $3P/4$ after the first. The phase and emission ephemeris are supplied independently of these arrivals.

Put $s=\sin i$, $r=GM_c/c^3$, and $x=(a/c)(M_c/M)s$. With a common clock offset $B$ and stable lag $b$, the supplied map is
$$
 y_u=B+k u-2r\ln(1-su),\qquad k=x+b .
$$
Here $u,s$ are dimensionless, $B,b,r,x,k,y_u$ are seconds, $n$ has units of inverse seconds, and $a$ is a length. The constants $G,c$, the clock and the gravitational/inertial mass registration set the mass scale. The orientation branch gives $0\le s\le\sqrt{3}/2$. The relative orbital speed obeys $na/c\le\epsilon=1/100$.

The shape, GR range, Kepler mass function, orbital phase, Rømer delay and leading Shapiro delay come from the circular specialization of Freire and Wex, equations (3)–(7) and (9). We keep the full logarithm at this order. The five samples, extra stable lag, speed domain and inverse below are part of this packet. CL069 supplies circular barycentric geometry as a comparison and CL057 supplies a precedent for timing a common emission feature. Their velocity, flux and lens observations play no role in these residuals. This is an exact inverse of the declared propagation prescription. It supplies neither a full relativistic clock treatment nor an error bound for real data. [Freire and Wex, arXiv:1007.0933v1, 6 July 2010](https://arxiv.org/pdf/1007.0933v1)

## Timing consistency

Require all five prescribed, ordered phase labels and exactly one finite real residual in seconds per label. Reject wrong, repeated or missing labels, nonfinite entries, and any candidate outside the stated domain. Read $B=y_0$. For each $h\in\{1/2,1\}$ define
$$
 E_h=\frac{y_h+y_{-h}}2-B,\qquad
 D_h=\frac{y_h-y_{-h}}{2h}.
$$
The forward map gives
$$
 E_h=-r\ln(1-s^2h^2),\qquad
 D_h=k+\frac{r}{h}\ln\frac{1+sh}{1-sh}.
$$
For admissible $s,h$, $1\pm sh>0$ and $1-s^2h^2>0$. Only positive arguments of real logarithms are admitted. These four contrasts and $B$ retain every recorded value, since $y_{\pm h}=B+E_h\pm hD_h$.

**Nonzero even contrasts.** Require $E_{1/2},E_1>0$. With $z=s^2$, let
$$
 R(z)=\frac{F(z)}{H(z)}
      =\frac{-\ln(1-z)}{-\ln(1-z/4)}.
$$
The necessary and sufficient shape condition is
$$
 4<\frac{E_1}{E_{1/2}}\le \frac{\ln 4}{\ln(16/13)} .
$$
Indeed $F(0)=H(0)=0$, $H'(t)=1/(4-t)>0$ and $F'(t)/H'(t)=(4-t)/(1-t)$ has derivative $3/(1-t)^2>0$. Thus $R(z)$ is the $H'(t)$-weighted average of this strictly increasing derivative ratio on $[0,z]$. It is strictly less than the ratio at $z>0$, which gives $R'(z)=(H'(z)/H(z))(F'(z)/H'(z)-R(z))>0$. The average tends to 4 as $z\downarrow0$ and at $z=3/4$ it equals the displayed upper endpoint. Continuity and strict increase give exactly one $z\in(0,3/4]$ for each allowed ratio. The upper endpoint is $i=\pi/3$. The lower endpoint is unavailable for nonzero contrasts.

Use that unique root to set $s=\sqrt z,\ i=\arcsin s,\ r=E_{1/2}/H(z)>0$. Both even equations now hold. Enforce the two odd readings by computing, separately,
$$
 K_h=D_h-\frac{r}{h}\ln\frac{1+sh}{1-sh}.
$$
Accept this timing step exactly when $K_{1/2}=K_1$, and call their common value $k$. Equality is required even with an arbitrary $b$, since the same lag acts at both phase pairs. With it, the reconstructed timing parameters reproduce all five residuals by the contrast inversion above. Physical mass and lag consistency must still be tested below.

**Zero even contrasts.** Positivity of $r$ makes $E_h=0$ for either $h$ equivalent, within the model, to $s=0$. A record with exactly one zero even contrast or either contrast negative is incompatible. When both vanish require $D_{1/2}=D_1=k$. The record then has the pure first-harmonic form $y_u=B+ku$, including a constant as $k=0$. At $s=0$ one has $i=0,\ x=0,\ b=k$. For calibrated $b=0$ this requires a constant record. For free $b$ every real $k$ is possible. This branch uses neither a ratio of zeros nor an estimate of $r$ from curvature.

## Physical inverse and witnesses

Write $\beta=na/c,\ q=nr,\ M_{\max}=\epsilon^3 c^3/(Gn)$. Kepler's law yields $\beta^3=nGM/c^3$, while $q=nGM_c/c^3$. For a reconstructed $r>0$, strict emitter positivity and the inclusive speed bound give
$$
 q^{1/3}<\beta\le\epsilon,\qquad
 M_c=\frac{c^3 r}{G},\quad M=\frac{c^3\beta^3}{Gn},\quad
 M_e=M-M_c .
$$
As $a/c=\beta/n$ and $M_c/M=q/\beta^3$, the geometric amplitude is $x=rs/\beta^2$.

* **Calibrated $b=0$, $s>0$.** Require $k>0$, set $\beta=\sqrt{rs/k}$, and accept exactly when $q^{1/3}<\beta\le\epsilon$. Equivalently the allowed amplitude interval is $rs/\epsilon^2\le k<rs/q^{2/3}$. The upper amplitude endpoint would give zero emitter mass. At the lower endpoint the speed bound is attained if $q<\epsilon^3$. The displayed masses give the sole ordered pair. Set $a=c\beta/n,\ x=k,\ B=y_0,\ i=\arcsin s,\ b=0$. These assignments satisfy the orbital and propagation equations and the record.

* **Free $b$, $s>0$.** Accept exactly when $q<\epsilon^3$. The entire set is the fixed $M_c=c^3r/G$ paired with $0<M_e\le M_{\max}-M_c$. For each such emitter mass take $\beta=[nG(M_c+M_e)/c^3]^{1/3},\ a=c\beta/n,\ x=rs/\beta^2,\ b=k-x,\ i=\arcsin s,\ B=y_0$. This constructs the same measured $k$ for every pair. The domain prior supplies the upper bound, attained at $\beta=\epsilon$. Equality $q=\epsilon^3$ already consumes the entire mass allowance in the companion and is excluded. The timing readout itself adds no emitter-mass bound to strict positivity once $b$ is free. Equivalently, independently specifying a known lag would fix $x=k-b$, to which the calibrated amplitude test applies.

* **Either calibration, $s=0$.** After its timing test, the entire mass set is $M_e>0,\ M_c>0,\ M_e+M_c\le M_{\max}$. Every such pair gives $\beta=[nG(M_e+M_c)/c^3]^{1/3},\ a=c\beta/n,\ r=GM_c/c^3,\ x=0,\ i=0,\ B=y_0,\ b=k$. At these phase labels the logarithm is $\ln 1$, so each assignment reproduces the record. The total-mass bound is the entire mass information in this branch, and comes from the speed prior.

All other records have empty compatible sets. An admitted pair specifies a circular realization using the supplied phase origin and uniform rotation at $n$, with emitter orbital radius $aM_c/M$ and companion orbital radius $aM_e/M$ on the other side of the barycentre. Phase-independent orientation about the line of sight does not enter this observation.

## Exact matched example

Choose any $n>0$ and $r=10^{-9}/n$. Set $s=1/2,\ i=\pi/6,\ M_c=c^3r/G,\ M_e=7M_c,\ B=b=0$. Then $\beta^3=8\cdot10^{-9}$, $\beta=2\cdot10^{-3}<1/100$, $a=c\beta/n$, and $x=1/(8000n)$. In the prescribed order the five exact residuals are
$$
 \left(0,\ \frac{1}{16000n}-2r\ln(3/4),\
 \frac{1}{8000n}-2r\ln(1/2),\
 -\frac{1}{16000n}-2r\ln(5/4),\
 -\frac{1}{8000n}-2r\ln(3/2)\right).
$$
Their even contrasts are $E_{1/2}=r\ln(16/15)$ and $E_1=r\ln(4/3)$, fixing $z=1/4$. For $h=1/2,1$ the odd slopes are $x+2r\ln(5/3)$ and $x+r\ln 3$, respectively. The corrections therefore agree at $k=x$. Calibrating $b=0$ recovers $\beta=2\cdot10^{-3}$ and the stated masses.

In a second world keep $n,r,s,B,M_c$ fixed and choose $M'_e=63M_c$. Then $\beta'=4\cdot10^{-3}<1/100$, $a'=c\beta'/n$ and $x'=1/(32000n)$. The stable lag $b'=3/(32000n)$ makes $x'+b'=1/(8000n)$. Both the logarithmic term and the full linear coefficient agree at every prescribed phase, proving equality of the five exact records. This is a synthetic ambiguity between two positive-mass circular worlds at a common calibrated $n$. The register uses exact residuals and a supplied GR mass–time conversion. Its conclusions concern this finite circular model and its two specified calibrations.

## Scientific review

Classical supplied the circular timing inverse. A distinct Classical reviewer checked the proof, and DET Quantum Relativity independently assessed its use for gravitational and orbital mass inference. The coordinator accepted the conditional result on 9 November 2026 HST.

- Donor control SHA-256: `b112653fe4f224b51368d7130553627f67297961dbedaf80b8ec218c5d13648a`.
- Author report SHA-256: `e6809c618981a09c9ab4dcdfde77866c28b39f21249e09201b2e84b177602488`.
- Author freeze SHA-256: `d491957805a2a97fed2726c9c42fb6c729f48cab8a5619eb527c62ce079c01ca`.
- Independent scientific review SHA-256: `be67200a2e3c3d393b44c4146c1f7adbbd047209a13193d8611b9d759a473393`.
- Classical disposition SHA-256: `eda314b3f4e47aa587d84339df531238e399c5790e835fa4a871e41cf353951b`.
- QR recipient review SHA-256: `198648cd5b18606339b89f538a1ff3e388341aa216bd610c66c9aa3f887bb928`.
