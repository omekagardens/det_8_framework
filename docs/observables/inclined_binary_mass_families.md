# Inclined binary mass families from two observed phases

The two tagged signed velocity channels determine the mass fraction when their orbital differences are nonzero, but normally leave the separation and inclination linked by one projected length. Registered same-band component photometry selects a unique mass pair except at exact photocentre cancellation. Even at cancellation, the supplied closed upper separation bound can force uniqueness. Face-on records never have a unique mass pair under these controls, with or without the registered light fraction.

This independently reviewed result uses a supplied exact Newtonian observation model. It does not use empirical binary data.

## 1. Supplied state, both balances and the six readings

Write B=4a0, n=2π/P, M=m1+m2 and q=m2/M, so 0<q<1. The orbit is supplied as

    r(t)=r2(t)−r1(t)=a(cos φ, cos i sin φ, sin i sin φ),   φ=nt,
    a0≤a≤B,   0≤i≤π/2,   0≤t≤P/2.

The mass barycentre is at rest at zero. Consequently r1=−q r and r2=(1−q)r. The norm of r is a at every time, and r̈=−n²r. The two reciprocal equations therefore require, separately,

    r̈1=q n²r = Gm2 r/a³,
    r̈2=−(1−q)n²r = −Gm1 r/a³.

Since both masses are positive, these equations are equivalent to

    M=n²a³/G,     (m1,m2)=(n²a³/G)(1−q,q).                 (1)

Conversely, (1) with any admitted a,q,i satisfies both body equations throughout the half-period. The mass barycentre is identically zero. The point bodies never collide because |r|=a≥a0>0. No finite component radii are specified, so this makes no separate assertion about finite-size contact.

Let f=F2/(F1+F2), with 0<f<1. The photocentre and radial velocities in the specified frame are

    X(t)=b+a(f−q)cos φ,
    V1(t)=δ1−n a q sin i cos φ,
    V2(t)=δ2+n a(1−q)sin i cos φ.                         (2)

The frame assumes that barycentric sky motion has already been independently measured and removed. At i=0, a physical line of nodes is undefined; the supplied diameter, sky x axis and phase registration still define (2). Face-on data do not authorize choosing a new phase to fit the observations.

For arbitrary finite real readings in their supplied channel and phase order, define

    b=(X_plus+X_minus)/2,
    δ1=(V1_plus+V1_minus)/2,   δ2=(V2_plus+V2_minus)/2,
    C=(X_plus−X_minus)/2,
    U=(V1_minus−V1_plus)/(2n),
    W=(V2_plus−V2_minus)/(2n).                            (3)

The offsets are uniquely these half-sums within this model, with no additional compatibility conditions on them. The informative equations are

    C=a(f−q),       U=a q sin i,       W=a(1−q)sin i.     (4)

In particular, the full six-reading forward map is

    (X_plus,X_minus,V1_plus,V1_minus,V2_plus,V2_minus)
      =(b+C,b−C,δ1−nU,δ1+nU,δ2+nW,δ2−nW).              (5)

## 2. Complete inverse with only the six readings

Every admitted record is in exactly one of the following branches. Negative U or W, or exactly one of U,W equal to zero, gives the empty mass set. There is no possibility of relabelling components, reversing phase order or changing a velocity sign to rescue such data under the frozen control. Two zero differences are consistent even if the raw velocities themselves are nonzero, because their stable offsets are unrestricted.

### 2.1 Both projected differences positive

For U>0 and W>0 put

    S=U+W,        q=U/S,
    A=max(a0,S),
    T=max(−C/q, C/(1−q)).                               (6)

Here S>0, 0<q<1 and T≥0; T=0 exactly when C=0. The necessary and sufficient feasibility test is

    S≤B    and    T<B.                                 (7)

Equivalently the second condition is −qB<C<(1−q)B. This includes all sign choices for C. When feasible, the complete parameter family is

    a ∈ I=[A,B] ∩ (T,∞),
    i=arcsin(S/a),      f=q+C/a,
    (m1,m2)=(n²a³/G)(1−q,q).                            (8)

