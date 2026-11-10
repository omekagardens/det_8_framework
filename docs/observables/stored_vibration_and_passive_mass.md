# What phase-tagged weighing can identify about stored vibration

**DET Energy Research · Conditional inverse for a differential passive-mass reading**

A crossing and two turning points in the mixed quadratic–quartic oscillator determine three combinations of passive-response coefficients. The support contribution leaves one parameter free, even if the mechanical energy and the entire weighing trace are known exactly. Independently establishing that the quadratic and quartic elastic energies have the same passive response fixes that parameter. In the worked record every reading equals the true energy. It identifies unit intrinsic responses under the shared elastic-response premise and also admits strictly positive, unequal intrinsic responses when that premise is released.

## Mechanical input and complete record

CL075 establishes when a network’s vibrational energy is observable. On its chain, three signed boundary displacements determine the initial velocity and energy. On its diamond, the same measurements permit every energy from a computable minimum upward. A squared middle-pair displacement at the first sample determines the missing energy even though a middle-handle exchange can remain invisible. Its original 60 marked histories, including the inactive symbol with no assigned energy, belong to that network. E58 uses a separately prepared, horizontal, one-coordinate oscillator. Neither its quartic elasticity nor its gravitational readout comes from CL075.

Use calibrated positive inertial mass $m$, stiffness $k$, and quartic coefficient $b>0$ in the mixed arm. Put $b=0$ in the harmonic arm. Register the support origin $q=0$, momentum $p$, phase, and a common physical time convention. On each conservative post-preparation interval,
$$
 K=p^2/(2m),\qquad V_2=kq^2/2,\qquad V_4=bq^4/4,\qquad
 E=K+V_2+V_4,\qquad
 \dot q=p/m,\quad \dot p=-kq-bq^3 .
$$

Thus $\dot E=0$ on each interval. The independent weighing channel reports the signed differential value $Y=c^2(P-P_{\rm blank})$ in the same energy units. The supplied instantaneous response is
$$
 Y=\gamma_K K+\gamma_2V_2+\gamma_4V_4+\eta D,\qquad D=\frac{d(qp)}{dt}.
$$

All four coefficients are finite real numbers. The same fixture, calibration and coefficients transfer across the specified preparations and arms. A single unknown constant $\eta$ multiplies the registered support term. A blank subtracts the baseline but gives no information about $\eta$, since $D=0$ at rest at the origin.

Let $E_H>0$ be the known common energy at the harmonic crossing and turn, and $E_X>0$ the mixed crossing energy. For the two mixed turns set $U=kA^2/2>0,\ V=bA^4/4>0$, with $A>0$. Retain the following labelled readings, each a finite point value conditional on its actual preparation and phase.

| Setting | $K$ | $V_2$ | $V_4$ | Signed reading |
| --- | ---: | ---: | ---: | --- |
| Matched equilibrium blank | 0 | 0 | 0 | $Y_0=0$ |
| Harmonic central crossing | $E_H$ | 0 | 0 | $Y_{HC}$ |
| Harmonic turn | 0 | $E_H$ | 0 | $Y_{HT}$ |
| Mixed central crossing | $E_X$ | 0 | 0 | $Y_X$ |
| Mixed turn at $A$ | 0 | $U$ | $V$ | $Y_A$ |
| Mixed turn at $2A$ | 0 | $4U$ | $16V$ | $Y_{2A}$ |

The mixed turns have their own total energies $U+V$ and $4U+16V$. The model calls for separate turning preparations. A change of the sign of the crossing momentum or a choice of the opposite turn of the same amplitude preserves that row’s energy terms and reading. Retain any registered signs. With any specified setting weights, the joint law is the setting weight times its conditional point mass. The control specifies ideal success at every setting. It supplies no sampling frequencies or native histories for this oscillator. A nonzero differential blank, a failed phase or energy registration, or an inconsistent stated preparation invalidates this observation model.

## The support term on a conservative trajectory

The product rule gives the instantaneous identity
$$
 D=p\dot q+q\dot p=2K-2V_2-4V_4 .
$$

It has energy units and can have either sign. This identity applies before any time averaging. The three observable coefficients are therefore
$$
 \alpha=\gamma_K+2\eta,\qquad \beta=\gamma_2-2\eta,\qquad
 \delta=\gamma_4-4\eta,\qquad
 Y=\alpha K+\beta V_2+\delta V_4 .
$$

Replacing $(\gamma_K,\gamma_2,\gamma_4,\eta)$ by
$$
 (\gamma_K-2t,\ \gamma_2+2t,\ \gamma_4+4t,\ \eta+t)
 \qquad (t\in\mathbb R)
$$

leaves $Y$ unchanged at every $(q,p)$ governed by the stated dynamics. In particular, an apparent kinetic-to-elastic contrast can be produced by a change in the assigned support contribution. The readout does not feed back on $q,p$ in this model.

## The harmonic observations

