# Can weight and tidal torque establish local passive-to-inertial mass proportionality?

A uniform-field force measures the total passive mass of this seven-site body. The tidal torque at the original radius measures the differences between its three axis-pair coefficients. Together they can exclude a common positive passive-to-inertial ratio. Whenever they admit that ratio, they also admit unequal local ratios. Two signed torque readings after moving one labelled pair to twice its radius determine all seven sites’ coefficients, including zero responses.

## The equal-radius record

Use the registered right-handed axes and origin. Write $p_0$ for the centre’s passive coefficient and $p_x,p_y,p_z$ for the coefficient of **one site** in each opposed pair at radius $a>0$. All four are finite and nonnegative. The corresponding $i_0,i_x,i_y,i_z$ are positive inertial masses calibrated on this body. Retain both signed force readings $f_\pm$ and both complete torque vectors $\boldsymbol\tau_\pm$. All observed entries must be finite. The signs label the applied field. Each instrument reads the external force or torque on the body in its fixed coordinate convention.

In the uniform fields $\pm g\,\mathbf e_x$, add the seven site forces. The force bias $b_f$ and total passive mass $S$ obey
$$
 f_\pm=b_f\pm gS,\qquad S=p_0+2(p_x+p_y+p_z),\qquad
 S=\frac{f_+-f_-}{2g},\qquad b_f=\frac{f_++f_-}{2}.
$$
The supplied gradient $H$ has zero diagonal and all six off-diagonal entries equal to $h>0$ in the registered axes. In the field $+H\mathbf r$, each site contributes $p\,\mathbf r\times H\mathbf r$. The two sites of a pair give equal moments. In units of $2a^2h$, the $x$ pair contributes $p_x(0,-1,1)$, the $y$ pair contributes $p_y(1,0,-1)$, and the $z$ pair contributes $p_z(-1,1,0)$. The centre has zero lever arm. The complete torque record therefore gives
$$
 \mathbf d=\frac{\boldsymbol\tau_+-\boldsymbol\tau_-}{4a^2h}
 =(p_y-p_z,\ p_z-p_x,\ p_x-p_y),\qquad
 \mathbf b_\tau=\frac{\boldsymbol\tau_++\boldsymbol\tau_-}{2}.
$$
Each raw torque is $\mathbf b_\tau\pm 2a^2h\,\mathbf d$. Only the field-odd part carries this signal. The vector midpoint is unrestricted.

Set $t=p_x$. The sharp set of passive masses consistent with the readings is
$$
 (p_0,p_x,p_y,p_z)
  =(S-6t+2(d_z-d_y),\ t,\ t-d_z,\ t+d_y),\qquad
 L=\max(0,d_z,-d_y)\le t\le U=\frac{S+2(d_z-d_y)}6 .
$$
The original record is feasible exactly when $S\ge0$, $d_x+d_y+d_z=0$, and $L\le U$. The two independent differences and the total give the displayed vector. Its four nonnegativity constraints give exactly the closed interval. Conversely, substituting any $t$ in this interval and the measured midpoints reproduces both original forces and every signed torque component.

At $L$ at least one outer pair has zero response. At $U$ the centre has zero response. A singleton is admissible and satisfies both conditions. If $S=0$, feasibility requires $\mathbf d=0$ and all four coefficients vanish. If $S>0$ and $\mathbf d=0$, any equal outer coefficients $0\le t\le S/6$ fit, with centre coefficient $S-6t$. The raw readings themselves can have either sign because of the biases.

## What the rigid body can establish

Define the known total inertial mass $I=i_0+2(i_x+i_y+i_z)$ and $\mathbf d^i=(i_y-i_z,i_z-i_x,i_x-i_y)$. On a feasible record, positive sitewise proportionality is compatible exactly when
$$
 S>0,\qquad \mathbf d=(S/I)\,\mathbf d^i .
$$
The total fixes the sole candidate $\kappa=S/I$, and $p_j=\kappa i_j$ then reconstructs every reading. Failure of this test on a feasible record excludes every positive ratio. Failure of unrestricted feasibility rejects the stated measurement model.

Whenever proportionality is compatible, that candidate has all four coefficients strictly positive. For every sufficiently small nonzero mass $s$, the shift
$$
 (p_0,p_x,p_y,p_z)\longmapsto(p_0-6s,\ p_x+s,\ p_y+s,\ p_z+s)
$$
preserves positivity, $S$, and $\mathbf d$. It changes local ratios because $S$ has already fixed $\kappa$. Thus no feasible original record establishes positive proportionality, even with a calibrated bulk equality $S=I$.

