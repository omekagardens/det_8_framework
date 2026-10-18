# RI240 canonical comparison and the blocking companion row

30 September 2026, Honolulu. Manual source-only author result for independent
review. An actual D2 cancellation requires a quantified reversal of the two
canonical competition masses, not merely a failure of their ordering.
A complete feasible-exchange lemma identifies the companion row or objective
comparison that must be controlled before inferring an allocation.

The actual canonical comparison is not resolved in this packet. No actual
normalized witness or signed inconsistency is asserted.

## 1. Fixed optimization problem and accepted decision

Keep the unchanged RI63 canonical lexicographic minimizer of its complete
primary problem. Its row weights are the actual prefix-history masses,
including natural-history multiplicity, not uniform weights.

At the exceptional five-parent P:r<a<b,r<x,o<x, write
i=r_r,j=r_a,k=r_b,l=r_o,m=r_x. The complete canonical proper mass is

    C_P(r)=a0 kappa_i+t(r)mu_(i,l)+v(r)tau_i+n(r)nu_(i,j),
    a0=41/352,  C_P(r)<=1.                               (C1)

All 32 records and every individual ideal remain. The other six proper
canonical terms are zero by the accepted defect-neutrality theorem;
their actual strict-restoration probabilities remain positive.

The complete two-parent incidences from RI231 are

    kappa: P and Y=C4 disjoint {o},
    mu:    P and P_mu:r<a<b<y,o<y,
    tau:   P and P_tau:r<a,r<x<y,o<x<y,
    nu:    P and P_nu:r<a,r<x,o<x,a<y,x<y.                 (C2)

On the companion parents, the changed family has respectively potentials

    1/64, 1/64, p(r)=q(N,{r,a}), p(r)=q(N,{r,a}),
    N:r<a,r<x,o<x,  p(r)>0.

The P potentials remain
t(r)=q(C3 disjoint {o},full),
v(r)=q(N,{r,o,x}), n(r)=q(N,full), with their induced records.
All other canonical components in every companion row remain fixed,
possibly nonzero contributions. They cannot be replaced by slack.

At the actual canonical optimum there is a tight P row in each root
sector and

    M_i=max_(P rows with root i)
              [t(r)mu_(i,l)+v(r)tau_i+n(r)nu_(i,j)],
    kappa_i=(352/41)(1-M_i), 0<=kappa_i<=352/41.           (C3)

The maximum and every competing coordinate are actual fixed quantities.
The original objective and all companion constraints are retained.

RI238, now independently accepted, proves the full normalized iff:

    d!=d7: a solution exists iff C_b=0;
    d=d7:  a solution exists iff C_2(ell)!=0.              (C4)

Here d=N1-N0, d7=-theta^2 K/(1-theta/8)<0,
C_b=g2(0)b1^2-g2(1)b0^2, and
C_2(ell)=g2(0)ell1-g2(1)ell0. This packet uses C4; it does
not reopen the settled T4 elimination or D5 recovery.

## 2. Cancellation requires a nontrivial reversed competition gap

Retain RI235–RI238's exact actual separation

    chi_i=(35/36)kappa_i,
    Q(x)=x^2-(1-2theta)x,
    Xi=b1^2 Q(chi0)-b0^2 Q(chi1),
    C_b=C_hat+lambda Xi, C_hat<-1/12000,
    lambda=s rho(1-rho)/64<7/22656.

Consequently C_b=0 requires Xi>236/875. RI238 already proves
kappa0<=kappa1 implies C_b<0. We now allow a small reversal.

The actual capacity C3 gives 0<=chi_i<=3080/369<9. Also

    0<b0^2-b1^2
       =(41/22000)(b0+b1)<41/11000<1/250,
    Q(x)>-1/4 for x>=0,

using 0<theta<1/10000 and 0<b1<b0<1.
If kappa0>kappa1, put delta_chi=chi0-chi1>0. Then, directly
factoring the quadratic difference,

    Q(chi0)-Q(chi1)
       =delta_chi[chi0+chi1-(1-2theta)]<18 delta_chi,
    Xi=b1^2[Q(chi0)-Q(chi1)]-(b0^2-b1^2)Q(chi1)
       <18 delta_chi+1/1000.                             (C5)

For the first term, a negative quadratic difference is already below
the positive right side; a nonnegative difference may be multiplied
by b1^2<1. Thus this bound does not assume monotonicity of Q on its
whole nonnegative domain.

If kappa0-kappa1<=1/70, then delta_chi<=1/72. Equation C5 yields

    Xi<1/4+1/1000=251/1000<236/875,

where 251*875=219625<236000. The same conclusion C_b<0 holds
when kappa0<=kappa1 by the accepted comparison. Therefore

    kappa0-kappa1<=1/70 implies C_b<0,
    M1-M0<=41/24640 implies C_b<0.                       (C6)

Both tests retain equality. In particular the simpler sufficient premise

    M1-M0<=1/625

suffices, since 41*625=25625>24640. Conversely an actual cancellation
must have

    kappa0-kappa1>1/70,
    M1-M0>41/24640>1/625,
    Xi>236/875.                                         (C7)

This strengthens the required gap, but does not assert that the actual
competition masses satisfy C6. It is a comparison of the fixed optimum,
not a relaxed independently selected allocation example.

## 3. Why a kappa-only exchange cannot establish the order

A proposal to decrease kappa0 and increase kappa1 leaves every root-1
competing mass unchanged. At any root-1 P row that is tight by C3,
its mass then increases by a0 times the positive kappa1 increment.
It violates the original row constraint immediately. The converse
root transfer has the same problem in a tight root-0 row.

