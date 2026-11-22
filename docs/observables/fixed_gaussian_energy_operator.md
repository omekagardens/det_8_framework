# Fixed Gaussian energy operator: unique closure and spectral moments

The fixed Gaussian-smeared quadratic energy defined below is essentially self-adjoint on its specified compact-momentum, finite-particle core. Its unique self-adjoint closure has, in the original one-particle packet, exactly the mean and ordinary variance established by the [full-Fock energy-fluctuation result](fixed_full_fock_energy_fluctuation.md). This supplies one ideal mathematical spectral observable within the provisional integrated model. It does not identify a physical preparation, detector or measurement law.

The result is conditional on the supplied continuum field/Fock representation, geometry, frame, clock scale, action scale, vacuum prescription and fixed kernels. The earlier state-action and variance proofs are reused, with their assumptions and qualifications. The closure proof below concerns this one operator and domain; it does not assert a general smeared-stress theorem, positivity or semiboundedness of the full energy operator, or a self-adjoint Weyl-curvature observable.

## 1. Fixed model, packet and starting operator

Work in the symmetric Fock space
\[
\mathcal F_s\bigl(L^2(\mathbb R^3,d^3q)\bigr),
\]
with normalized symmetric-sector wavefunctions, normalized vacuum, the accepted canonical commutation relations, anti-linear annihilation and inner products anti-linear in their first argument. All momentum integrals below use Lebesgue measure in three dimensions. Orthogonal symmetrization is denoted by \(\operatorname{Sym}\).

The supplied positive constants are \(c,\tau,A_*,\kappa\). In the dimensional coordinates the accepted dispersion is \(\omega_k=c|k|\), and the sampling is
\[
F(t,x)=\frac{e^{-t^2/(2\tau^2)}}{\sqrt{2\pi}\tau}
       e^{-|x|^2/(2\ell^2)}.
\tag{1}
\]
The spatial Gaussian is unnormalized. The same vacuum normal ordering, center, width, bandwidth and common field cutoff convention as in the source result are retained. The parameter \(\ell\) is the accepted initial energy radius of that packet. The field normalization \(\kappa\) cancels from the fixed energy kernels; it has not been derived from DET. The temporal and spatial tails of (1) are noncompact and frame-specific.

Use the dimensionless momentum and supplied dimensional energy scale
\[
q=c\tau k,\qquad \alpha=\frac{5\pi}{4},\qquad
\epsilon=\frac{\pi}{16},\qquad
\lambda=\frac{\ell}{c\tau},\qquad E_0=\frac{A_*}{\tau}>0.
\tag{2}
\]
The accepted radius fixes
\[
\lambda^2=64+\frac4{5\pi^2}
\int_{-1}^{1}\frac{\cos^2(\pi y/2)}{1-y^2/400}\,dy>64.
\tag{3}
\]
The original real normalized one-particle wavefunction is
\[
g(q)=\frac{\cos[\pi(|q|-\alpha)/(2\epsilon)]}
           {\sqrt{4\pi\epsilon}\,|q|}
      1_{\{||q|-\alpha|<\epsilon\}}.
\tag{4}
\]
Its compact shell and unsmoothed shell-edge regularity remain unchanged. When used as a Fock vector, \(g\) occupies only the one-particle sector.

For \(r=|q|\), \(s=|p|\) and
\(\gamma=\lambda^3/[2(2\pi)^{3/2}]\), fix the real symmetric kernels
\[
n(q,p)=\gamma\sqrt{rs}(1+\widehat q\cdot\widehat p)
 e^{-[(r-s)^2+\lambda^2|q-p|^2]/2},
\]
\[
p_2(q,p)=-\gamma\sqrt{rs}(1+\widehat q\cdot\widehat p)
 e^{-[(r+s)^2+\lambda^2|q+p|^2]/2}.
\tag{5}
\]
Direction choices at zero momentum affect only null sets. There is no projection of either kernel onto the packet's shell. The subscript on \(p_2\) distinguishes the pair kernel from a momentum argument.