The same freedom survives every rigid orientation and every conservative affine acceleration field $\mathbf u+G\mathbf r$, with $G=G^\mathsf T$. The passive first moment $\sum p\mathbf r$ vanishes by opposed-pair symmetry. The net force is $S\mathbf u$, and the uniform part contributes zero torque about the origin. Write $Q=\sum p\,\mathbf r\mathbf r^\mathsf T$. The gradient torque has components $\tau_i=\sum_{j,k,\ell}\epsilon_{ijk}G_{k\ell}Q_{j\ell}$, where $\epsilon$ is the alternating tensor. The shift adds $2a^2s$ times the identity to $Q$ in the body frame and after every rotation. Its torque increment vanishes because $\sum_{j,k}\epsilon_{ijk}G_{kj}=0$. This argument uses the symmetry of a gravitational potential gradient and the affine field law over the body. The original record already determines every mass combination that these rigid measurements can distinguish.

## The selective radial move

Extend the same $x$ pair to $\pm2a\,\mathbf e_x$, preserving all material labels and coefficients. Retain the two finite signed $z$-torques $\tau'_{\pm,z}$. The $x$-pair lever arm and the sampled acceleration each double. The $y$-pair term stays fixed, and the centre and $z$ pair give zero $z$-moment. Hence
$$
 d'_z=\frac{\tau'_{+,z}-\tau'_{-,z}}{4a^2h}=4p_x-p_y=d_z+3p_x,
 \qquad b'_z=\frac{\tau'_{+,z}+\tau'_{-,z}}2 .
$$
This midpoint may differ freely from the original torque midpoint. The added readings select $t_*=(d'_z-d_z)/3$. The full record is feasible exactly when the original checks hold and $L\le t_*\le U$, equivalently $d_z+3L\le d'_z\le d_z+3U$. Both endpoints are attained. Substitution of $t_*$ into the original vector gives the unique four coefficients and the midpoints give all biases. They reconstruct $\tau'_{\pm,z}=b'_z\pm2a^2h\,d'_z$ as well as the original record. For zero total response the added signed difference must also vanish.

On this feasible full record, a positive common ratio is established exactly when the original compatibility test holds and $t_*=(S/I)i_x$. Equivalently the added comparison is $d'_z=(S/I)(4i_x-i_y)$. Every other feasible full record excludes positive proportionality, including a fit with any zero coefficient. Unit proportionality additionally requires $S=I$ in a common calibrated mass convention.

**Two strictly positive worlds.** Give each individual site inertia $m>0$. In the order $(p_0,p_x,p_y,p_z)$, take world A to have $(m,m,m,m)$ and world B to have $(m/2,13m/12,13m/12,13m/12)$. Both give $S=I=7m$, identical $f_\pm=b_f\pm7mg$, and $\boldsymbol\tau_+=\boldsymbol\tau_-=\mathbf b_\tau$ at the original orientation for any shared biases. Only A has equal local ratios. The moved pair gives $d'_z=3m$ in A and $13m/4$ in B. A new common bias shifts both moved-shape readings together and preserves their distinguishing difference.

## Physical registrations and reach

The inverse uses calibrated positive $g,h,a$, signed force and torque gains, a torque origin, a common frame and the verified radius change. The affine field and its reversal must hold over both shapes out to $2a$. Force divided by acceleration and torque divided by $a^2h$ both have mass units. These two mass calibrations must agree to combine their readings. A common positive rescaling of all passive masses preserves the existence of a common ratio. Its numerical value and a comparison with one require calibration against the inertial mass unit.

Reading the result physically requires a matched fixture subtraction, stable biases within each reversal, the additive local force law, and negligible field-odd responses from supports, actuators and probes. Such a residual enters the same signed difference as a gravitational signal. Moving and holding the sites, generating and reversing the field, and calibrating the instruments are supplied operations with unmeasured costs. The proof uses static external loads. It requires neither angular motion nor a timing measurement.

CL077 calibrates inertia for its own registered rotor. E62 imports independent inertias for these seven sites. CL018 concerns a source-density determination from a tidal field, and CL078 concerns a separate spring and work store. Earlier clock, lift and mutual-force comparisons use other registrations and observables. Here the unknown is the passive response of one held body to a prescribed field. A conventional model with the same site law, measurements and registrations gives the same inverse. The comparison supplies no active source mass, native gravitational coefficient, or universal equivalence law.

## Scientific review

DET Energy Research supplied the derivation. A distinct reviewer verified the full interval of compatible masses, the ambiguity under rigid rotations and the inversion after the labelled pair moves. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `ef71d0cd60c42f8eb12f704219bd1164cff52ec8083290fc567c33a727984458`.
- Author report SHA-256: `037013bf5e80a1f6f512d7fcdba048e5075d18f45b19a0fc97fe8fb7fbd14357`.
- Author freeze SHA-256: `d326b86f95a6f9ea7cb8fe85793855ac31f7c860f73d02dddac023bbe13609f0`.
- Independent scientific review SHA-256: `32e27bb728427754102bc85ac8160de7767a62dd8e5970d053f7a1a1be2279dc`.
