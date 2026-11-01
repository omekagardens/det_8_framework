# GDM007: restoring support and a finite prepared-pair response

This is a conditional theorem in a supplied canonical two-body model. It
does not derive that model from DET or identify its response with physical
inertial or rest mass. The current disposition and review are recorded in
`ADOPTION.md` and `REVIEW.md` in this directory.

## Exact premises and observable

Let `e,c,ell > 0`, `d=4ell`, `k=e/ell^2`,
`q=X2-X1-d`, and `R=(X1+X2)/2`. For `chi` equal to zero or one, use all
canonical Hamilton equations for

```
K(P) = sqrt(e^2+c^2 P^2),
H_chi = K(P1)+K(P2)+chi k q^2/2.
```

The entire pair and potential are the system boundary. There is no external
force after preparation. The link is selected at `q=0` before the kicks and
is never switched during a run. Its energy zero is fixed there. Time,
canonical coordinates, fixed component energies, instantaneous interaction,
constituent tracking and ideal impulse/readout access are supplied premises.

Prepare `X1=-d/2`, `X2=d/2`, initially at rest. Apply the same relative
disturbance `(-p_star,+p_star)`, with `p_star=e/(10c)`, then a total impulse
`zeta I`, split equally, where `I=e/(10c)` and `zeta` is plus or minus one.
Thus `P1=-p_star+zeta I/2`, `P2=p_star+zeta I/2`. There are exactly four
trajectories, crossing `chi` and `zeta`.

Organization means a unique uninterrupted trajectory with finite momenta,
positive fixed `e`, and `|q(t)|<ell` at every time through `T=10ell/c`.
Equality or exit is failure. Check the same criterion during
`h=ell/(4c)`. These are fixed finite diagnostics, not asymptotic stability
or matter formation.

The sole response observable is

```
V_chi^zeta = [R_chi^zeta(h)-R_chi^zeta(0)]/h,
M_resp,chi = 2I/(V_chi^+ - V_chi^-),
```

provided the denominator is finite and positive. It has mass units but is
not defined to equal `H/c^2`, `2e/c^2`, or a physical mass.

## Claim

Both linked runs pass organization through `T`. Both unlinked runs pass
through `h` and fail before `T`. Both response coefficients exist, and

```
e sqrt(401)/(10c^2) < M_resp,1 < M_resp,0
M_resp,0 = e/{5c^2 [3/sqrt(409)-1/sqrt(401)]}.
```

All four preparations have the same total Hamiltonian energy. This proves
a conditional support/response connection, but not a comparison of two
continuing composites through `T`.

## Complete reduction and continuation

Use `tau=ct/ell`, `y=q/ell`, `r=R/ell`,
`a=c(P1+P2)/(2e)`, `b=c(P2-P1)/(2e)`, and

```
f(u) = u/sqrt(1+u^2),
A(a,b) = sqrt(1+(a-b)^2)+sqrt(1+(a+b)^2),
F_a(b) = f(a+b)-f(a-b),
W_a(b) = [f(a+b)+f(a-b)]/2.
```

The full equations, with primes denoting `d/dtau`, are

```
a'=0,  y'=F_a(b),  b'=-chi y,  r'=W_a(b),
H_chi/e = A(a,b)+chi y^2/2.
```

Initially `y=r=0`, `b=1/10`, `a=zeta/20`. Total momentum is exactly
`zeta I` and conserved. `A,F` are even in `a`, while `W` is odd. Uniqueness
therefore gives the same `y,b` and opposite `r` for the two signed runs.
It suffices to consider `a=1/20`.

The vector field is smooth. Each particle speed is less than `c`, bounding
positions and `q` on every finite interval. The linear forces then bound
momenta. Local existence and uniqueness extend without finite-time escape.
This is separate from passing the organization criterion.

## Work and organization

The energy after the relative kick is `e sqrt(101)/5`; after either signed
kick it is