Form $a_H=Y_{HC}/E_H,\ b_H=Y_{HT}/E_H$. These determine $\alpha=a_H,\ \beta=b_H$. Every finite such pair with a valid blank and preparations is attainable. The exact parameter set in the order $(\gamma_K,\gamma_2,\gamma_4,\eta)$ is
$$
 \{(a_H-2t,\ b_H+2t,\ z,\ t):t,z\in\mathbb R\}.
$$

The quartic response $z$ is unobserved. With a shared elastic coefficient one sets $z=b_H+2t$, leaving $t$ free. A known support coefficient fixes the kinetic and quadratic responses. The harmonic arm still needs a separate premise to assign a quartic response.

The harmonic data determine $\gamma_K+\gamma_2=a_H+b_H$. Equal kinetic and quadratic responses are always compatible, at $t=(a_H-b_H)/4$ and common response $(a_H+b_H)/2$. Unequal responses are also compatible with the same two readings. Unit kinetic and quadratic responses are compatible precisely if $a_H+b_H=2$, with $t=(a_H-1)/2$. A unit quartic response can then be assigned but does not enter either observation. Equal readings at matched energies therefore identify $\alpha=\beta$. They do not identify intrinsic equality or normalize the passive scale.

## Mixed observations and the exact joint inverse

The mixed crossing gives $\alpha=Y_X/E_X$. At the two turns,
$$
 \begin{pmatrix}Y_A\\Y_{2A}\end{pmatrix}
 =\begin{pmatrix}U&V\\4U&16V\end{pmatrix}
   \begin{pmatrix}\beta\\\delta\end{pmatrix}.
$$

The determinant is $12UV>0$, so the measured combinations are uniquely
$$
 \boxed{\quad
 \alpha=\frac{Y_X}{E_X},\qquad \beta=\frac{16Y_A-Y_{2A}}{12U},\qquad
 \delta=\frac{Y_{2A}-4Y_A}{12V}.\quad}
$$

The independent powers of amplitude give the separation. Repeating the same turn would give a proportional row, and $b=0$ removes the quartic column. Neither degeneracy occurs in the specified mixed design.

The mixed settings alone, with the matched blank and valid energy registrations, admit any finite signed triple of readings. There is no sign restriction on differential response coefficients. If the harmonic rows are also present, require **both** $Y_{HC}=E_H\alpha$ and $Y_{HT}=E_H\beta$. These are direct transfer checks. A failure leaves the combined record with no realization under one common set of coefficients. On a consistent record the entire solution is the line
$$
 \boxed{\quad(\gamma_K,\gamma_2,\gamma_4,\eta)
       =(\alpha-2t,\ \beta+2t,\ \delta+4t,\ t),\qquad t\in\mathbb R.\quad}
$$

This is necessary by the three independent measured combinations. For sufficiency choose any $t$ on the line. Keep the same calibrated mechanics in all candidates. The harmonic phases are realized at $q=0,\ |p|=\sqrt{2mE_H}$ and at $p=0,\ |q|=\sqrt{2E_H/k}$ on the same energy orbit. The mixed crossing is realized at $q=0,\ |p|=\sqrt{2mE_X}$, and the two registered turns at $p=0,\ q=A,2A$ in their respective preparations. Substitution reproduces all retained readings, including the zero blank. A common absolute passive baseline cancels in the differential record. If positive absolute passive masses at the finite tags are desired, any baseline exceeding $\max(0,\max_i[-Y_i/c^2])$ realizes them. The differential law fixes no baseline mass value. This gives every point of the line within the supplied model.

## What equality means in the two material models

**Independent elastic coefficients.** Each single pairwise equality can hold at one value of $t$. For $\gamma_K=\gamma_2,\ \gamma_K=\gamma_4,\ \gamma_2=\gamma_4$ those values are respectively $(\alpha-\beta)/4,\ (\alpha-\delta)/6,\ (\beta-\delta)/2$. Requiring equality of all three in one world gives the observable test
$$
 I=\alpha-3\beta+2\delta=0.
$$

Indeed $I=\gamma_K-3\gamma_2+2\gamma_4$ for every $t$. If $I\ne0$, the data exclude a common intrinsic response regardless of support. If $I=0$, exactly one point on the line has three equal responses, and unequal points remain. The common value at that point is $2\beta-\delta$. In particular the all-unit hypothesis is compatible precisely when $I=0$ **and** $2\beta-\delta=1$, equivalently $\alpha+\beta=2,\ \delta=2\beta-1$. Compatibility of the unit point still leaves the rest of the line.

**Independently registered shared elastic response.** Suppose the material law supplies $\gamma_2=\gamma_4=\gamma_V$ across both energy contributions and both turn preparations. Their effective difference then measures the support coefficient. The unique solution is
$$
 \boxed{\qquad
 \eta=(\beta-\delta)/2,\qquad
 \gamma_V=2\beta-\delta,\qquad
 \gamma_K=\alpha-\beta+\delta .\qquad}
$$