Let \(D_0\) be the union, over finite particle bounds \(M\) and finite \(R>0\), of the direct sums of sectors \(N=0,\ldots,M\) whose symmetric \(L^2\) wavefunctions are supported where every occupied \(|q_j|\le R\), extended by zero outside that set. Arbitrary correlated sector functions are allowed. No smoothness or tensor-product restriction is imposed. The vacuum and the original \(g\) lie in \(D_0\).

On this exact domain define, sectorwise,
\[
S_0=d\Gamma(n)+B(p_2),\qquad
C(p_2)=\iint p_2(q,p)a^\dagger(q)a^\dagger(p)\,dq\,dp,
\]
\[
A(p_2)=C(p_2)^*,\qquad
B(p_2)=\tfrac12\bigl(C(p_2)+A(p_2)\bigr).
\tag{6}
\]
The adjoint pairing in (6) is justified on the finite sectors below. The notation \(d\Gamma(n)\) initially means the sectorwise sum of the uncut number-kernel action; it assumes neither boundedness nor an independently self-adjoint realization of \(n\). The pair minus sign and factor \(1/2\) in (5)–(6) are part of the fixed operator.

The mathematical comparison operator is
\[
m(q)=1+|q|,\qquad N_{\rm part}=d\Gamma(1),\qquad
K=I+d\Gamma(m)\ge N_{\rm part}+I.
\tag{7}
\]
Here \(K\) is the maximal self-adjoint multiplication operator, with the direct-sum domain on which multiplication by \(1+\sum_jm(q_j)\) is square-integrable. It is not an additional physical Hamiltonian.

## 2. The comparison core and pair action

**Core property.** For a vector in \(D(K)\), truncate to particle sectors \(N\le M\), then multiply each occupied coordinate by \(1_{\{|q_j|\le R\}}\). These projections commute with \(K\). They converge strongly to the identity, and their \(K\)-images converge by dominated convergence applied to the square-integrable \(K\)-vector. Their ranges lie in \(D_0\). Thus \(D_0\) is a graph core for \(K\), and in particular is dense. This does not assert invariance of \(D_0\) under \(S_0\).

**Weighted pair integrability.** Set
\[
L=\|p_2\|_{\rm HS},\qquad
L_m=\|(m(q)+m(p))p_2(q,p)\|_{\rm HS}.
\tag{8}
\]
The accepted source establishes \(L<\infty\). Its fixed Gaussian kernel gives, for \(u=|q|\) and \(v=|p|\),
\[
|p_2(q,p)|^2\le4\gamma^2uv\,e^{-(u+v)^2}.
\tag{9}
\]
After multiplying by \((2+u+v)^2\) and the radial measures \(u^2du\,v^2dv\), the integrand is bounded by a finite polynomial times a product Gaussian, since \((u+v)^2\ge u^2+v^2\). Hence \(L_m<\infty\). No numerical value of either constant is needed.

**Pair norm and symmetry.** Orthogonal symmetrization is a contraction. The normalized symmetric-sector creation and contraction formulas give
\[
\|C(p_2)\psi_N\|\le L\sqrt{(N+1)(N+2)}\,\|\psi_N\|,
\]
\[
\|A(p_2)\psi_N\|\le L\sqrt{N(N-1)}\,\|\psi_N\|,
\tag{10}
\]
with the annihilation bound zero for \(N<2\). Hilbert–Schmidt contraction and the symmetric-sector inner products give the adjoint pairing and therefore symmetry of \(B(p_2)\) on \(D_0\). Each action sends this domain into Fock space, although pair-created tails need not have bounded momentum support.

Sum squared norms over the distinct output sectors and use \(N+2\le2(N+1)\). For \(\psi\in D_0\),
\[
\|C(p_2)\psi\|\le2L\|(N_{\rm part}+I)\psi\|,
\qquad
\|A(p_2)\psi\|\le L\|(N_{\rm part}+I)\psi\|,
\]
\[
\boxed{\|B(p_2)\psi\|\le\frac{3L}{2}\|K\psi\|.}
\tag{11}
\]