The inclination is unique for each a because it is restricted to [0,π/2]. More explicitly,

    I=[A,B]   if T<A,
    I=(T,B]   if A≤T<B.                                (9)

These formulas follow directly from sin i=S/a≤1 and the strict positive-flux inequalities −qa<C<(1−q)a, which are equivalent to a>T. Necessity of (7) is immediate. For sufficiency, a=B satisfies both the inclination and flux conditions whenever (7) holds.

The mass set is a singleton exactly when S=B and T<B. In that case a=B, i=π/2 and q=U/B, with f=q+C/B. In every other feasible positive branch S<B, and I has positive length: both A and T are then strictly less than B. The mass set is a continuum because M=n²a³/G is strictly increasing with a. There are no other finite nonempty multiplicities.

The lower separation bound a=a0 is included exactly when S≤a0 and T<a0. Equality a=T is excluded because one component flux would be zero. Equality a=S is included and means edge-on inclination; the closed upper bound a=B is included whenever (7) holds. Equality T=B is infeasible, not a singleton. For a stationary photocentre C=0, f=q and T=0; the complete separation interval is [max(a0,S),B], with the same singleton rule S=B. Stationary light position does not imply a stationary binary.

### 2.2 Both projected differences zero: the face-on branch

For U=W=0, positivity of a and both masses forces sin i=0, hence i=0. Define, for each a,

    L(a)=max(0,−C/a),     H(a)=min(1,1−C/a).

The necessary and sufficient feasibility test is

    |C|<B.                                             (10)

The complete family is

    a ∈ [a0,B] ∩ (|C|,∞),
    L(a)<q<H(a),       i=0,       f=q+C/a,
    (m1,m2)=(n²a³/G)(1−q,q).                            (11)

Indeed, intersecting 0<q<1 with 0<q+C/a<1 gives exactly the displayed open q interval. It is nonempty exactly when |C|<a. Taking a=B proves sufficiency of (10). Every feasible face-on record admits a continuum of ordered mass pairs, already from the open q interval at a=B. Equality |C|=B is impossible because masses and fluxes are strictly positive; a=a0 is included only if |C|<a0. At C=0, any a∈[a0,B] and q=f∈(0,1) is admitted. The absence of radial differences leaves the mass ratio undetermined.

### 2.3 Reconstruction and exhaustiveness

For each parameter choice in (8) or (11), choose any finite total flux F>0 and set

    F1=(1−f)F,       F2=fF.

Use (1), the worldlines in section 1, and the unique offsets in (3). Both masses and component fluxes are positive; the separation and inclination satisfy their supplied bounds. The already verified two body equations hold at all times, and (4) reproduces (5), hence every raw reading. Conversely, every admissible world must obey the barycentric form, (1) and (4); these force exactly the branch conditions and parameters listed above. This proves sufficiency and completeness for the actual dynamics, not merely for projected products. The arbitrary light normalization F is the only additional light parameter and never changes a mass pair. No phase, barycentric motion or unobserved acceleration is fitted.

## 3. Add only an independently registered same-band light fraction

Let g=f_star be a finite independently registered fraction for tagged body 2 on the same orbit and in the same observation band. Its admissible range is 0<g<1. A proposed g outside that range, including the endpoints, is incompatible with the positive-flux preparation. The half-sum offsets remain those in (3), and the wrong-sign/one-zero branches remain empty.

### 3.1 Positive projected differences

For U,W>0 retain S=U+W and q=U/S, and define k=g−q. There are three exhaustive cases.

* If k≠0, define a_star=C/k. Compatibility holds exactly when

      a0≤a_star≤B   and   S≤a_star.                     (12)

  If compatible, the unique ordered mass pair is (n²a_star³/G)(1−q,q), with i=arcsin(S/a_star), a=a_star and f=g. Otherwise the mass set is empty. In particular C=0 is incompatible in this case, and nonzero C must have the same sign as k. All the equalities in (12) are closed and allowed. Positive flux follows from 0<g<1, so there is no extra open-flux test to add.

* If k=0 and C≠0, the record is incompatible: C=a(g−q)=0 would be required.