Every feasible mixed triple has exactly one such explanation. Consequently fitting these three readings cannot itself establish that the elastic responses are shared. Given that registration, $\gamma_K-\gamma_V=I$ is an identified physical-response contrast under the assumed law. Equality is decided by $I=0$, and the common response is unit-normalized exactly when it also satisfies $2\beta-\delta=1$. A unit intrinsic response can coexist with nonzero $\eta$, so a raw reading need not equal $E$ at each phase even in that case.

For independent elastic responses, an independently measured $\eta$, or one independently calibrated intrinsic coefficient, fixes the remaining scalar in the mixed inverse. More generally, an exact scalar linear calibration with weights $(l_K,l_2,l_4,l_\eta)$ fixes the ambiguity precisely if $-2l_K+2l_2+4l_4+l_\eta\ne0$. If the expression vanishes, the calibration checks an already determined combination and either agrees with the entire line or rejects it. This criterion explains why an independently established zero elastic contrast is sufficient, whereas a common fixture or known total mechanical energy alone is insufficient. Any further passive readings on exactly the same Hamiltonian obey the product-rule identity. Even full phase traces at more amplitudes, or their averages, preserve the line. On a complete periodic orbit $\langle D\rangle=0$ also follows from the return of $qp$. Averaging supplies no additional independent coefficient.

## Worked record with $Y=E$ at each tag

Keep $m,k,b,A,E_H,E_X$, the fixture, blank and all calibrations fixed. The six readings, in the table’s order, are
$$
 (0,\ E_H,\ E_H,\ E_X,\ U+V,\ 4U+16V).
$$

The mixed turn differences give $16Y_A-Y_{2A}=12U$ and $Y_{2A}-4Y_A=12V$. Thus $(\alpha,\beta,\delta)=(1,1,1)$ and both harmonic checks pass. The complete independent-coefficient solution is $(1-2t,\,1+2t,\,1+4t,\,t)$. Two realizations are

| Assignment | $\gamma_K$ | $\gamma_2$ | $\gamma_4$ | $\eta$ |
| --- | ---: | ---: | ---: | ---: |
| Unit intrinsic responses | 1 | 1 | 1 | 0 |
| Unequal positive intrinsic responses | $1/2$ | $3/2$ | $2$ | $1/4$ |

In the second realization the support contributes $K/2-V_2/2-V_4$. Adding the intrinsic contribution $K/2+3V_2/2+2V_4$ gives $Y=K+V_2+V_4$ pointwise. The same positive absolute passive baseline can be used in both realizations, with identical differential readings. In the shared-material model only the first row qualifies. It uniquely gives $\eta=0$ and $\gamma_K=\gamma_V=1$ for this record. In the harmonic arm alone, even the shared-material premise leaves $t$ free.

## Interpretation as a gravity comparison

Here $P$ is a passive coefficient in a separately calibrated weak external field. Interpreting $Y/E$ requires a calibrated signed differential weighing gain and zero, a matched reference in that field, known $c$, stable support transfer and an independently established mechanical energy scale. The phase assignments require the displacement origin, momentum and timing registration, a reproducible undamped preparation and an instantaneous readout with sufficient time resolution. Material matching concerns where deformation energy is stored and how that material couples to this channel. Attributing differences to kinetic or elastic response requires the same support calibration or registered elastic law across compared preparations. Mechanical identification of $E$ alone establishes none of these gravitational properties.

The accepted binding comparison also depends on how energy is distributed among materials and on a matched support ledger. The signed-lift result uses calibrated field and holder contrasts. Neither gives this oscillator's $\eta$. The closed radiation shell concerns the leading **active** mass of a static conserved source under supplied field equations. Its stress cancellation supplies no instantaneous passive law for this oscillator. CL076 studies spatial acceleration data from separate Newtonian source templates. A conventional oscillator given the same preparations, passive readout, support term and material information has exactly the same inverse.

A physical interpretation would have to account for preparation energy, support and fixture forces, controller and sensor disturbance, work, losses and restoration of both oscillator and reference. An ideal equilibrium blank removes a common offset but cannot calibrate dynamic support response. This calculation establishes a finite conditional attribution test. It supplies no active source mass, empirical equivalence test or DET-native energy unit.

## Scientific review

DET Energy Research supplied the derivation. DET Relational State Research independently checked the inverse, the full-trace counterexample and the conditions for identifying the intrinsic responses. The coordinator accepted this conditional result on 9 November 2026 HST.

- Control SHA-256: `87816781191b8213baf7be048ff6dc2721ab7d893466c7d6ada71db90bbfc456`.
- Author report SHA-256: `c46c9dac55468f022d2eda1f34c6f8c66b778fd67763fa5ee898820d90e51150`.
- Freeze SHA-256: `dd2b44a211c6aff58758530dfb450d2eb6fed794a4855c6b387ddb6ec3058be2`.
- Independent scientific review SHA-256: `fe7689ee51027ca5122a57a4fad7381953358e59ed2717d0d114d8e54bc85e56`.
