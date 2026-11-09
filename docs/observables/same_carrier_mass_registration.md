# Same-carrier mechanical verification identifies the proportionality decision under successful coverage

**Independently reviewed conditional result.** Unknown static mispreparation need not prevent an active/inertial proportionality decision. Under the supplied binding to the SAME actual whole carrier, a common first-lobe reference spring and positive successful verification coverage of every true sector, the complete augmented record gives a finite admissibility test. On admissible records proportionality is either true in every compatible world or false in every compatible world, including tied inertias and merged clock atoms. This does not certify sector identity inside an unobserved exact degeneracy or derive a physical registration apparatus.

If successful coverage is withdrawn only on the two native-history-indistinguishable sectors, two worlds can have the identical complete augmented law and opposite proportionality. A positive overall diagnostic success rate is therefore insufficient.

## 1. Fixed coefficient model and full record

Use the THREE-CLOCK spherical coefficient model of registered_active_and_inertial_mass, not the later twelve-clock arbitrary-profile active bounds or lift experiment. Sectors i=0,1,2 start at delta00,delta10,delta11. Both internal states 10,01 share the sector 1 coefficients. Whole-carrier inertia M_i>0 and active coefficient A_i>0 persist through static acquisition and the diagnostic. Ordinary mechanical pairs remain faithfully prepared, with two independent entire carriers.

Retain all eight native histories h=(a_h,b1,b2):

    p_i(h)=(q_a/4)[1+(eta_a/2) 1_(i=1)],
    (q_E,eta_E)=(2/3,1/8448),
    (q_F,eta_F)=(1/3,-1/4224).

These sum to one, have positive eight-cell support, and p0=p2 exactly. Their underlying latent support zeros are unchanged; no true sector tag is exposed.

Keep mode I (original mechanics) and A (static) each probability 1/2, and their three labelled settings each conditional probability 1/3. Every setting thus has unconditional mass 1/6. Original acquisition failure F=1 remains forbidden; the NEW diagnostic failure token is a separate outcome and never removes a static record.

