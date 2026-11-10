# Redshifted compact mass from two images in constant shear

**Result.** On compatible observations with unequal image radii, the two resolved angular vectors and their signed delay uniquely determine the redshifted point mass, despite unknown constant convergence, shear, source position and time-distance coefficient. The inner image is necessarily later in the stated positive-definite background. Equal radii force zero delay and do not identify the mass. No flux, parity measurement or complete-image census is used.

This is a conditional analytic inference in the supplied single-plane lens. It does not derive lens dynamics, qualify observations or establish DET-native mass units.

The point-mass potential and constant shear are supplied. The timing-to-mass calibration uses the compact logarithmic component and excludes external sheet or shear matter. [An and Evans, §§2 and 7](https://arxiv.org/abs/astro-ph/0601457v2) · [Circular timing calibration](two_lensed_images_and_central_mass.md)

## Eliminate the quadratic background and source

Use exactly the supplied potential
$$
 \phi(x)=\tfrac12x^{\mathsf T}Bx-y\cdot x-A\log(|x|/r_0)+C,
 \qquad A>0,\quad B=B^{\mathsf T}>0.
$$
The two distinct nonzero stationary exterior images have radii r_j=|x_j| and obey
$$
 Bx_j-y=A\,x_j/r_j^2.
$$
Subtracting gives
$$
 B(x_2-x_1)=A(x_2/r_2^2-x_1/r_1^2). \tag{1}
$$
At either stationary point, y·x_j=x_jᵀBx_j−A, so
$$
 \phi(x_j)=-\tfrac12x_j^{\mathsf T}Bx_j
              +A-A\log(r_j/r_0)+C.
$$
Symmetry and constancy of B now give
$$
 x_2^{\mathsf T}Bx_2-x_1^{\mathsf T}Bx_1
 =(x_2+x_1)^{\mathsf T}B(x_2-x_1)
 =A(x_1\cdot x_2)(r_2^{-2}-r_1^{-2}).
$$
The self terms cancel in the last step. Consequently the measured signed delay satisfies
$$
 \frac{t_2-t_1}{TA}
 =\frac{x_1\cdot x_2}{2}(r_1^{-2}-r_2^{-2})
       -\log(r_2/r_1). \tag{2}
$$
Thus the source vector, both shear components, convergence, reference radius and common potential zero have disappeared. No circular alignment has been assumed.

For unequal radii, label the inner and outer images i,o and put
$$
 R=r_o/r_i>1,\quad \chi=\frac{x_i\cdot x_o}{r_i r_o},
 \quad
 D(R,\chi)=\log R-\tfrac{\chi}{2}(R-R^{-1}).
$$
Then
$$
 \Delta t:=t_i-t_o=TA\,D(R,\chi). \tag{3}
$$
The sign of the original tagged t2−t1 must be converted consistently when ordering by radius. It is not replaced by an unregistered absolute delay.

## Why the coefficient cannot vanish on feasible unequal-radius data

Let v=x_o−x_i and w=x_o/r_o²−x_i/r_i². Equation (1) and B>0 imply
$$
 0<v^{\mathsf T}Bv=A\,v\cdot w,\quad
 v\cdot w=2-\chi(R+R^{-1}).
$$
Hence every compatible unequal-radius pair obeys
$$
 \chi<\frac{2}{R+R^{-1}}.
$$
Writing η=log R>0, this is χ<sech η. Since D=η−χ sinh η,
$$
 D>\eta-\tanh\eta>0. \tag{4}
$$
The last strict inequality follows from zero value at η=0 and derivative tanh²η>0 for η>0. Positive definiteness, not an assumed parity or source-axis geometry, fixes the sign.

Thus the inner image is later. An unequal-radius record with Δt≤0 is incompatible with this stipulated A>0,T>0,B>0 model. Equation (4) also excludes an accidental zero coefficient at any feasible unequal-radius pair. The optional physical nonnegative-sheet condition tr B≤2 does not weaken this conclusion; it is not needed for the proof.

Using the supplied TA calibration gives the unique mass observable
$$
 \boxed{\displaystyle
 M_z=(1+z)M=\frac{c^3}{4G}\,
       \frac{\Delta t}
       {\log(r_o/r_i)-\frac{x_i\cdot x_o}{2}
                         (r_i^{-2}-r_o^{-2})}.} \tag{5}
$$
This identifies the redshifted compact point mass on compatible exact data. It requires no separate measurement of the constant shear or convergence and no independent distance coefficient T, source location, flux ratio, parity or other-image census.

As a convention check, antipodal images have χ=−1, and D becomes log R+(R−R⁻¹)/2, exactly the accepted circular delay factor. For noncollinear images the dot product must be retained; inserting that circular factor would change the problem.

The inference need not identify A,B,y or T separately. For example, simultaneous changes (B,y,A,T)→(ρB,ρy,ρA,T/ρ) preserve stationarity and the measured delay, with TA unchanged. A nonempty range of positive ρ preserves the optional trace restriction. Thus elimination of the background nuisance from M_z is not a reconstruction of the background.

## Equal-radius exceptional record and a physical witness

When r1=r2, equation (2) gives φ(x2)−φ(x1)=0 for every compatible model. Therefore:

- equal radii and a nonzero signed delay reject this model;
- equal radii and zero delay do not identify M_z.

The ambiguity is not confined to a centred source, an Einstein ring or critical images. Choose one small positive angular scale θ0 and record
$$
 x_1=\theta_0(1,1),\qquad x_2=\theta_0(-1,1),
 \qquad t_2-t_1=0.
$$
For α=1 or α=1/2, let
$$
 A_\alpha=\alpha\theta_0^2,\quad
 B_\alpha=\operatorname{diag}(\alpha/2,1),\quad
 y_\alpha=\theta_0(0,1-\alpha/2).
$$
Both image radii are √2 θ0 and
$$
 (B_\alpha-A_\alpha/r^2\,I)x_j
   =\theta_0(0,1-\alpha/2)=y_\alpha,
$$
so both images are stationary for the same nonzero source within each model. In both models B is positive definite and tr B=1+α/2≤2. In the standard notation B=(1−κ)I−Γ, their nonnegative convergences are κ=1/4 and 3/8; the corresponding constant shear matrices are diag(1/4,−1/4) and diag(3/8,−3/8).

The lens-map Jacobians at these images are
$$
 H_\alpha^\pm=B_\alpha-\frac{A_\alpha}{r^2}I
                +\frac{2A_\alpha}{r^4}x_jx_j^{\mathsf T}
  =\begin{pmatrix}\alpha/2&\pm\alpha/2\\
                   \pm\alpha/2&1\end{pmatrix}.
$$
Their determinants are (α/2)(1−α/2): 1/4 and 3/16. They are nonzero, so neither observed image is singular. Other images are allowed; their number, fluxes and delays are not part of this record.

Hold the same positive T0 in both models. The redshifted point masses are c³T0θ0²/(4G) and c³T0θ0²/(8G), differing by a factor of two while the entire retained record agrees. Even an independently held T would not remove this particular ambiguity without more information about the unknown background/source.

More generally, for any compatible equal-radius zero-delay model, scaling (B,y,A) by 0<ρ<1 with T held fixed preserves the positions, zero delay, B>0 and tr B≤2 where imposed, while changing TA. Thus the exception is intrinsically nonidentifying in this observation class, not just a defect of the displayed example.

## Exact identification versus sensitivity

The exceptional set is exact, but nearby inference is poorly conditioned. For fixed R,χ with exact astrometry, absolute delay uncertainty ε_t propagates to
$$
 |\delta M_z|\le\frac{c^3}{4G\,D(R,\chi)}\,\epsilon_t .
$$
This conditional timing amplification is exact because (5) is linear in delay. Astrometric, centre and model uncertainties require their own bounds; they are not covered by ε_t.

As R→1, D=η−χ sinh η→0. At fixed distinct angular direction χ<1, D=(1−χ)η+O(η³). The feasibility-only lower bound η−tanh η is itself asymptotic to η³/3. Thus exact nonvanishing away from equal radii supplies no positive uniform timing margin over all permitted records. No detector precision, finite-error mass interval with uncertain astrometry or empirical discrimination guarantee has been established.

## Required standards and interpretation

The dimensionless factor D uses only the radius ratio and relative Euclidean angle about the known compact centre. A common positive isotropic angular gain, rotation or reflection of the whole frame leaves both unchanged. Absolute angular scale is therefore unnecessary for M_z itself, although reconstructing angular A or y would use it. A misregistered centre or anisotropic angular calibration is not canceled by this observation.

The dimensional mass still uses a calibrated signed observer-clock delay, common-emission association and the imported G,c and TA relation. An independent lens redshift is required to obtain M=M_z/(1+z). The unknown source position is not an independently observed standard. The result does not infer the compact centre from the two vectors; that centre is supplied.

A is the stipulated point-mass logarithmic coefficient. External sheet/shear matter is excluded from this compact mass. The data do not determine that background mass, prove the compact profile is a point, or import the earlier disk-fraction lower bounds. In an exterior-log model representing a distributed compact total, the same coefficient would measure that stipulated total, not an unresolved central subfraction. The present contract fixes the point lens and does not add a profile catalogue.

The result relies on a single plane, quasistatic geometric optics, one constant symmetric positive-definite quadratic background and two stationary exterior images of the same emission. It is a mass-registration result conditional on those supplied physical correspondences. Two returned images are sufficient here without any assertion that exactly two rays exist or that a detector has completed a census. More general backgrounds, source structure and propagation/readout errors require a different registered model.

This is an external lens comparison, not a native gravitational field equation, a derivation of physical units or an energetic/quantum advantage. No data acquisition, empirical fit, simulation or apparatus is supplied. A matched comparison must receive the same centre, two-dimensional angular frame, timing, source association and model assumptions.