**Pair weak commutator.** Define \(b(q,p)=(m(q)+m(p))p_2(q,p)\). The weighted Hilbert–Schmidt estimate permits the \(K\)-weighted created pair; spectator weights are bounded on each input component of \(D_0\). Sectorwise contraction, or finite momentum truncation followed by the weighted \(L^2\) limit, gives
\[
\langle B(p_2)\psi,K\psi\rangle-
\langle K\psi,B(p_2)\psi\rangle
=-\tfrac12\langle\psi,[C(b)-A(b)]\psi\rangle.
\tag{12}
\]
The sign uses the anti-linear-first inner product. Only the modulus will be used. Writing \(a_N=\|\psi_N\|\),
\[
|\langle\psi,C(b)\psi\rangle|
\le L_m\sum_N\sqrt{(N+1)(N+2)}\,a_{N+2}a_N
\le L_m\sum_N(N+1)a_N^2.
\tag{13}
\]
For the second inequality, replace the square root by
\(\sqrt{(N+1)(N+3)}\) and apply Cauchy–Schwarz to the shifted sequences. The annihilation expectation is its complex conjugate, so the half-difference in (12) has the same bound. Since \(K\ge N_{\rm part}+I\),
\[
\boxed{
|\langle B(p_2)\psi,K\psi\rangle-
 \langle K\psi,B(p_2)\psi\rangle|
\le L_m\langle\psi,K\psi\rangle.}
\tag{14}
\]
The registered weak form itself requires only \(S_0\psi\) and \(K\psi\) in Fock space. It does not posit \(S_0\psi\in D(K)\); the extra weighted pair estimate justifies this particular pair calculation.

## 3. Uncut number action and uniform sector estimates

Define the normalized Gaussian
\[
G(z)=\frac{\lambda^3}{(2\pi)^{3/2}}
      e^{-\lambda^2|z|^2/2},
\qquad
C_n=\int\sqrt{1+|z|}\,G(z)\,d^3z\ge1,
\qquad
B_n=\int|z|G(z)\,d^3z<\infty.
\tag{15}
\]
These constants are finite Gaussian moments. The fixed kernel satisfies
\(|n(q,p)|\le\sqrt{rs}\,G(q-p)\). From \(r\le s+|q-p|\),
\[
\frac{\sqrt{rs}}{1+s}\le\sqrt{1+|q-p|}.
\]
Both absolute Schur integrals of the kernel \(n(q,p)/m(p)\) are bounded by \(C_n\). Thus it defines a bounded operator on \(L^2\), and, on bounded-support inputs,
\[
\boxed{\|nf\|\le C_n\|mf\|.}
\tag{16}
\]
This gives uncut \(L^2\) output; it does not make \(n\) itself bounded. Real kernel symmetry, compact supports of the two test functions and Cauchy–Schwarz justify the symmetric form. Coordinatewise application and density extend the action to arbitrary bounded-support \(L^2\) sector functions, including correlated ones.

The positive-contraction identity used for the uniform Fock bound is the source's equation (20):
\[
n=\sqrt r\,J\sqrt r,\qquad 0\le J\le I.
\tag{17}
\]
For completeness, its fixed-kernel construction is as follows. Convolution \(T\) by \(G\) has Fourier multiplier \(e^{-|x|^2/(2\lambda^2)}\), so \(0\le T\le I\). Its normalized Gaussian-time average under multiplication by \(e^{itr}\) is a positive contraction \(B_0\) with kernel \(e^{-(r-s)^2/2}G(q-p)\). For the real bounded direction multipliers \(M_i(q)=q_i/r\),
\[
J=\tfrac12\bigl(B_0+\sum_iM_iB_0M_i\bigr),\qquad
\sum_iM_i^2=I.
\]
This proves (17) as an operator-order statement, rather than inferring it from pointwise kernel order. In particular \(0\le n\le r\le m\) as forms on bounded-support inputs.

