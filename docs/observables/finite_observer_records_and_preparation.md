# Finite observer records and preparation

A conserved quantity can influence a committed record without that record identifying the quantity when the observer preparation is unknown. The adopted GDM042 and E040 results make this distinction explicit in one finite classical model. A known reference restores the chosen mean only under a shared, nonuniform preparation premise. Neither result supplies a physical apparatus, mass interpretation or calibrated unit.

## The fixed source and observer

Use source coordinates i=(00,10,01,11), source and reservoir rows r=(0,1,0,1), e=(0,0,1,1), and Q=r+e=(0,1,1,2). Add an observer bit m=0,1; joint coordinates are (i,m), with states represented by columns. Native validity holds on the full simplex Delta8, including arbitrary source–observer correlations. The trial ends after exactly three births.

The first two births commit distinct data marks D_0 or D_1. Every actual ideal is supported: the empty parent has its sole empty ideal; a singleton has empty E and full F ideals. Set

    M(x)=[[3/4+x/2,1/4-x/2],
          [1/4+x/2,3/4-x/2]],
    D(x)=diag(1,M(x),1), K=D(0),
    B_(S,b|C)=(q_C(S)/2)D(x_C,S),
    A_(S,D_b|C)=B_(S,b|C) tensor I2.

At empty, (q,x)=(1,0). At a singleton, (q_E,x_E)=(2/3,a) and (q_F,x_F)=(1/3,c), where a=1/8448 and c=-1/4224=-2a. Both bits have the same map but remain separate outcomes. The observer does not change during these births. The [conservation and record-access note](finite_conservation_and_record_access.md) explains the underlying source model and its additional composition assumptions.

The third birth is a receipt R_y, y=0,1, whose past is the ENTIRE two-event parent. Write

    u=(1/2,1/2)^T,
    tau_0=3/4, tau_1=1/2, tau_2=1/4,
    f_0^(q)=(tau_q,1-tau_q),
    f_1^(q)=(1-tau_q,tau_q),
    C_y^(q)=u f_y^(q),
    T_y=sum_i |i><i| tensor C_y^(Q_i).

Thus T_y[j,n;i,m]=delta_(j,i) f_y^(Q_i)[m]/2 for BOTH final observer values n. Receipt effects and observer state changes are specified together; a recorded label is not being substituted for an instrument.

At sizes zero and one every R branch is zero. At size two every D branch and every proper-ideal R branch is zero. Branches from impossible phase prefixes have zero algebraic extensions; normalized dynamics is asserted only on admitted nonterminal prefixes. This supplied phase/support family is not a positive-all-ideal extension to arbitrary horizons. Old marks and relations remain immutable. The formulas use current unmarked size, actual ideal status and declared residual coordinates, not old-mark values or preparation names. Marked relabeling transports the same maps; birth count is a protocol index, not physical duration.

Each data branch has twelve positive joint entries: the six source pairs 00->00,10->10,10->01,01->10,01->01,11->11, each with unchanged m. The other 52 entries vanish. Each receipt has sixteen positive entries, all fixing source i while allowing every m->n; its other 48 entries vanish. Wrong-stage/ideal maps are wholly zero. Supported branch effects are strictly positive on Delta8, so outputs normalize by their FULL branch mass. Zero events have no conditional child.

The complete data-stage sum is K tensor I2: the singleton cancellation uses (2/3)a+(1/3)c=0. K is column stochastic. Since f_0^(q)+f_1^(q)=(1,1), the receipt sum is I4 tensor J, J=u(1,1), also column stochastic. Every admitted stage is therefore normalized. With w4=(1,1,1,1)^T/4 and w8=w4 tensor u, each D(x) preserves w4 and each C_y^(q)u=u/2. Consequently the branchwise anchor coefficients are q/2 for data, 1/2 for supported receipts and 0 for zero branches.

The finite consistency check uses full unnormalized maps. At the empty base, swapping the two incomparable data births gives the same product (1/6)[D(a)K tensor I2] for every bit pair; all typed pairs involving R give zero. At a singleton, D/D has a forbidden second D; D/R or R/D has a forbidden first R or a second R on a proper transported old ideal; R/R has a forbidden first R. Even the old full ideal omits the other newborn, so is proper after transport. Both orders therefore give zero in every such case. After the nonzero empty-base diamond, both receipt suffixes left-multiply the same map by T_y; all other suffixes vanish. Linear terminal projections preserve these equalities. Size two admits no further two-birth diamond. These statements exhaust this horizon, not larger ones.

Every positive source transition preserves Q. The exchanges 10->01 and 01->10 have source/reservoir changes (-1,+1) and (+1,-1); self-transitions and receipts have changes (0,0). All observer transitions remain in the ledger, but both observer states are assigned zero Q charge. Thus Qbar=Q tensor(1,1) is conserved pathwise. Conditional balance compares before and after conditioned on the SAME positive branch/history/record event, including updated mixed-sector weights. Normalization separately yields unconditional conservation. Zero assigned Q is a bookkeeping premise, not zero physical observer energy.

## Complete committed records

Fix natural birth labels once. Observe only Z=(h,y), where h=(s,b1,b2), s=E or F, and both actual data bits are retained. The receipt has both data events in its past. No initial source label, preparation identifier, intermediate state or terminal residual basis is observed. There are eight data histories and two receipts, hence sixteen supported record cells.

Let

    N(x)=M(x)M(0)
        =[[5/8+x/4,3/8-x/4],
          [3/8+x/4,5/8-x/4]],
    W_h=(q_s/4)diag(1,N(x_s),1),
    g(s)=(1,1+x_s/2,1-x_s/2,1).

