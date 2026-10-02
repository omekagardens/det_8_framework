> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Conditional optimization of the complete parent block

1 October 2026, OBSCURED-LOCATION. RI264 manual author result pending independent
adjudication. This is a conditional theorem for the unchanged original
canonical problem, not a calculation of its unknown allocations.

Holding every other original allocation fixed to the same feasible
canonical point, the four coordinates kappa_i, tau_i, nu_(i,0), nu_(i,1)
have an exact one-variable optimization. All carrying-parent capacities
are retained. They are residuals of that one fixed point, not freely
chosen inputs. The companion note proves the finite attained maximum,
the original lexicographic endpoint and a sharp conditional kappa test.

## Fixed rest and admitted complete incidence

Fix sector i and write

    p=p_i>0, v=v_i>0, n_l=n_(i,l)>0,
    h_l=h_(i,l)>0, s_lm=s_(i,l,m)>0, a0=41/352,
    kappa=kappa_i, tau=tau_i, nu_j=nu_(i,j), l,j=0,1.     (B1)

All lower coefficients are the actual fixed-prefix ones. None is
acquired or numerically evaluated. The varying coordinates are exactly
these four; mu, eta, xi, sigma, other sectors and every unlisted
allocation are fixed to their actual values at the SAME full feasible
canonical point. In particular, accepted canonical zero roles stay
zero. The theorem does not extend the reduced row formulas to an
arbitrary original feasible point whose other roles differ.

RI231 CANONICAL_CAPACITY sections 1–3 exhaust the ideals and two-parent
components of P. RI248 COMPANION_ROW sections 2–5 exhaust the companion
and prove the coefficients and record transports used here. Their
complete carrying inventory is

| Changed coordinate | Carrying parents | Potentials in those parents |
| --- | --- | --- |
| kappa_i | P and Y | a0 and 1/64 |
| tau_i | P and P_tau | v and p |
| nu_(i,j) | P and P_nu with its compulsory j | n_l and p |

Each terminal has exactly two maxima. Every possible parent presentation
comes from deleting one of them; ratio paths preserve that terminal.
The compulsory r mark selects i, and the compulsory r,a marks select
i,j for nu. The accepted marked incidence connects every optional
assignment without changing those compulsory marks. Distinct terminals
and marks distinguish the four original coordinates.

Consequently no other parent carries these coordinates. In particular
P_nu carries neither kappa nor tau, and a row with its fixed j does not
also carry the other nu. There is exactly one proper occurrence of
its compatible nu coordinate. Thus the complete residual B_nu below
is independent of ALL FOUR changing coordinates. This independence
follows from the inventory, not from the name "residual".

## Every original marked constraint

Retain i=r_r, j=r_a, k=r_b, l=r_o, m=r_x on P, and t=r_y
on P_tau. The t used as a record index is distinct from the positive
lower coefficient t_K(r) multiplying mu. For every carrying marking,

    a0*kappa+v*tau+n_l*nu_j
                    <=1-t_K(i,j,k,l,m)*mu_(i,l),        (B2)

    kappa/64<=1,                                       (B3)

    p*tau<=1-h_l*eta_(i,l)-n_l*xi_(i,l,m)
                                      -s_lm*sigma_i,   (B4)

    p*nu_j<=1-B_nu(i,j,l,m,k)-v*xi_(i,l,m).             (B5)

B2 is the COMPLETE P row: its other six proper roles vanish by the
accepted canonical neutrality theorem, not by omission. B3 is the
complete Y row because kappa is its only possible canonical proper
contribution. B4 is the complete P_tau row, including eta, xi and sigma.
B5 keeps every other original P_nu proper contribution in B_nu, even
when nonzero or binding. All its summands are fixed and nonnegative.

There are sixteen P records at fixed i; four for each fixed l,j.
P_tau has sixteen records at fixed i; its coefficient expression is
independent of j,t by the admitted transport and therefore appears
four times for each l,m. P_nu has eight records at fixed i,j,
indexed by l,m,k. All labels, both newborn bits and equivariant
presentations remain. Equivalent inequalities may be compressed by
an exact minimum, but original objective multiplicities may not.

Define the UNEVALUATED residual caps

    R_lj=min_(k,m) [1-t_K(i,j,k,l,m)*mu_(i,l)],

    N_j=min_(l,m,k)
          [1-B_nu(i,j,l,m,k)-v*xi_(i,l,m)]/p,

    T=min_(l,m)
          [1-h_l*eta_(i,l)-n_l*xi_(i,l,m)-s_lm*sigma_i]/p.
                                                               (B6)

The last minimum is exactly the minimum over all P_tau j,t,l,m
records, because their j,t independence was proved. R retains all four
k,m markings for each l,j. N retains all eight l,m,k markings for
each j; no independence of B_nu is asserted beyond the changing block.
N_j is a scalar cap, not the earlier four-event parent N or the
vanishing hook corrections N0,N1.

The original fixed feasible point witnesses

    0<=R_lj<=1,   0<=N_j<infinity,   0<=T<infinity.       (B7)

Indeed each residual is at least its current nonnegative block
contribution. The upper R bound follows from t_K*mu>=0. Finiteness
follows from finite original rows and p>0. These facts do not make
the caps independent: they share the SAME fixed allocations and
remain coupled to every unchanged original constraint.

Writing

    x=a0*kappa, y=v*tau, r=x+y,
    b=v*T>=0, Rmin=min_(l,j)R_lj,                       (B8)