* If k=0 and C=0, compatibility holds exactly when S≤B. All solutions have

      a∈[max(a0,S),B],   i=arcsin(S/a),   f=g=q,
      (m1,m2)=(n²a³/G)(1−q,q).                         (13)

  This is a singleton exactly when S=B, and otherwise a continuum. At S=B, the inequalities S=a sin i≤a≤B force both a=B and sin i=1. The uniqueness comes from the supplied closed upper separation bound combined with the projected separation, even though the photocentre has cancelled and the light measurement supplies no new scale equation.

Equation C=a(g−q) proves necessity. Substitution into the reconstruction of section 2.3 proves sufficiency in every case and recovers positive fluxes, both worldlines and both individual force balances. No inferred mass ratio is equated with light except when the data and the independent fraction actually require it.

### 3.2 Face-on with registered light

For U=W=0, i=0 and q=g−C/a. Define

    T_g=max(C/g, −C/(1−g)).                            (14)

Compatibility holds exactly when

    T_g<B,    equivalently −(1−g)B<C<gB.                (15)

All solutions are

    a∈[a0,B] ∩ (T_g,∞),    q=g−C/a,    i=0,    f=g,
    (m1,m2)=(n²/G)a²((1−g)a+C, ga−C).                  (16)

This follows from 0<g−C/a<1; the strict boundary now excludes a zero mass. For every compatible record, max(a0,T_g)<B, so the admissible a interval has positive length. Total mass is strictly increasing with a, and the mass set is always a continuum. It cannot collapse to the upper endpoint: T_g=B would exclude that endpoint rather than admit it. At C=0 the fractions satisfy q=g, but every separation in [a0,B] remains possible. The same full worldline and flux reconstruction proves sufficiency.

### 3.3 Cardinalities summarized

| Data branch | Six readings alone | With registered 0<g<1 |
|---|---|---|
| Any wrong sign or exactly one zero among U,W | Empty | Empty |
| U,W>0 | Empty if (7) fails; singleton if S=B and T<B; otherwise continuum | For g≠q: singleton exactly when (12) holds, otherwise empty. For g=q: empty unless C=0 and S≤B; then singleton iff S=B, otherwise continuum |
| U=W=0 | Empty if &#124;C&#124;≥B; otherwise continuum | Empty if (15) fails; otherwise continuum |

This table concerns ordered mass pairs. An admitted unique pair still allows arbitrary positive total flux normalization, which is not a mass ambiguity.

## 4. Exact raw-data witnesses at the same fixed G, P and a0

Set M0=n²a0³/G. In all examples b=δ1=δ2=0. The following raw ordered tuples display sky readings in units a0 and velocities in units n a0; multiply back by those supplied scales to obtain the six physical readings. This notation does not replace any reading by an inferred ratio.

### 4.1 Distinct masses and inclinations with identical optional photometry

Take g=1/3 and the raw tuple

    (X_plus/a0,X_minus/a0,V1_plus/(na0),V1_minus/(na0),
       V2_plus/(na0),V2_minus/(na0))
      =(0,0,−1/3,1/3,2/3,−2/3).                       (17)

Two admitted worlds are

| a/a0 | i | q=f=g | (m1/M0,m2/M0) |
|---|---|---|---|
| 1 | π/2 | 1/3 | (2/3,1/3) |
| 2 | π/6 | 1/3 | (16/3,8/3) |

Both have a sin i=a0, U=a0/3, W=2a0/3 and C=0. Choosing total flux F=3 gives the identical positive flux pair (F1,F2)=(2,1) in relative light units for both worlds. Their masses and inclinations differ, but every raw entry of (17) and the same registered g agree. Their separation lies inside [a0,4a0]. The full construction in section 1 supplies the two worldlines and verifies both force balances, including for the second, more massive orbit.

### 4.2 A unique pair because photometry independently fixes scale

