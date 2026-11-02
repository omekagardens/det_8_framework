# Boost-defined inertia of the complete radiation-shell source

For the complete stationary radiation-plus-shell tensor specified below, a supplied Lorentz boost gives E′=γE and P′₁=γvE/c². Its small-velocity momentum coefficient is therefore M_in=E/c². The leading rest-frame active mass of this identical conserved source is also E/c² in the stated linearized gravitational approximation. The comparison retains the wall's energy and supporting stress. It is a conditional conventional result, not a DET-native mass law, an acceleration experiment or a material-realization claim.

## 1. One source and its accepted conservation identity

Use signature(−,+,+,+), x⁰=ct, and c,R,u,σ>0. Let V=4πR³/3, S=4πR², p=u/3 and n=x/R on the sphere. In the rest frame the contravariant tensor is

    ε=T⁰⁰=u 1_(r<R)+σc² δ(r−R),
    T⁰ⁱ=0,
    S_ij=Tⁱʲ=p δ_ij 1_(r<R)−τ(δ_ij−n_i n_j)δ(r−R),
    τ=uR/6,   E_r=uV,   E_w=σc²S,   E=E_r+E_w.

The radial delta is the surface measure convention ∫f(x)δ(r−R)d³x=∫_(S_R)f dS. The tensor is stationary and compactly supported. The [complete-source calculation](closed_radiation_shell_mass.md) proves distributional conservation at this tension. Its spatial stress integral is

    Σ_ij=∫S_ij d³x=(E_r/3)δ_ij−(2τS/3)δ_ij=0,

because ∫n_i n_j dS=(S/3)δ_ij and 2τS=E_r. The two local stresses remain nonzero. All wall energy is included; σ is independent of τ. No constitutive law, energy condition, stability assumption or external support is added.

## 2. Boost and simultaneous-slice definitions

Take the supplied active plus boost

    x′⁰=γ(x⁰+βx¹),   x′¹=γ(x¹+βx⁰),
    x′²=x²,   x′³=x³,   β=v/c,   γ=(1−β²)^(−1/2),

for each fixed finite |β|<1. Transform the complete spacetime tensor distribution with two Lorentz factors at the inverse argument. Define, rather than assume a transformation law for their totals,

    E′=∫_(x′⁰=0) T′⁰⁰ d³x′,
    P′_i=(1/c)∫_(x′⁰=0) T′⁰ⁱ d³x′.

Write y=(x′¹,x′²,x′³) on this slice. The inverse boost gives x⁰=−γβy¹ and x=Ay, with A=diag(γ,1,1). Thus the rest-time slice is tilted, x⁰=−βx¹. Stationarity permits evaluation of the same spatial source at every sampled rest time, and d³y=d³x/γ.

The shell requires the same change of measure. For every smooth compactly supported test function φ and rest shell density a(n),

    ∫φ(y)a(n(Ay))δ(|Ay|−R)d³y
      =(1/γ)∫_(S_R)φ(A⁻¹x)a(n(x))dS_x.

Equivalently, on the ellipsoid |Ay|=R the coarea weight is dS_y/|Aᵀn|, while dS_y=|Aᵀn|dS_x/γ. The gradient is nonzero for R>0 and finite γ. The normal in the density is the transported rest-sphere normal, not a substituted primed unit normal. The radial delta is not treated as an invariant spatial scalar or an unweighted ellipsoid surface measure. These statements evaluate the stationary slice of the already supplied tensor transformation.

## 3. Direct integrated tensor calculation

Since the rest mixed components vanish, multiplying the two boost factors gives

    T′⁰⁰(0,y)=γ²(ε+β²S_11)(Ay),
    T′⁰¹(0,y)=γ²β(ε+S_11)(Ay),
    T′⁰ᵃ(0,y)=γβS_1a(Ay),   a=2,3.

Apply the volume and surface measure factor1/γ to each component. A compact cutoff equal to1 near the source support justifies using the test-function identity for the total integrals. Before invoking conservation,

    E′=γ(E+β²Σ_11),
    P′₁=(γβ/c)(E+Σ_11),
    P′_a=(β/c)Σ_1a.