Thus a root-order argument cannot use a kappa-only feasible exchange.
It must accompany any increase of kappa_i with decreases of other
competing contributions in every affected tight P row. Negative
individual cost or equal Y potentials do not supply that feasibility.

This rejects the proposed exchange premise for this actual optimum;
it is not a countermodel to the fixed law or a theorem that no more
complete comparison can work.

## 4. A complete kappa to tau exchange and its exact blocker

The following lemma gives a concrete coupled test rather than treating
the missing companion constraints as an unspecified global problem.

Fix root i and retain all P records with that root. Let

    v_i^max=max_(r:r_r=i) v(r),
    L_i=sum_(P rows root i) pi_P(r)[v_i^max-v(r)],
    T_i=sum_(P_tau rows carrying tau_i) pi_tau(r)p(r).     (C8)

All weights and individual-history multiplicities are the original
ones. These are definitions of fixed finite sums, not evaluated input
coordinates or new sampling measures.

Let the complete companion slack be

    S_tau(r)=1-C_can(P_tau,r),

where C_can includes every canonical proper contribution, not just
p(r)tau_i. Consider, for small epsilon>0, exactly

    Delta tau_i=epsilon,
    Delta kappa_i=-(v_i^max/a0)epsilon,
    Delta mu=Delta nu=0,
    all other canonical coordinates unchanged.           (C9)

Suppose kappa_i>0 and every P_tau row carrying tau_i has strictly
positive complete slack. There are finitely many such rows, and all
p(r)>0. Choose epsilon smaller than both the available kappa
nonnegativity bound and every S_tau(r)/p(r).

Then C9 is feasible in the entire original canonical problem:

- Each affected P mass changes by epsilon[v(r)-v_i^max]<=0,
  including every previously tight P row.
- Each affected Y mass decreases, since its only changed term is
  kappa_i/64.
- Each affected P_tau mass increases by p(r)epsilon but stays
  below one by the chosen complete slack.
- No P_mu or P_nu row changes. The exhaustive two-parent incidence
  proves that no other row is affected.
- All changed coordinates remain nonnegative.

There is no modification of the strict law in this argument: C9 is
a candidate variation used to test optimality of the unchanged
canonical boundary vector. No actual coefficient is reassigned.

The accepted full objective-change formula is

    Delta Phi=-sum_P pi_P Delta C_P
               -sum_Ptau pi_tau p Delta tau
               -sum_Pnu pi_nu p Delta nu.

Substitution of C9 gives exactly

    Delta Phi=epsilon(L_i-T_i).                          (C10)

Therefore the canonical primary optimum obeys the following necessary
alternative:

    kappa_i=0, or some carrying P_tau row is tight,
                or T_i<=L_i.                            (C11)

Indeed if all three alternatives failed, C9 would be feasible with
strictly negative objective change, contradicting primary optimality.
This is a complete coupled blocker theorem; the possible nonzero
other components in P_tau are retained inside S_tau.

If T_i=L_i, primary cost alone is silent. A lexicographic argument
must additionally use the actual global component order: a feasible
zero-cost C9 descends only if its earliest changed coordinate has
negative change. If tau_i comes before kappa_i, C9 instead increases
the first changed coordinate. No global ordering is guessed from
the shapes or from the two root bits.

C11 does not establish either kappa value. It identifies precisely
why simply transferring mass from kappa to a seemingly more rewarded
family is not yet a proof: either the complete companion row blocks
it or the weighted gain comparison does.

## 5. Exact missing premises and a bounded acquisition obligation

The admitted RI63 COMPLETION proves the existence and identity of the
complete canonical solution, including primary and sequential optimal-face
certificates. It does not print the following selected values or a theorem
ordering them. RI231 CANONICAL_CAPACITY supplies their symbolic incidence,
not their residual allocations.

For the C9 route the missing items are specifically:

1. The complete slack S_tau(r) on each carrying P_tau row, retaining
   all other incident canonical components, or a proof that all such
   slacks are positive when kappa_i>0.
2. The actual weighted comparison T_i>L_i, or its opposite/equality,
   with the original pi and p,v potentials.
3. Only on primary equality, the applicable earlier-coordinate
   bindings and relative canonical order needed to prove a
   lexicographic descent.

A sufficient analytic lemma would prove the first two under kappa_i>0
for each i; C11 would then force both kappas zero and hence C_b<0.
No such premise is assumed, and no zero-slack companion row is ignored.

A more direct sufficient comparison need only establish the one-sided
canonical bound kappa0-kappa1<=1/70, equivalently the bound in C6.
That can be supplied by a same-law analytic optimal-face lemma or,
under separate explicit source admission, a bound on these two existing
coordinates tied to their complete P/Y presentations and the canonical
selector. The scientific certificate is not opened here, no component
index is guessed, and no automatic optimization or coefficient extraction
is proposed as already authorized.

Neither gap statement is a proof of nonderivability from the full law.
They are exact missing premises for the attempted routes. A new broad
coverage or identifiability exercise would not supply them.

## 6. Preserved system and scope

HOOK_AND_EXCEPTION.md preserves the actual hook formula, develops an
independent exceptional D2 bound, and prints the original thirteen
equations and complete recovery. All ten unknowns, all records, all
individual ideals, actual g1/g2 offsets, minima/ties, strict endpoints
and unchanged scales remain binding.

Only admitted analytic sources and administrative provenance are used.
No scientific body, new coordinate read, numerical amplitude, automatic
scientific arithmetic, H/z, graph/LP, runtime, capture, fixture/card,
measurement, RET or repository/Git/index operation occurs. This bounded
packet does not assign its own successor or claim physical QM, geometry,
mass/gravity or an all-size result.