Let an \(N\)-particle \(\psi_N\) have every occupied momentum bounded by \(R\), and let \(P_R\) denote the one-coordinate ball projection. The diagonal terms in \(\|\sum_i n_i\psi_N\|^2\) obey (16). For \(i\ne j\), the unchanged compact coordinate on the opposite side of the inner product removes the output tail, giving
\[
\langle n_i\psi_N,n_j\psi_N\rangle
=\langle\psi_N,(P_RnP_R)_i(P_RnP_R)_j\psi_N\rangle.
\tag{18}
\]
Each compressed number operator is bounded positive on its ball, with
\(0\le P_RnP_R\le P_RmP_R\). The two operators in (18) act on distinct coordinates and commute. Tensor order therefore gives
\[
0\le\langle n_i\psi_N,n_j\psi_N\rangle
\le\langle\psi_N,m_im_j\psi_N\rangle.
\tag{19}
\]
The identities first hold on finite tensor sums and extend by bounded compression to every stated sector function. In particular each cross term is real. Combining the diagonal and cross terms and using \(C_n\ge1\),
\[
\Bigl\|\sum_i n_i\psi_N\Bigr\|^2
\le C_n^2\Bigl\|\sum_i m_i\psi_N\Bigr\|^2.
\]
Summing sector norms yields the bound, with constant independent of particle number,
\[
\boxed{\|d\Gamma(n)\psi\|\le C_n\|K\psi\|,
\qquad \psi\in D_0.}
\tag{20}
\]
No extra particle-number factor from a sum of coordinate norms is introduced. Number action preserves particle number; its symmetry on \(D_0\) follows from the same real-kernel and bounded-support argument.

The one-particle weak commutator has kernel \((s-r)n(q,p)\). Sandwiching it by \(m^{-1/2}\), using
\(\sqrt{rs}/\sqrt{(1+r)(1+s)}\le1\) and
\(|r-s|\le|q-p|\), gives the absolute majorant \(|q-p|G(q-p)\). Schur's bound is therefore
\[
|\langle nf,mf\rangle-\langle mf,nf\rangle|
\le B_n\langle f,mf\rangle.
\tag{21}
\]
This form on compact-support \(f\) does not require \(nf\in D(m)\). On \(D_0\), different-coordinate terms cancel by separate-coordinate symmetry and commutation. Extend (21) with identity on spectator variables and sum to obtain
\[
\boxed{
|\langle d\Gamma(n)\psi,K\psi\rangle-
 \langle K\psi,d\Gamma(n)\psi\rangle|
\le B_n\langle\psi,K\psi\rangle.}
\tag{22}
\]
Finite-sector truncation and coordinatewise density justify these operations. They do not assume invariance of the energy domain or a separately self-adjoint number operator.

## 4. Essential self-adjointness on the fixed core