```
E_star = e [sqrt(401)+sqrt(409)]/20.
W_relative = e [sqrt(101)/5-2],
W_kick = E_star-e sqrt(101)/5,
W_total = E_star-2e.
```

Both increments are positive. For the second, `A(a,1/10)` is even and
strictly convex in `a`; the kick changes `|a|` from zero to `1/20`.
These exact work differences and total energies are the same in all four
runs. An excluded ideal apparatus supplies work and momentum. Zero
potential-energy jump at selection does not imply zero apparatus or
switching cost. An additive energy constant changes neither the forces,
response nor preparation-energy differences. Physical costs are unspecified.

For `chi=0`, `b=1/10` and

```
y(tau) = F0 tau,
F0 = 3/sqrt(409)+1/sqrt(401),
4/21 < F0 < 1/5.
```

Thus `y<1/20` through `tau=1/4`, but reaches the forbidden value one at
`tau_star=1/F0 < 21/4 < 10`. Both unlinked cases pass the readout and fail
the full organization window.

For `chi=1`, strict convexity minimizes `A(a,b)` at `b=0`. Conservation
therefore gives, at all finite times,

```
y^2/2 <= A(1/20,1/10)-A(1/20,0)
       = [sqrt(409)-sqrt(401)]/20 < 1/20.
```

Consequently `y^2<1/10<1`. Both linked cases pass through `T`, including
the readout. Necessity of the link is established only for this disturbance,
criterion and matched removal control; no damping or formation is proved.

## Finite displacement, with no instantaneous substitution

Define

```
barW_chi = 4 integral from 0 to 1/4 of W_(1/20)(b_chi(tau)) d tau.
```

Signed symmetry gives `V_chi^+=c barW_chi` and
`V_chi^-=-c barW_chi`, hence `M_resp,chi=e/(10c^2 barW_chi)`.
For the unlinked case,

```
barW_0 = [3/sqrt(409)-1/sqrt(401)]/2 > 0.
```

For the linked case, a first-exit argument gives `y>0` and
`0<b<1/10` on `0<tau<=1/4`. While in that interval,
`0<F_a(b)<=2b<=1/5`, since `0<f'(u)<=1`. Thus `y<=tau/5` and
`b>=1/10-tau^2/10>=3/32>0`, preventing a first zero before readout.
Positive `y` prevents return to the initial upper boundary. The initially
positive `F_a(1/10)` starts the argument.

For positive `a,b`,

```
dW_a/db = [f'(a+b)-f'(a-b)]/2 < 0,
f'(u) = (1+u^2)^(-3/2),
```

because `|a+b|>|a-b|`. Also `W_a(b)>0` by oddness and strict monotonicity
of `f`. Every positive readout time therefore satisfies

```
W_a(1/10) < W_a(b_1(tau)) < W_a(0) = 1/sqrt(401).
```

Integration proves `0<barW_0<barW_1<1/sqrt(401)` and the claimed strict
mass-unit response bounds. The integral with its stated initial-value
problem is an exact implicit value. No solver, series, infinitesimal
impulse, endpoint replacement or fitted rigid constraint is used.

## Interpretation and open physical premise

During readout the link reduces outward relative momentum and stores energy
in the quadratic potential. At fixed total momentum, the nonlinear kinetic
velocity relation increases the arithmetic center's positive-impulse mean
velocity. This lowers this particular response coefficient.

Equal `E_star` with unequal responses shows that total Hamiltonian energy
alone does not determine this observable across these preparations. It is
not a universal binding-energy law. The unlinked value describes prepared
constituents during `h`; that pair later fails organization. It is not the
mass of a continuing composite over `T`.

The arithmetic center is not a derived physical center of energy. A physical
interaction/field/stress energy-momentum and boost correspondence, together
with calibrated preparation/readout, remains missing. This theorem supplies
no physical inertial/rest-mass identification, native gravity, global quantum
reconstruction, ontological identity or empirical validation.