Change only the sky readings of (17) to (+1/3,−1/3) in units a0, and supply g=1/2. Thus C=a0/3, S=a0, q=1/3 and g−q=1/6. Equation (12) gives a_star=2a0, i=π/6 and the unique pair (16M0/3,8M0/3). Relative fluxes can be F1=F2=1. Without the registered g, these same six readings allow every a∈[a0,4a0], since T=a0/2; they do not identify the masses. The separate same-band light registration is precisely the additional premise that makes this example unique.

### 4.3 Cancellation can still be unique at the supplied upper bound

Take g=1/3 and the raw tuple

    (0,0,−4/3,4/3,8/3,−8/3).                          (18)

Here C=0, q=g=1/3 and S=4a0=B. The unique orbit has a=4a0, i=π/2 and masses (128M0/3,64M0/3); again choose relative fluxes (2,1). This pair is already unique from the six readings because S≤a≤4a0 forces equality. If the independently supplied upper separation bound were removed, every a≥4a0 with sin i=4a0/a and f=q would give the same readings and g. The uniqueness is therefore a consequence of that domain bound, not evidence that cancellation itself measures separation.



## 5. Supplied units, omitted information and scope

The natural supplied mass scale is

    M0=n²a0³/G=4π²a0³/(G P²).

With α=a/a0, every allowed pair is (m1/M0,m2/M0)=α³(1−q,q). Sky lengths, a0, C,U,W,S,T and T_g have units of length; n has units of inverse time; velocities and their offsets have units of length/time; G has units length³/(mass·time²). Angles, q,f,g, α, C/a0 and S/a0 are dimensionless. The component fluxes have only arbitrary relative normalization here.

The algebra can be stated entirely in these dimensionless quantities once the relative length, time and velocity calibration is supplied. A common change of units leaves the fractions, dimensionless normalized masses and inclination unchanged. In the positive branch the ratio q=U/(U+W) is a ratio of signed velocity differences and does not require an absolute mass standard. Absolute masses still require the supplied conversion M0. With physical length and time standards but no calibrated G, the dynamics identify gravitational parameters Gm rather than masses in an independent mass unit. If absolute length/time standards are also absent, one can retain the formal normalized family and any actually registered dimensionless ratios, but cannot assign a physical mass scale; without the required relative sky/velocity/time calibration, S/a0 and hence the inclination constraints cannot simply be recovered from uncalibrated numbers. None of this supplies a native DET mass unit or derives the shared inertial/gravitational mass assumption.

Known barycentric sky-motion removal and independent same-band light registration are controls, not conclusions of the six readings. For example, if an unremoved constant sky velocity w were present, the measured half-difference at times 0 and P/2 would instead be C−wP/4; an arbitrary b cannot remove that contribution. The two sky samples alone cannot distinguish it from orbital photocentre displacement. Separate stable radial offsets are accommodated by the half-sums, but additional radial drift or gain errors are outside the supplied model. An unregistered flux ratio, a different band, or loss of the component tag does not satisfy the optional control.

The earlier edge-on, single-tagged-velocity inverse supplies only the accepted circular Newtonian/photocentre comparison and is not asserted for this new observation model. The separately reviewed [five-pulse timing inverse](five_pulse_arrivals_and_binary_masses.md) uses a supplied relativistic propagation-delay law and additional phase samples, which are absent here. No outside or nested source theorem is needed for the algebra above. The registered inclined geometry, second velocity channel, exact standards, common gravitating/inertial masses and reciprocal force law are supplied assumptions; the new classification is their consequence. This is a conventional observation-sufficiency benchmark over one half-period, with no empirical binary data, finite-precision claim, ontology validation, native gravity derivation or extension beyond the frozen question.

## Scientific review

Classical derived the complete inverse; its distinct reviewer checked the signed readings, strict boundaries and both body equations. An independent recipient review confirmed the observation, calibration and native-mapping limits. Source SHA-256 7e60b34c9c4005a93f2358e794d4a399fe91a45a583d058fa5f3aae68463c754; scientific review e87878aaaaeb635a0cf1287494ef804137c15c19a9c1c0d040ad38e471c20eb2; recipient review 7fbf65bbe4a25356f055d3ce3d296ade2e5a2153ce88ce9973cf5a2579f25d35.
