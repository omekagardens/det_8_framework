# Gravity and vorticity from an annular free surface

**Result.** For a compatible record, different signed tracer advances at the two radii determine the downward acceleration $g$, the axial fluid vorticity $2A$, the circulation contribution $2\pi B$ and the camera rate $W$. Equal advances force $B=0$ and admit every $g>0$. In that branch a flat surface identifies a stationary fluid and the camera rate. A curved surface identifies $A^2/g$ and $A-W$, leaving both signs of rigid rotation possible.

## What enters the surface and the tracer observations

Take $z$ upward and use the prescribed oriented inertial azimuth $\phi$. The homogeneous fluid of density $\rho>0$ occupies an annulus with slip boundaries. The preparation specifies the steady velocity $v_r=v_z=0,\ v_\phi=Ar+B/r$. Its angular profile has the functional form of Fitzpatrick's equation 10.36. The free-surface and observation equations below follow from the supplied inviscid dynamics and the material tracer and camera premises. [R. Fitzpatrick, *Taylor-Couette Flow*, eq. 10.36 (2016)](https://farside.ph.utexas.edu/teaching/336L/Fluid/node137.html)

A particle at fixed $r,z$ has $\dot\phi=v_\phi/r$. Its radial acceleration is $-v_\phi^2/r$ from the turning azimuthal unit vector. The azimuthal and vertical accelerations vanish. Inertial Euler balance with body acceleration $-g\mathbf e_z$ gives
$$
p_r=\rho\, v_\phi^2/r,\qquad p_\phi=0,\qquad p_z=-\rho g .
$$
On the surface $z=h(r)$, differentiation of $p(r,h(r))=p_{\rm atm}$ gives $g h'(r)=v_\phi^2/r$. Integrating from the sampled radius $R$ yields
$$
g[h(r)-h(R)]=\tfrac12 A^2(r^2-R^2)+2AB\ln(r/R)
                    +\tfrac12 B^2(R^{-2}-r^{-2}).
$$
A negative cross term is possible. The derivative remains a nonnegative square even across a change in the direction of fluid motion.

Use the calibrated radius and duration to define $x=r^2/R^2,\ a=AT,\ b=BT/R^2,\ w=WT,\ G=gT^2/R>0$, all dimensionless. The full shape relative to $R$ is
$$
\frac{h(r)-h(R)}{R}
=\frac{a^2}{2G}(x-1)+\frac{ab}{G}\ln x+\frac{b^2}{2G}(1-x^{-1}). \tag{1}
$$
Write $\alpha$ and $\beta$ for the signed, unwrapped tracer advances in radians relative to the camera at $R$ and $2R$, respectively. Inertial tracer and camera azimuths advance by $(A+B/r^2)T$ and $WT$, so
$$
\alpha=a-w+b,\qquad \beta=a-w+b/4 .
$$
The two angular readings are equivalent to
$$
b=\tfrac43(\alpha-\beta),\qquad c=\tfrac13(4\beta-\alpha)=a-w. \tag{2}
$$
The common camera contribution cancels in the first expression. These are direct advances over the stated exposure, including any whole windings.

## Finite feasibility test and all solutions

For the four finite heights in radial order define $d_j=(h_{j+1}-h_j)/R$ for $j=0,1,2$. The radii have $x=1,2,4,8$. Taking successive differences of (1) gives
$$
d_j=2^j P+L+2^{-j}Q,\qquad
P=\frac{a^2}{2G},\quad L=\frac{ab}{G}\ln 2,\quad Q=\frac{b^2}{4G}. \tag{3}
$$
For arbitrary height data put $e_0=d_1-d_0$, $e_1=d_2-d_1$. Equation (3) gives $e_0=P-Q/2$ and $e_1=2P-Q/4$. Their inverse, plus the first row of (3), is
$$
P=(2e_1-e_0)/3,\qquad Q=2(P-e_0),\qquad L=d_0-P-Q.
$$
Thus every triple of differences has exactly one coefficient triple. The complete compatibility conditions are
$$
P\ge0,\qquad Q\ge0,\qquad L^2=8(\ln 2)^2 P Q,\qquad
(Q=0)\ \Longleftrightarrow\ (b=0). \tag{4}
$$
Failing any condition gives an empty parameter family. For a passing record use the following solutions, with dimensioned quantities recovered as $g=GR/T^2,\ A=a/T,\ B=bR^2/T,\ W=w/T$.

1. **Unequal advances, $b\ne0$.** Then $Q>0$. The unique solution is
   $$
   G=b^2/(4Q),\qquad a=GL/(b\ln 2),\qquad w=a-c .
   $$
   These choices reproduce $Q$ and the signed $L$. The squared equality in (4) gives $a^2/(2G)=P$, so no sign ambiguity remains. If $P=0$, then $L=0$ and $a=0$. This pure circulation branch can measure $g$ even though the local axial vorticity vanishes. When $P>0$, the sign of $L/b$ fixes the sign of $A$, including counter-rotation of the two profile contributions.