the exact affected constraints are

    x,y,nu_0,nu_1>=0,
    r+n_l*nu_j<=R_lj for all l,j,
    nu_j<=N_j, y<=b, x/a0<=64.                          (B9)

Every unchanged original row stays feasible because all its coordinates
stay fixed. Conversely B9 implies B2–B5 for EVERY original marking.
This is exact feasibility of the restricted block, not a substitute
for checking feasibility of the fixed rest.

## Derive the Y redundancy and exact scalar domain

Keep the Y cap in B9 until the P bounds and nonnegativity imply

    0<=x<=r<=Rmin<=1,
    kappa=x/a0<=1/a0=352/41<64.                         (B10)

Thus Y is redundant for this restricted feasible set, with the same
derived canonical margin as before. No assumed Y slack was needed.

Every feasible block has r in [0,Rmin]. Conversely, for any such r,
the choice x=r, y=nu_0=nu_1=0 is feasible in B9, including Y by B10.
Thus the scalar domain is EXACTLY the nonempty compact interval

    D=[0,Rmin].                                        (B11)

For a fixed r in D, all remaining bounds decouple:

    0<=y<=min(r,b), x=r-y,
    0<=nu_j<=g_j(r),
    g_j(r)=min{N_j,(R_0j-r)/n_0,(R_1j-r)/n_1}.          (B12)

All three entries of each minimum are nonnegative throughout D.
No nonnegativity lower bound on nu has been lost. If Rmin=0 the
domain is the singleton {0}; this forces kappa=tau=0, but does NOT
in general force both nu coordinates to vanish. Their g_j(0) values
must still be retained.

## Derive the complete primary reward

RI258 PARENT_CIRCULATION and DUAL_NU_AND_EQUALITY establish the
complete marked weights

    Pi_P(i,j,k,l,m)=3p/1280,
    Pi_tau(i,j,l,m,t)=7v/3840,
    Pi_nu(i,j,l,m,k)=n_l/768.                           (B13)

They follow from the admitted fixed-prefix history identities,
including both final newborn factors; they are not a uniform-row
replacement. For each fixed sector, summing its sixteen P and
sixteen P_tau records gives respectively

    Pi_P,i=3p/80,   Pi_tau,i=7v/240.                    (B14)

For a fixed j,l, the four relevant records in each of P and P_nu
have masses 3p/320 and n_l/192 respectively. The complete nu
coefficient is therefore

    beta_nu_j
      =-sum_l[n_l*(3p/320)+p*(n_l/192)]
      =-7p*(n_0+n_1)/480.                              (B15)

Y is objective-neutral, but its constraint was retained above.
There are no other carrying objective terms by the full inventory.
Consequently, writing

    c=7p*(n_0+n_1)/480>0,

the original objective on this block has the exact form

    Phi=Phi_fixed-W(x,y,nu_0,nu_1),

    W=(3p/80)*x+(p/15)*y+c*(nu_0+nu_1).                (B16)

For y the P and P_tau rewards sum to

    3p/80+(p/v)*(7v/240)=p/15,

whereas x has only its P reward 3p/80. Phi_fixed collects every
unchanged contribution and is independent of this block. It is
not given a numerical value. Maximizing W is exactly minimizing
the original primary objective WITH this rest fixed.

## Unique best block at a fixed r

Substituting x=r-y in B16 gives

    W=(3p/80)*r+(7p/240)*y+c*(nu_0+nu_1).               (B17)

The coefficients of y and each nu are strictly positive. Their
intervals in B12 are independent at fixed r. Hence the unique
primary-best block at that r is

    y(r)=min(r,b),       x(r)=(r-b)_+,
    tau(r)=min(r,b)/v,   kappa(r)=(r-b)_+/a0,
    nu_j(r)=g_j(r).                                    (B18)

This includes zero caps and ties among upper-bound expressions:
a tie changes neither the unique upper-bound VALUE nor the
strictly increasing coordinate objective. At a fixed r there is
no separate secondary choice among four-coordinate allocations.

The remaining scalar reward is exactly

    F(r)=(3p/80)*r+(7p/240)*min(r,b)
               +c*sum_(j=0,1)
                     min{N_j,(R_0j-r)/n_0,(R_1j-r)/n_1},
    0<=r<=Rmin.                                        (B19)

Every feasible block satisfies W<=F(r). Equality holds if and only
if ALL FOUR coordinates equal B18. Every B18 block is feasible.
Thus the full restricted primary-optimal set is exactly the image
of argmax_D F under B18. The companion note proves its attained
maximum and actual lexicographic selection without any engine.

## Scope retained

This derivation uses the accepted complete canonical zero roles,
actual lower law, component incidence, marked weights and original
selector. It does not choose new capacities, change mu/eta/xi/sigma,
or prove that independently supplied cap values come from any
full feasible or optimal system.

All original 13 equations and 10 coordinates, u2=-1, complete
recovery and actual offsets remain as in RI248 CANONICAL_BINDING
section 7. Accepted hook d=0!=d7 and normalized-system existence
iff actual C_b=0 remain. Original records, labeled ideals, both
newborns and strict restoration endpoints are unchanged. B9 uses
the closed canonical constraints; it does not replace strict-law
restoration by a closed endpoint.

All fifteen whole typed/raw boundaries and the 423-source manifest
remain by reference. Original scientific routes and RI250 stay closed.
No original body/hash/checker, scientific JSON, new coefficient/cap
acquisition, mathematical engine, H/z/vector reconstruction, subject
execution, measurement/RET or repository/Git/index operation is used.

