# Eight orbital phases for the PSR J1738+0333 companion-delay design

**Decision.** Advance this grid to phase and precision qualification as a conditional companion-mass design. At eight equally spaced, independently registered phases it cancels the entire leading eccentricity correction that contaminated the five-phase contrast. Two components of the supplied propagation law survive. At the adopted J1738+0333 parameters they are −31.25 ns and +6.52 ns, and they separately constrain range and inclination in a neighborhood of that point. This result supplies neither calibrated observations nor an emitter mass.

## The projection

Take $\phi_j=j\pi/4$, $j=0,\ldots,7$, on one clock with known conjunction phase. Write each signed reading as the sum of $g_j=-2r\ln(1-s\sin\phi_j)$, an arbitrary linear combination of $1,\cos\phi,\sin\phi,\cos2\phi,\sin2\phi$, and a reading error. Here $r>0$ is the propagation range in seconds and $s=\sin i$ is dimensionless. All five nuisance coefficients are free. In particular both quadratures of the first-order eccentric Rømer delay belong to this space. The earlier design's illustrative −184 ns leakage from that correction motivates this change of grid. [Circular propagation and eccentricity terms, equations (6) and (9)](https://arxiv.org/pdf/1007.0933v1) · [Accepted five-phase screen](five_phase_timing_precision_for_psr_j1738.md)

For an eight-vector of readings $y$, the following three coordinates give one orthogonal projection.
$$
 C_3=\tfrac14\sum_j y_j\cos3\phi_j,\qquad
 S_3=\tfrac14\sum_j y_j\sin3\phi_j,\qquad
 C_4=\tfrac18\sum_j(-1)^j y_j .
$$
The projected vector has entries $C_3\cos3\phi_j+S_3\sin3\phi_j+C_4(-1)^j$. The identity $\sum_j e^{ik\phi_j}=0$ unless $8\mid k$, when the sum is 8, proves orthogonality to every nuisance column. The squared lengths of the surviving columns are 4, 4 and 8. Together the five removed and three retained columns span all eight readings. The sine at frequency four vanishes at every sample.

**Finite-grid aliasing.** Frequencies differing by a multiple of eight agree on all eight phases. Reflection of frequency reverses the sine sign and preserves the cosine. For example, a fifth sine harmonic contributes the negative of its coefficient to $S_3$, and a twelfth cosine harmonic contributes its coefficient to $C_4$. The following expressions evaluate the full sampled logarithm, so include aliases of all its harmonics. An independent source of higher harmonics can occupy those same coordinates.

## Two propagation coordinates and one local rank test

For the supplied signal alone, $C_3=0$. Reflection $\phi\mapsto\pi-\phi$ pairs equal values of the signal with opposite values of $\cos3\phi$. Thus $C_3$ is a model consistency check. A zero value there cannot exclude contamination in the other two coordinates.

Let $a=1/\sqrt2$. The sampled sines are $(0,a,1,a,0,-a,-1,-a)$. Summing the symmetric and antisymmetric log pairs in the projection gives
$$
 S_3=rA(s),\quad A(s)=\sqrt2\,\operatorname{atanh}(s/\sqrt2)-\operatorname{atanh}s,
 \qquad
 C_4=rB(s),\quad B(s)=\frac{2\ln(1-s^2/2)-\ln(1-s^2)}4.
$$
Use $r_*=0.8915\,\mu\mathrm{s}$ and $s_*=0.53877$, fixed from optical and radio inferences in Paper II, Table 1(b). These are conditional design inputs. The exact grid expressions give $S_3=-31.2476$ ns, $C_4=+6.51864$ ns. Either is a test of departure from the declared nuisance space. A single nonzero amplitude leaves a trade between the two unknowns $r,s$. [Radio paper, §2.4 and Table 1(b)](https://arxiv.org/pdf/1205.1450v1) · [Optical paper, §§4.2, 4.7 and Table 2](https://arxiv.org/pdf/1204.3948v3)

With rows $(S_3,C_4)$ and columns $(r,s)$, the Jacobian is
$$
 \begin{pmatrix} A&rA'\\ B&rB'\end{pmatrix},\qquad
 A'=-\frac{s^2}{2(1-s^2/2)(1-s^2)},\qquad B'=-sA'/2 .
$$
At the design point the rows are $(-0.03505058,-0.21326037\,\mu\mathrm{s})$ and $(0.00731199,0.05744914\,\mu\mathrm{s})$. The determinant is approximately $-0.000454268\,\mu\mathrm{s}$. Its sign can also be checked without rounding since $A(0)=B(0)=0$, $A'<0$ on $(0,s_*]$, and $(B+sA/2)'=A/2$. Hence $B(s_*)+s_*A(s_*)/2=\frac12\int_0^{s_*}A(t)\,dt<0$. The determinant $-r_*A'(s_*)[B(s_*)+s_*A(s_*)/2]$ is strictly negative. The inverse function theorem gives local identification from exact coordinates at this point. Inferring $M_c=c^3r/G$ additionally uses the supplied GR conversion. Local invertibility supplies no finite-error mass accuracy.

## One attainable error bound

Choose the smaller nominal coordinate, $C_4$. If every signed reading has error $|e_j|\le\delta$, then
$$
 |\widehat C_4-C_4|=\left|\tfrac18\sum_{j=0}^7(-1)^j e_j\right|\le\delta .
$$
The alternating errors $e_j=(-1)^j\delta$ attain equality. Thus a measured $+6.51864$ ns would exclude a true zero in this coordinate under a certified per-reading bound strictly below $6.51864$ ns. This is an observed-value criterion for the one contrast. An inference on both physical parameters also needs joint errors on the two surviving amplitudes.

**Physical boundary.** The cancellation requires the prescribed grid. Actual epochs, finite exposures, phase origin, clock and dispersion corrections must support the signed readings at those phases. A source of third or higher harmonics would need an independent constraint before attributing the residuals to propagation. The earlier public record screen did not establish those inputs. At $s=0$ the logarithm vanishes for every $r$, so the grid gives no face-on companion-mass information. The free fundamental includes the geometric orbital amplitude and its stable lag. Projecting it away leaves the emitter mass ambiguous without an independent lag or geometric-amplitude calibration. [Accepted timing comparison](five_pulse_arrivals_and_binary_masses.md)