For any joint input nu in Delta8 the complete law is

    P_nu(h,y)=1^T T_y(W_h tensor I2)nu
      =(q_s/4)sum_(i,m)g_i(s)f_y^(Q_i)[m]nu_(i,m).

This formula assigns every actual bit pair separately. Summing y, all four bit pairs and both ideals gives one, using sum_s q_s g_i(s)=1. All sixteen cells are positive; the forbidden channels remain zero in the larger microscopic/record space.

For a product input rho tensor pi, the latent weight for each final observer n is

    rho_i pi(m0) B1[k,i] B2[j,k]
      1_(m1=m0) 1_(m2=m1) f_y^(Q_j)[m2]/2.

Sum BOTH n, all source/observer indices and all h,y. There is no selected observer output, herald, retry or omitted complement. The latent indices account for transitions; they are not extra observations.

For the same observer delta0, sources delta00 and delta11 yield receipt probabilities (3/4,1/4) and(1/4,3/4). For each of four bit pairs their respective (E,R0),(E,R1),(F,R0),(F,R1) probabilities are (1/8,1/24,1/16,1/48) and (1/24,1/8,1/48,1/16). Each full law sums to one. The records therefore carry statistical Q information, without perfect single-shot recovery or the full source/reservoir transfer ledger.

## Unknown preparation and one reference

Now restrict the preparation family to independent rho tensor pi_p, with arbitrary rho in Delta4 and pi_p=(p,1-p), p in[1/2,1]. This independence premise is additional to the full-domain native theorem. Define

    mu=E_rho[Q], d=rho10-rho01, t=2p-1,
    B=t(1-mu).

Averaging the receipt effect gives f_y^(Q)pi_p=1/2+(-1)^y t(1-Q)/4. Hence the complete law becomes

    P(s,b1,b2,y)=(q_s/8)[1+x_s d/2+(-1)^y B/2].

The four rows (E,0),(E,1),(F,0),(F,1) apply to EACH of the four actual bit pairs, giving all 16 cells and all complements. The cross term disappears because only the Q=1 coordinates have nonconstant g, and there 1-Q=0. Summing receipts and bits gives P(s)=q_s(1+x_s d/2), then total mass one.

The ideal marginal recovers d=(2/a)[P(E)/q_E-1], and the receipt contrast Delta_test=P(y=0)-P(y=1) recovers B=2Delta_test. Thus complete test laws agree if and only if d and B agree on the admitted parameter domain. Unknown p can hide mu even with every record probability retained.

For example, world 1 has rho=(3/4,0,0,1/4), p=1, mu=1/2; world 2 has rho=delta00, p=3/4, mu=0. Both have d=0,B=1/2. Their identical complete cells are:

| Ideal/receipt | Probability per actual bit pair | Multiplicity |
| --- | ---: | ---: |
| E,0 | 5/48 | 4 |
| E,1 | 1/16 | 4 |
| F,0 | 5/96 | 4 |
| F,1 | 1/32 | 4 |

Each law sums to one, with both p values strictly above 1/2. Describing these witness sources grants no hidden target-label access.

Add ONE separately labelled reference setting with known source delta00 and the SAME unknown observer preparation p. Its complete law is

    P_ref(s,b1,b2,y)=(q_s/8)[1+(-1)^y t/2],
    Delta_ref=P_ref(y=0)-P_ref(y=1)=p-1/2.

If Delta_ref>0, exact population laws identify p and

    mu=1-Delta_test/Delta_ref.

This holds for every source rho at p>1/2. Zero test contrast with positive reference contrast means mu=1. At p=1/2, however, both delta00 and delta11 tests have the same complete law q_s/8 per cell and the same reference law, although their means are 0 and 2. Reference contrast zero therefore defeats general identification over Delta4; the ratio must be refused, not divided by zero. Even away from this boundary, full rho is not generally identified: equal mixtures of 00/11 and 10/01 both have d=0,mu=1.

## Preparation is a resource

The reference result assumes a known reference source and setting label, initial independence, the same stable preparation distribution p across settings/repetitions, a fixed instrument and complete population laws. Same p does not mean access to an individual initial observer bit or the same microscopic realization. The algebra does not certify stability or physical preparation.

For any pre-receipt nu, T_y nu=z^y tensor u, where z_i^y=sum_m f_y^(Q_i)[m]nu_(i,m). After a positive receipt the observer is uniform and uncorrelated with the conditioned source. It is not returned in pi_p when p>1/2. Reuse without renewed preparation moves a subsequent independent trial to the p=1/2 boundary. Refresh/reset, source replacement, reference preparation, physical readout, retention, failures and controller/environment costs need their own complete account.

A conventional comparator receives the same records, setting labels and preparation assumptions. Exact population identification gives neither finite-sample accuracy nor a noise/conditioning guarantee near zero reference contrast. The supplied conserved Q, observer charge convention and controlled coupling establish no physical energy, mass, time, action, unit, calibrated detector or efficiency advantage. This is a finite mathematical observer and reference result; physical realization remains a separate question.

## Reviewed source identities

GDM042 report SHA256 e95ca3d81313d852aa4c0fe43a61696cc78a7e83b2afd57496b674c4c2538f81; review bbb2d292312b62e2b73f94967dfbdf474b4c88651ab2255ef19b1084f61f6092; disposition 76b38c121adf51ed698765aae5495c6634c149cb5747c595a0f09266ca32878d.

E040 report SHA256 a63613d97eb065ac23cbc598ef5798a47061173308e3f42bef0f952b1ab3fc1d; review 50355aaa67a43edc2cf249c96b9d40b38db00ab9c6090d1e48cc86658df6a01e; disposition 34dc574cf326cf2b7a4aa250986eaed2967bb39a1b02c29ac13ca5892415ed6e.