2. **Equal advances, $b=0$, curved surface $P>0$.** Equations (3)–(4) give $Q=L=0$, so the heights vary linearly with $r^2$. For every $G>0$ and either sign take $a=\pm\sqrt{2GP}$ and $w=a-c$. This is the entire family. For example $(G,a,w)=(1,\sqrt{2P},\sqrt{2P}-c)$ and $(4,-2\sqrt{2P},-2\sqrt{2P}-c)$ give the very same six tags. Each has nonzero vorticity. The measured combinations are $A^2/g=2P/R$ and $A-W=c/T$.
3. **Equal advances, $b=0$, flat surface $P=0$.** Now $P=Q=L=0$, $a=0$, and $w=-c$ for every $G>0$. A stationary fluid can have any common tracer advance through choice of camera rate. Two parameter choices $G=1$ and $G=4$ with this same $w$ give the same heights and advances.

The model allows any finite camera rate as a preparation. Its possible values for a given record follow from $w=a-c$ and the three branches above. The axial vorticity in the fluid is $r^{-1}\partial_r(rv_\phi)=2A$. The full signed inertial circulation on an oriented ring of radius $r$ is $2\pi r v_\phi=2\pi A r^2+2\pi B$. The term $2\pi B$ is identified in every compatible record, including zero. The annulus excludes the axis, which permits a nonzero ring integral of the locally irrotational $B/r$ component.

## Realization and measurement scale

For any member of the listed families, set $h(R)=h_0$ in the reported height coordinates and extend $h$ by (1) throughout $R/\sqrt2\le r\le4R$. The inverse of (3) ensures that this single choice matches all four height tags. The compact annulus stays away from the origin, so $h$ is bounded. Place a horizontal bottom below its minimum using the available depth. Define the flow by the given azimuthal field and
$$
p(r,z)=p_{\rm atm}+\rho g\,[h(r)-z].
$$
This pressure has both Euler gradients and equals $p_{\rm atm}$ on the surface. The fluid is incompressible by axisymmetry and zero radial and vertical velocity. The velocity is tangent to the walls, bottom and free surface. From any allowed initial azimuth $\phi_0$, the paths are $r,z$ constant and $\phi(t)=\phi_0+(A+B/r^2)t$, including fixed particles when $A+B/r^2=0$. Observing the two labelled paths through a camera angle $\phi_{\rm cam,0}+Wt$ recovers both advances in (2). This constructs a steady realization for every passing branch.

Changing the common height zero translates the whole surface and the chosen vertical coordinates. A change of angular origin cancels from advances. Reversing the registration of angular sense negates $\alpha,\beta,a,b,c,w$ and the signed vorticity and circulations. The cross term $ab$, both squared terms, all heights, and $g$ are invariant. In physical units $A,W$ have dimension inverse time, $B$ and circulation have dimension area per time, and $g$ has dimension length per time squared. In the unequal-advance branch, the dimensionless output $G$ becomes an absolute local acceleration through the calibrated multiplier $R/T^2$. Its interpretation as gravity uses universal passive/inertial coupling, the prescribed uniform downward field, and the absence of translational acceleration of the observation axis and of other body forces.

## Synthetic sign-changing fixture

Take $a=-1,\ b=2,\ w=1/2,\ G=1$ and $h(R)=0$. Equation (1) gives $(h(r)-h(R))/R=(x-1)/2-2\ln x+2(1-1/x)$. In the specified order the six exact tags are
$$
(h_0,h_1,h_2,h_3)=R(0,\ 3/2-2\ln2,\ 3-4\ln2,\ 21/4-6\ln2),
\qquad (\alpha,\beta)=(1/2,-1).
$$
The inertial angular rates at the tracked rings are $+1/T$ and $-1/(2T)$, and the stationary ring is $r=\sqrt2 R$. At that ring $h'=0$ and the pressure and surface remain regular. From the heights,
$$
(d_0,d_1,d_2)=(3/2-2\ln2,\ 3/2-2\ln2,\ 9/4-2\ln2),
$$
so $e_0=0,\ e_1=3/4,\ P=1/2,\ Q=1,\ L=-2\ln2$. The angles give $b=2,\ c=-3/2$. The inverse yields $G=1,\ a=-1,\ w=1/2$, hence $g=R/T^2,\ A=-1/T,\ B=2R^2/T,\ W=1/(2T)$.

This is a conditional exact inverse for one prepared steady state and one exposure. The record appends four jointly calibrated surface labels and two material angle changes. Field dynamics, calibration, and assignment of the labels to fluid and camera are premises. The result concerns a local acceleration in supplied units. Profile preparation, stability, measurement precision, empirical verification, source mass and a native DET gravity scale lie outside the question.

## Direct gravity reading and frame registration

After checking compatibility, set $D=d_2-3d_1+2d_0$. When the advances differ, the local acceleration is $g=(R/T^2)(\alpha-\beta)^2/(3D)$. Assigning that acceleration to gravity requires a known vertical and an axis with zero translational acceleration. The rotating camera contributes the same offset to both tracer advances. Using the comparison requires the four heights and the two material tracers in the same registered frame. [Optical-ring frame comparison](rotating_optical_rings_mass_and_spin.md) · [Local tides and support](local_mass_from_tides_and_support.md)