Apply the operator-bound commutator criterion in **Reed and Simon, _Methods of Modern Mathematical Physics II_, Theorem X.37, pp. 197–198, equations X.59–X.60**. In the form used here, a symmetric operator on a core of a self-adjoint \(K\ge I\) is essentially self-adjoint there when its \(K\)-norm bound and weak commutator bound by the \(K\)-form hold throughout that core. This is the operator estimate version; a weaker form estimate is not a substitute, and no additional invariant-domain hypothesis is imposed. The original scientific review checked these specific primary theorem passages. [Primary book](https://www.astrosen.unam.mx/~aceves/Metodos/ebooks/reed_simon2.pdf)

All hypotheses now refer to the exact registered objects:

- Section 2 establishes that \(K\) is self-adjoint, \(K\ge I\), and \(D_0\) is its graph core.
- Sections 2–3 establish well-defined number and pair actions from every \(D_0\) vector into Fock space, and symmetry of their sum on precisely \(D_0\).
- Equations (11) and (20) imply
  \[
  \|S_0\psi\|\le(C_n+3L/2)\|K\psi\|.
  \tag{23}
  \]
- Equations (14) and (22) imply
  \[
  |\langle S_0\psi,K\psi\rangle-
    \langle K\psi,S_0\psi\rangle|
  \le(B_n+L_m)\langle\psi,K\psi\rangle
  =(B_n+L_m)\|K^{1/2}\psi\|^2.
  \tag{24}
  \]

The constants are finite and depend only on the fixed kernels. Theorem X.37 therefore gives essential self-adjointness of \(S_0\) on \(D_0\). Its graph closure is self-adjoint and is the unique self-adjoint extension of that starting restriction. With the supplied positive dimensional factor,
\[
\boxed{E=\overline{E_0S_0}=E_0\overline{S_0}.}
\tag{25}
\]
No alternative extension, domain, profile or subtraction is selected. The positivity of the number-channel comparison used above is not a positivity or semiboundedness claim for the complete number-plus-pair operator \(E\).

## 5. Original packet and dimensional spectral moments

The original compact-shell \(g\) lies in \(D_0\subset D(E)\). Pair annihilation vanishes on its one-particle sector, while the normalized creation convention retains the factor \(\sqrt{3/2}\):
\[
S_0g=\zeta_{\rm dim}
=(ng)\ \oplus\ \sqrt{\frac32}\operatorname{Sym}(p_2\otimes g).
\tag{26}
\]
The closure agrees with \(S_0\) on \(D_0\).

The accepted coordinate unitary
\[
Uf(q)=(c\tau)^{-3/2}f\bigl(q/(c\tau)\bigr)
\tag{27}
\]
takes the original dimensional packet \(h\) to \(g\). It transforms its number kernel to \(E_0n\) and its pair tensor under \(U\otimes U\) to \(E_0p_2\). The source's dimensional full-Fock state-action limit is
\[
\zeta_*=(Nh)\ \oplus\ \sqrt{\frac32}
\operatorname{Sym}(P\otimes h),
\]
where \(N,P\) are those dimensional source kernels. Consequently second quantization of the coordinate unitary gives
\[
\boxed{Eg=E_0\zeta_{\rm dim}=\Gamma(U)\zeta_*.}
\tag{28}
\]
Coordinate change does not divide dimensional energy by \(E_0\). Both sides of (28) retain the same energy scale; only the action of the dimensionless closure is \(\zeta_{\rm dim}\).

Let \(\nu_g\) be the normalized spectral probability measure of the self-adjoint \(E\) in \(g\). The membership \(g\in D(E)\) gives the finite spectral second moment
\[
\int x^2\,d\nu_g(x)=\|Eg\|^2=\|\zeta_*\|^2.
\tag{29}
\]
Cauchy–Schwarz gives absolute integrability of the first moment, and
\[
\int x\,d\nu_g(x)=\langle g,Eg\rangle=\mu_*.
\tag{30}
\]
This uses neither an assertion \(g\in D(E^2)\) nor an expression \(\langle g,E^2g\rangle\) that would require it.

To state the accepted moments explicitly, distinguish the scalar \(m_{\rm source}\) from the comparison multiplier \(m(q)=1+|q|\), and define
\[
\begin{aligned}
m_{\rm source}&=\iint g(q)n(q,p)g(p)\,dq\,dp,\\
I_N&=\int\left|\int n(q,p)g(p)\,dp\right|^2dq,\\
I_P&=\iint|p_2(q,p)|^2\,dq\,dp,\\
I_C&=\int\left|\int p_2(q,p)g(p)\,dp\right|^2dq.
\end{aligned}
\tag{31}
\]
Their convergence and the original full-Fock contractions are established in the accepted source. Equations (26)–(30) identify their dimensional spectral meaning:
\[
\mu_*=E_0m_{\rm source},\qquad
\boxed{\operatorname{Var}_{\nu_g}(x)=V_*
=E_0^2\bigl(I_N-m_{\rm source}^2+\tfrac12I_P+I_C\bigr).}
\tag{32}
\]
The ordinary vacuum-pair contribution \(I_P/2\) and stimulated contribution \(I_C\) are retained. Neither normal ordering the square, discarding the vacuum variance nor projecting onto a one-particle space is part of this result.

By exact reuse of the accepted mean and variance result,
\[
\mu_*>0,\qquad 0<\mathcal R_*:=\frac{V_*}{\mu_*^2}
<\frac{4691}{5184}<1.
\tag{33}
\]
This bound is not recomputed here. It is not the exact ratio, a sharpness claim or a statement that fluctuations are negligible. The complete spectral distribution of \(E\) has not been calculated.

## 6. Scope, provenance and limits

The proof discharges the fixed action/symmetry/core obligation, the uniform operator-norm and weak-commutator obligations, and the original-state dimensional spectral correspondence. It is an analytic result for the full Fock space, not a particle-number or numerical cutoff test. Finite sectors and momentum truncations establish the domain and limits used in the argument; the constants in (23)–(24) are uniform in particle number. No numerical integration, solver, simulation, empirical trial or new case is used.

The full-Fock energy-fluctuation article remains the accepted dependency for the original packet, dimensional field/kernels, state-action norm limit, integrals and strict variance bound. Its earlier restriction to a state-action diagnostic describes that earlier result. The present separately reviewed proof supplies the unique closure for the fixed \(S_0,D_0\); it does not amend the earlier proof or import a different operator. The supplied geometry/frame, field/Fock representation, vacuum subtraction, action scale \(A_*\) and clock scale \(\tau\) remain assumptions. The relation \(E_0=A_*/\tau\) is dimensional correspondence, not a derivation of native units, a finite physical clock, an action store or a work store.

This mathematical spectral measure does not certify a detector, physical measurement or preparation protocol, causal sampling, donor funding, native mass, or empirical applicability. The provisional integrated model remains provisional. No gravity or semiclassical adequacy follows from the energy variance bound, and the energy closure does not provide a self-adjoint limiting Weyl-curvature operator. Unavailable native attachments remain undefined; they are not assigned a vacuum or zero-noise value. No other profile, state, Gaussian, general stress smearing, full spectral law, positivity or semiboundedness is claimed.

The result received the original distinct scientific review by DET Energy Research and scoped coordinator acceptance. Author-side checks and assistance are distinct from that review. The fixed candidate core and estimate route were exposed during the preceding registered design, so the proof is not a blind first-exposure test. Prior interface-selection requirements marked **NOT MET**, the repeated-readout full-control-before-proof failure, and earlier mass adjudication, exposure and process-record qualifications remain material and unrepaired. The mathematical conclusion does not provide an unconditional certificate about hidden reasoning, every worker's chronology, or empirical prospectivity. The earlier capacity interruption left final saved-report checking unfinished; that checking and the original distinct review were subsequently completed. Administrative completion does not relabel earlier exposure or erase those order limits.

The exact identities underlying this exposition are:

| Record | Bytes | SHA-256 |
|---|---:|---|
| Fixed operator author CONTROL | 862173 | `c688151b05c86904b5dc3bfdec80a7066ecaa3e181daf49a8fa3341312640997` |
| Fixed operator author REPORT | 14222 | `f64bafecdb3a6784cec04f626b4fcf84ab9f0116a0ade43d385fd51a3dbe7e37` |
| Fixed operator author MANIFEST | 3036362 | `c6463b18ef003449fb0d41422faad25405a62879ac8bac496374cbd5494c58dd` |
| Original Energy REVIEW | 12221 | `65759a89c00a83b0b8d435d008dddf1d1957691ec0e8362c0a52ae26627c6191` |
| Original Energy review MANIFEST | 55923 | `0b9d53c23133981b5ba9693f971d6cb6c4659e9cb36862c119785ad6852df114` |
| Scoped operator disposition | 4391 | `ab8c0ee57ed6fbc62dc4cebccc34b2d728b66e7f528dcce3b2bdbe0e0b935721` |
| Published full-Fock fluctuation dependency | 19588 | `8810deda9b74701eb5580c07dec68307de8a91b2764683db10b46fd0b6b5194c` |

These hashes identify the reviewed versions; they are not independent scientific validation. The article preserves the admitted theorem and its assumptions rather than introducing a new claim or physical calibration.
