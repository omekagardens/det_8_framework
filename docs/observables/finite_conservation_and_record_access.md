# Finite conservation, additive quantities and record access

The independently reviewed GDM040 and NE042 results separate three questions: which state quantities a finite law conserves, which additional composition conventions select a total, and whether its committed records identify that total. The construction is an optional classical carrier. Its occupation labels, factorization, coefficients and access rules are supplied; neither physical mass nor an absolute native unit follows.

## Fixed two-birth model

Use the full simplex Delta4, including every mixed and boundary state, in order (00,10,01,11). The two binary coordinates are a source r and reservoir e. Define Q=(0,1,1,2), with Q=r+e. States are columns and operators act on the left. For every actual ideal S and both distinct committed bit marks b, use

    B_(S,b|C) = (q_C(S)/2) D(x_C,S),
    D(x) = diag(1,M(x),1),
    M(x) = [[3/4+x/2, 1/4-x/2],
            [1/4+x/2, 3/4-x/2]].

The empty parent has one ideal with (q,x)=(1,0). At a singleton, the empty ideal E has (2/3,1/8448), and full ideal F has (1/3,-1/4224). Both marks use the same operator but remain different outcomes. The horizon ends after two births. No coefficient, input domain, ideal or outcome is fitted after observation.

Each branch has six positive state-transition entries: four self-transitions and the two exchanges 10 to 01 and 01 to 10. The other ten entries are exactly zero. Its effect row is (q/2)(1,1+x,1-x,1), strictly positive on the simplex at the fixed coefficients. Branch probabilities use that effect; positive-branch posterior states divide the output by the full branch probability. The singleton weights satisfy sum q=1 and sum q*x=0, so the summed map is D(0), whose columns sum to one. The empty summed map is also D(0). Thus the complete trial is normalized; a single D(x) need not be column stochastic.

The uniform column w4=(1,1,1,1)/4 satisfies D(x)w4=w4 branchwise. Dependence on the parent/ideal geometry and absence of old-mark dependence give the declared covariance/locality. At the empty base the only incomparable two-birth exchange has, for every bit pair, the same unnormalized product (1/6)D(1/8448)D(0) on both sides. Complete terminal projections preserve that equality. These are finite-horizon facts, not an all-horizon growth law or a physical observer construction. The [record-process contract](../track_b/RECORD_PROCESS_CONTRACT.md) keeps commitment and access distinct.

## Conserved quantities and additional composition

For a fixed real state row f, write D_f=diag(f). Each entry of D_f B-B D_f is (f_j-f_i)B_ji. The positive middle exchanges require f10=f01, while the isolated sectors impose no further equality. Conversely that equality makes every supported entry vanish. Therefore the complete pathwise conserved class is

    f=(A,B,B,D),   A,B,D arbitrary real.

Constants are included but do not exhaust it. Full normalization plus this support conservation also gives unconditional expectation conservation. Conditional before/after comparison must use the SAME branch or history event; it does not equate a posterior mean with the unconditioned prior.

Additional subsystem additivity f(r,e)=u(r)+v(e) is equivalent to the rectangle equation f00+f11=f10+f01. Necessity follows by adding opposite corners. For sufficiency choose any k and set u0=k, v0=f00-k, u1=f10-f00+k, v1=f01-k; the rectangle equation supplies the remaining corner. Intersecting this condition with the conserved class yields

    f=A*1+tau*Q,
    u=(k,k+tau),  v=(A-k,A-k+tau),
    tau=B-A.

The split of a constant between subsystems remains arbitrary. An extra vacuum convention f00=0 sets A=0. Only after that convention does the orientation f10>0 require tau>0; before it, the condition is merely A+tau>0. Every positive magnitude remains possible. Additivity, zero convention, orientation and physical calibration are separate premises.

The pointwise square Q^2=(0,1,1,4) is conserved and has zero vacuum and positive single occupation, but violates the rectangle equation. It is one explicit control showing that conservation, vacuum and orientation alone do not derive the additive total or physical extensivity.

## What complete committed records reveal

Fix one natural birth-labelling convention. The record is exactly h=(s,b1,b2), with s=E or F and both bits retained. Initial source state i, intermediate state k and terminal residual state j are not observed. The complete history map is

    W_h=(q_s/4) diag(1,N(x_s),1),
    N(x)=M(x)M(0)
        =[[5/8+x/4, 3/8-x/4],
          [3/8+x/4, 5/8-x/4]].

For rho=(u,v,w,z), summing every terminal residual gives

    Pr_rho(h)=(q_s/4)[1+(x_s/2)(v-w)].

All eight histories and their complete denominators are retained. Summing both bits and both ideals yields one; sum q_s*x_s=0. The microscopic trial is rho_i (B1)_(k,i) (B2)_(j,k), including its zeros, summed over all latent i,k,j for the observed law. No preparation name is silently included in h, and no successful subset is selected.

Consider the two admitted preparations delta00 and delta11. Each of the four E histories has probability1/6 under either preparation; each of the four F histories has probability1/12. These are identical complete record laws, each summing to one. Yet the expectations of f=A*1+tau*Q are A and A+2tau. For every nonconstant additive charge, tau is nonzero, so the expectations differ even if tau was fixed beforehand. Thus these committed records do not identify that charge expectation. Constants are trivially identifiable.

The separately supplied augmented observation (i,h,j) changes the access contract. For delta00 only i=j=00 cells have nonzero weight q_s/4; for delta11 only i=j=11 cells do. Terminal basis access alone evaluates a chosen f_j, and pathwise conservation with full normalization gives E[f_j]=f*rho. This is population access under a stronger stipulated observation, not a derived detector, finite-sample guarantee, event-resolved transfer count or calibrated unit. It does not make residual inspection equivalent to ordinary reading of committed marks.

## Use and limits

The reusable dependency is: transition support fixes a conserved class; extra composition fixes an affine Q family; zero and orientation select a positive ray; the observation contract decides whether its expectation is identifiable. No step supplies the next one automatically. The [native mass mapping inventory](../coordination/NATIVE_MASS_MAPPING.md) separates such conditional mathematics from physical correspondence. The [response-and-scale result](finite_branching_response_and_scale.md) concerns a different model; its gain transformation is not transferred into this carrier.

Physical preparation, readout, disturbance, failures, controller/reset cost and dimensional calibration remain unprovided. A future explicitly modelled observer would need its own prospective design, complete consistency proof and independent review. This note adopts no such extension, no empirical run and no physical energy, mass, time, action, work store or native unit. Earlier incomplete procedural records are not retroactively qualified by the accepted proof and review.

## Reviewed source identity

GDM040 author report SHA256 16b71a6d354e347a34e638ccf0226d077d1cf8ffc18e95a7b55f3700011348db; distinct proof review 1db97fb8f90811fe1782c5ca319fc544638d808b60960874372a09c2f840273e; coordinator disposition f6268fede4b995bd96af94e5c9e74a9535c0fb504ae87b02e57896ad5a191b6e.

NE042 author report SHA256 7d4b8d9632f1486782aabc0372d0f31a27d931150b6cc4348db9b88332ad3cac; distinct proof review c1bec43c76a71778a61f0e843807035e628178c87bee356a7bf199107e616030; coordinator disposition 2eafe581b9785b8115459a9d5af6241f0c2cc8100e5dc33c8241244d63f82863. These identities locate exact internal reviewed versions; they are not substitutes for the definitions and arguments above or independent physical evidence.