For ij=01,02,12 the original law remains

    P(I,ij,h,h',Y in E,F=0)
       =(1/6)p_i(h)p_j(h') 1_[y_ij in E].

Require its complete product history cells and common signed point readings, no other support, -1<y_ij<1. Set d_ij=(arccos y_ij)^2 and

    u0=(d01+d02-d12)/2,
    u1=(d01+d12-d02)/2,
    u2=(d02+d12-d01)/2,

all strictly positive. Then M_i=C/u_i, C=KT^2>0, and every pair sum lies in (0,pi^2). These identified u_i are the fixed mechanical inputs. Neither an unsigned spring magnitude nor setting-specific stiffness may replace this inverse.

In nominal static slot j, preparation draws true sector i with unknown B_ji>=0, sum_i B_ji=1, independent of its subsequent native draw. There is no trusted cross-mode sector label. The clock reading of that TRUE carrier is

    z_i=(Z_i-,Z_i+)=(-2w_i-b,w_i+b),
    w_i=H A_i>0, H=gG/(12ac^2)>0,
    b=g U1 a/c^2.

G,c,a>0, the held radii2a,3a,4a, signed channels, instrumental zeros and common gradient/positive gain retain the original model. The gradient b may have either sign; a potential offset cancels. The diagnostic takes place AFTER that acquisition on that very same whole package.

## 2. What the reference spring measures

Let K_d>0,T_d>0 be the one diagnostic stiffness and tick, M_R>0 a fixed finite reference mass, and C_d=K_d T_d^2. In a release from rest at a fixed signed relative extension D_d, the two-body relative motion obeys

    relative_extension(T_d)/D_d
       =cos(T_d sqrt(K_d(1/M_i+1/M_R))).

Use its supplied OPEN first lobe, retain the signed ratio y_i^d in (-1,1), and invert

    d_i=(arccos y_i^d)^2
       =C_d/M_i+C_d/M_R
       =alpha u_i+beta,
    alpha=C_d/C>0, beta=C_d/M_R>0.

The diagnostic ratios need their own faithful signed readout and release normalization. The original and diagnostic ticks, springs and display scales need not be equal. Common diagnostic timing/loading across sectors gives a common positive affine map; it is not a claim of calibration equality. beta>0 excludes an infinite-mass reference, and alpha>0 excludes a mechanically uninformative zero coupling/tick. Every d_i lies strictly between 0 and pi^2.

Conditional on true i and nominal slot j, the diagnostic reports its true y_i^d with probability e_ji in [0,1], independent of h; otherwise it records perp WITH its already acquired z_i,h. Define

    r^+_ji=B_ji e_ji,  r^-_ji=B_ji(1-e_ji).

They are nonnegative with sum_i(r^+_ji+r^-_ji)=1 for every slot. The main theorem requires

    sum_j r^+_ji>0 for EVERY true i.                    (coverage)

This permits a sector to fail in some or most slots. It also implies representation sum_j B_ji>0. Coverage and same-carrier binding are substantive premises; neither follows from a nominal label or a nonzero pooled success rate.

For Borel reading sets E the entire static law is

    P(A,j,h,(Z,Yd) in E,F=0,diagnostic=success)
       =(1/6)sum_i r^+_ji p_i(h) 1_[(z_i,y_i^d) in E],

    P(A,j,h,Z in E,F=0,diagnostic=failure)
       =(1/6)sum_i r^-_ji p_i(h) 1_[z_i in E],

with the explicit diagnostic token perp on the second line. Both lines, all eight h and all three j sum to mode mass 1/2. No conditioning on successful diagnostics is substituted for this law. Original mechanical mode still sums to 1/2.

## 3. Finite necessary-and-sufficient admissibility certificate

Here all observed atoms and masses refer to the exact labelled conditional population laws; multiply by 6 to remove the unconditional setting factor before the static equations below. This is not a test based on means or a finite sample omitting a setting.

First check the complete mechanical law and domain in Section 1, the prescribed setting masses, original F=0 support, and finite readings throughout. Across all static outcomes invert EVERY clock pair:

    w(z)=-(Z_-+Z_+)>0,
    b(z)=Z_-+2Z_+.

Every b(z) must be the SAME real b, and the two signed coordinates must equal(-2w-b,w+b). No separate sign restriction is imposed on either clock channel.

Let S be the set of distinct successful pairs a=(z,y^d) having positive probability somewhere, and write d(a)=(arccos y^d)^2. Require 1<=|S|<=3, all -1<y^d<1, and no non-atomic or other static support. Every failure clock atom must be the z projection of some member of S. These are necessary under successful coverage. Equal atoms are merged in S; all zero-probability history/setting cells are still checked.

Enumerate the at most |S|^3<=27 assignments

    a_i in S,  i=0,1,2,

allowing repetitions but requiring that their image covers S. For a branch set z_i=z(a_i), w_i=w(a_i), d_i=d(a_i). Test feasibility of the following FINITE system:

1. Find alpha>0,beta>0 with d_i=alpha u_i+beta for all three i. The observed d_i already lie in (0,pi^2).
2. Find nonnegative r^+_ji,r^-_ji with row sums 1 and coverage sum_j r^+_ji>0 for each i.
3. For EACH slot j, EACH of the eight histories h, and EACH successful atom a, require

       s_j,h,a = sum_(i:a_i=a) r^+_ji p_i(h).

   Here s is the observed conditional probability of that successful reading and history, including zero cells.
4. For EACH slot j, h and distinct clock projection z of S (including those with zero observed failure mass), require

       f_j,h,z = sum_(i:z_i=z) r^-_ji p_i(h).

   Check every absent atom or history cell as zero, and allow no other outcomes.

All equations and strict/non-strict inequalities are linear in the branch variables alpha,beta,r^+,r^-; the clock amplitudes are already observed constants. Standard finite linear feasibility with open inequalities gives an exact certificate and a finite witness. A vanishing B_ji is allowed; strict coverage applies only to the summed successful mass for a true sector. There is no search over unobservable measures, missing sectors with freely invented clocks, source shapes or latent detector kernels.

Retain the original local weak-field and scale admissibility as well. In the given free-common-gain coefficient model, for any stipulated local amplitude tolerance epsilon>0 one may take U0=0 and

    g>(4|b|+6 max_i w_i)/epsilon.

This ensures the original sampled-segment bound; it does not control physical transfer remainders or an infinite affine ray. If an additional external calibration restricts g, the original allowed-g/local-amplitude condition must instead pass at that value. Such a calibration is not supplied by this diagnostic. No arbitrary-profile mass intervals or passive/lift coefficients from the separate joint-mass paper enter this test.

The complete law is admissible exactly when all preliminary tests and at least one branch pass. Failure means the COVERED, bound, ideal coefficient model is inconsistent; missing observation/access/coverage premises are not repaired by inventing weights.

### Necessity and construction of compatible worlds

Necessity follows by assigning each true sector its deterministic pair(z_i,y_i^d). Positive coverage places every such pair in observed S; each observed success comes from a true sector, so the assignment is onto. The actual alpha,beta and r's satisfy the displayed equations, including native histories and failed rows. All preliminary domains are inherited from the original law.

Conversely take any passing branch. Set B_ji=r^+_ji+r^-_ji. Where B_ji>0 put e_ji=r^+_ji/B_ji; where B_ji=0 choose any e_ji in [0,1], for example 0. Row normalization and coverage hold, and these choices reproduce every static history/read/failure cell by the finite equations.

For the mechanical realization, if the reference M_R is fixed, take

    C=M_R beta/alpha,  C_d=M_R beta,
    M_i=C/u_i,  K=C/T^2,  K_d=C_d/T_d^2.

All are positive and give both spring laws with their common ticks and the same actual carrier inertias. If the reference is not numerically calibrated, any positive fixed M_R gives a realization; equivalently choose C and set M_R=alpha C/beta. Choose permitted g, set H=gG/(12ac^2), A_i=w_i/H and U1=bc^2/(ga), with the original spherical source and local field construction. True coefficients are held fixed across every occurrence of their sector and through the post-static coupling. The two mechanical histories remain independent copies of the whole carrier; the static-then-diagnostic specimen is one and the SAME whole carrier.

These parameters reproduce the entire observed law, original zero support and all diagnostic masks. The proof assumes the stated whole-package coefficient model and compatible source/fixture attachment; it does not supply a physical transfer, force sensor or coupling realization.

## 4. Inertia classes and an observable proportionality decision

Let U1<...<Ur be the distinct known values among u0,u1,u2, r in{1,2,3}. On any admissible covered law, the distinct successful phases D1<...<Dr satisfy

    Dt=alpha Ut+beta.

There are exactly r of them: positive alpha separates unequal u, ties have the same phase, and coverage makes EVERY true phase appear. Thus sorting the observed phases identifies their inertia VALUES uniquely, with no sector tag, unknown reference scale or unknown gradient fitted to reverse them.

For r>=2 the first two distinct pairs determine alpha=(D2-D1)/(U2-U1) and beta=D1-alpha U1; all remaining pairs must lie on the same positive-affine line. For r=1 the single D permits 0<alpha<D/U1 and beta=D-alpha U1>0; no unique diagnostic scale is identified. These facts also give a simple phase-rank check within the admissibility procedure.

For every successful pair atom a, let U(a) be the inertia inverse value matched to its phase by that sorted list, and compute

    J(a)=U(a) w(z(a))>0.                              (observable)

Then on admissible covered records:

    There exists a compatible proportional world
    iff J(a) has one value on ALL observed successful pair atoms
    iff EVERY compatible world has A_i=k M_i for one k>0.

To prove the equivalence, in any compatible branch d(a_i)=alpha u_i+beta identifies U(a_i)=u_i. Hence the true three products u_i w_i occur among the observable J(a). Conversely each observed a receives positive success weight from some true sector, so every observed J(a) is one of those products. Coverage places every true sector's product in that same observed set, even if several sectors/pairs merge. Therefore

    {J(a):a in S} = {u_i w_i:i=0,1,2}

as sets for EVERY compatible world. Its being a singleton is branch-independent. Finally A_i/M_i=u_iw_i/(CH); equal positive products give k=J/(CH)>0, and distinct products preclude proportionality in every branch.

This proves both existence and truth identification under the covered model; there is no admissible record that permits one proportional world and one nonproportional world. Unrestricted admissibility must be checked first. A failed model is not classified as a physical violation of proportionality.

### Ties, equal clock atoms, failure rows and identity limits

If u_i=u_l, their diagnostic phases coincide; they form one mechanically tied class. Different active amplitudes within it still produce different successful pair atoms and different J, rejecting proportionality. Equal amplitudes merge, harmlessly: those true products already agree. If all u coincide, the test reduces to equality of all successfully observed clock amplitudes, while alpha,beta may remain undetermined.

Equal clocks in unequal inertia classes have different phases and are kept as different successful pair atoms; their products can still be compared. A failure row may merge such sectors because it lacks the phase, but its exact native eight-cell mass is retained in the linear equations. Zero mixture/success entries remain legal, without losing the strict requirement that EACH sector succeeds somewhere.

No sector identity inside an exactly tied class is claimed beyond what the full native/clock law independently supplies. In particular tied sectors 0 and 2 with the same clock have identical native histories and diagnostics. Exchanging their hidden preparation contributions can remain unobservable. This does not change their active/inertial ratio or the proportionality decision. The result replaces trusted cross-mode labels only for the specified coefficient decision, not for every identity question.

## 5. One matched control: positive success without coverage is insufficient

Relax ONLY successful coverage of true sectors 0 and 2. Keep same-carrier binding, all actual physical couplings, common alpha/beta, B independent of h, every true sector represented, all native histories and all clocks including failed diagnostics. Use any s>0 and

    u=(1,1/2,1/4),  M=C(1,2,4),
    (d01,d02,d12)=(3/2,5/4,3/4),
    alpha=1, beta=1/4, C_d=C, M_R=4C.

All original and diagnostic phases are strictly on the first lobe; diagnostic squared phases are (5/4,3/4,1/2). The reference spring and mechanical parameters are identical in both worlds.

Use the SAME genuinely mixing static preparation in both:

    B_0=B_2=(1/2,0,1/2),  B_1=(0,1,0).

Take e_j1=1 and e_j0=e_j2=0 for every j. Each true sector appears, and the nominal sector 1 slot always produces a successful same-carrier verification, but sectors 0,2 are never successfully checked. Static success rate is 1/3, or 1/6 of all mode-mixed trials, so this is not a zero-success instrument.

Choose b=s and the two positive true amplitude profiles:

    World P: w=(s,2s,4s),  u_iw_i=(s,s,s),          proportional.
    World N: w=(4s,2s,s),  u_iw_i=(4s,s,s/4),       nonproportional.

Use the same finite common g and C in both. Then k=s/(CH) in P, while no common positive ratio exists in N. Both obey the original spherical coefficient law. Taking g>28s/epsilon with U0=0 realizes the same prescribed positive local weak-field tolerance in both worlds.

The three clock values that occur are

    z_small=(-3s,2s),  z_middle=(-5s,3s),  z_large=(-9s,5s).

For nominal slots j=0,2, the diagnostic ALWAYS fails. Conditional on each such slot the complete native-and-clock masses are

    P(h,z_small,perp)=p0(h)/2,
    P(h,z_large,perp)=p0(h)/2.

These agree in P and N because p0=p2 and B mixes the two sectors equally. For j=1 the complete record is

    P(h,z_middle, y^d=cos(sqrt(3/4)),success)=p1(h).

Every other conditional cell is zero. Multiply by 1/6 for the original unconditional setting weights. The mechanical laws are identical in the two worlds. Thus EVERY augmented signed-clock/history/diagnostic/failure cell agrees, while true proportionality differs. The failed carriers are not replaced or misbound; their true diagnostic phases simply never enter the observed record. The only withdrawn main hypothesis is their positive successful coverage.

This control also shows why a pooled positive success fraction and a nominal label are not coverage evidence. Native resampling alone cannot separate the 0/2 contributions. A barcode would instead need an independent faithful tag-to-composition premise; none is added here.

## 6. Scales, access, costs and physical limits

The original dimensionless u_i identify Mi/Ml=u_l/u_i. If r>=2, the diagnostic additionally identifies alpha,beta and hence C/M_R=beta/alpha and M_i/M_R=beta/(alpha u_i) within the supplied mechanical model. A physically calibrated reference could transfer its mass scale; no reference calibration or native absolute mass unit follows from being “fixed.” If all u tie, even alpha,beta need not be separately identified. Clock H and original mechanical scales retain their allowed common freedom, so the magnitude of k is not generally fixed.

The inputs remain distinct: faithful preparation in the THREE original mechanical pairs; untrusted stochastic static labels B; the observed actual-clock/history/reference-spring record; SAME-SPECIMEN persistence and binding across those measurements; common diagnostic stiffness/tick and first-lobe calibration; common signed clock gain/background/zero conventions; and coverage of every true sector. The proof derives the finite association/class decision from these premises. It does not infer that a diagnostic acts on the correct specimen from an exchangeable separately prepared copy.

Required and unobserved resources include carrier/source preparation and its stochastic composition, nominal setting retention, native record acquisition, original pair preparations and spring loading/recoil, static supports and held clock/transfer/controller contributions, specimen custody and persistence, moving or reconfiguring the same whole package, the finite reference and diagnostic spring/release/timer/ratio readout, handling failures without discarding prior data, and full source/reference/fixture/clock/carrier reset. Damage, changed loading stress, adapters or removed supports can alter inertia or active coefficients; the model requires their inclusion in the complete package or controlled compatibility. Equal preparation distributions are not that physical identity connection. A conventional comparator receives the same records, reference, binding, coverage and calibration premises. No efficiency or physical feasibility has been established.

The separate joint-active/passive source input underscores cross-protocol identity and finite-feasibility boundaries; its arbitrary-shape bounds, lift losses and additional observables are NOT used. CL071's harmonic-probe energy/clock/phase assumptions are disjoint and are not imported. No new sensor, field family, native history law, source-to-physical-unit map, instrument implementation or empirical run is authorized.

## Reviewed sources

- [Testing proportionality of active and inertial mass across three carrier sectors](registered_active_and_inertial_mass.md)
- [Inertial mass ratios from three relative-extension readings](sector_inertial_mass_ratios.md)
- [Can the same three carriers have proportional passive and active gravitational coefficients?](joint_active_and_passive_gravitational_mass.md)
- [Finite observer records and preparation](finite_observer_records_and_preparation.md)

Scientific report SHA-256 315095314e08564e46673f34813b1214c17892335e67e487f8e54953a80faa72. Independent review SHA-256 eb5604be23e876b23c116fe9f2d59b6a38b7749d14731322981136f6b5635a1c.