The complete Σ_ij=0 then proves

    E′=γE,   P′₁=γβE/c=γvE/c²,   P′₂=P′₃=0.

The prescribed plus boost makes P′₁ positive for positive v. At β=0 the rest energy and zero momentum are recovered. An integrated four-vector transformation was not assumed as a shortcut.

The component accounting is explicit:

| Contribution to this same source | Rest energy | Integrated S_11 | Boosted energy | Boosted longitudinal momentum |
| --- | ---: | ---: | ---: | ---: |
| Radiation | E_r | E_r/3 | γE_r(1+β²/3) | (γβ/c)(4E_r/3) |
| Supporting shell | E_w | −E_r/3 | γ(E_w−β²E_r/3) | (γβ/c)(E_w−E_r/3) |
| Complete source | E_r+E_w | 0 | γ(E_r+E_w) | (γβ/c)(E_r+E_w) |

These rows are contributions to one conserved tensor, not separate isolated systems with separately assigned component inertias. Individual shell contributions need not be positive without a material energy condition. Their complete sum has positive energy for the supplied parameters.

## 4. Inertia and the same-source active-mass comparison

Define the boost-momentum inertia coefficient by the two-sided limit

    M_in=lim_(v→0)P′₁/v=E/c²,

since P′₁/v=γE/c² for v≠0. The same formulas give the consistency expansions

    E′−E=Ev²/(2c²)+O(Ev⁴/c⁴),
    P′₁=Ev/c²+O(Ev³/c⁴).

This is the momentum-versus-boost definition, not a derived response to an applied force or an implemented acceleration protocol. It does not import the kinetic mass of a different model.

For the identical conserved rest source, the separate leading-field calculation uses supplied c,G, a static whole-space decaying solution, and matter held at zeroth order. Its asymptotic convention gives

    M_active=(1/c²)∫(T_00+Σ_iT_ii)d³x=E/c².

Consequently M_active/M_in=1 at that shared source/field approximation. The boost integrals are exact for every fixed finite |β|<1 within their flat-background model. This does not compute the moving gravitational field, prove uniform weak-field accuracy as γ becomes arbitrarily large, or include binding energy, source-equilibrium corrections and nonlinear gravity. A universal equivalence-principle claim does not follow.

## 5. Units, normalizations and a useful omission check

With q=σc²/(uR), M_star=uR³/c², and the same supplied weak-field parameters g=GuR²/c⁴≪1 and gq=GσR/c²≪1,

    M_in=4πuR³/(3c²)+4πσR²,
    M_in/M_star=M_active/M_star=4π(1/3+q),
    M_in c²/E=M_active c²/E=1.

Tensor components have energy/volume units. δ has inverse-length units, while σc² and τ have energy/area units. An integrated T′⁰ⁱ divided by c has momentum units; its coefficient relative to velocity has mass units. The dimensionless ratios survive consistent unit changes. They determine no numerical values of c,G,R,u,σ or a native DET unit.

Dropping the wall stress while retaining wall energy leaves Σ_11 incorrectly equal to E_r/3. The general boost formulas would then report E′_omit=γ(E+β²E_r/3), P′₁,omit=(γβ/c)(E+E_r/3), and the apparent coefficient(E+E_r/3)/c². That omitted tensor has boundary divergence−p n_jδ(r−R); it is not the conserved isolated source studied here. The excess is a completeness error, not a second admissible physical mass.

## 6. Scope and provenance

The same-source relation and shell/simultaneity calculation were independently reviewed and coordinator-adopted as E039, using the accepted GDM032 source. This public note assembles that exact result; it introduces no new source, law, experiment or scientific execution. Its active-mass premise is stated above and fully derived in the linked complete-source note, so the reader need not reconstruct chronological packets.

The result is a conventional target for any proposed native energy/source mapping: keep supporting stresses and the correct simultaneous slice with the energy being compared. Neither this calculation nor its companion supplies a DET-native stress tensor, stable excitation, mass spectrum, calibrated physical cavity, equation of state, material energy condition, preparation/work budget or empirical test. The [separate local boost theorem](conditional_boost_mass_relation.md) concerns another supplied model and is not a dependency of this inertia calculation.
