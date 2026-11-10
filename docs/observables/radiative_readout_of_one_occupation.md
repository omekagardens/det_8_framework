# Can a photon count the entire one-occupation mass sector?

**DET Energy Research · Finite result under the supplied free-recoil and unitary model**

One available outgoing mode gives a sharp click probability of **$1/2$ on the one-occupation mixture**, or **$2/7$ per native preparation**. Two orthogonal outgoing modes give **1 and $4/7$**, respectively. At full conversion a photon click counts membership in the sector on every trial. Even then, the photon can have the same density operator for both native labels. Their distinction can reside in the joint state of the photon and its recoiling daughter.

## Preparation and the energy ledger

After the two native births, $A=00,B=10,C=01,D=11$ have probabilities $(5,4,4,1)/14$ conditional on **each** complete marked history. $B,C$ have one occupation and the same registered rest mass $M_1>M_0>0$, where $M_0$ is the mass of $A$. Initially every carrier is at rest and the optical field is in vacuum. $A$ and $D$ are spectators on this preparation. The one-occupation probability is $p_1=8/14$. On that sector the input density operator is $I_2/2$. The terminal operation has no access to a history, external label copy, environment or extra mode.

Write $\lvert B\rangle,\lvert C\rangle$ for the two orthogonal carrier-at-rest, vacuum states, and $E$ for their span. The available emitted states are selected from
$$
 \lvert F_\sigma\rangle
 =\lvert A,-\sigma k\rangle_{\rm d}\otimes\lvert1_\sigma\rangle_{\gamma},
 \qquad \sigma\in\{+1,-1\}.
$$
Here $k>0$ is a **momentum**, the photon momentum is $\sigma k$, and its energy is $ck$. The daughter and photon momenta add to zero for each sign. In the parent rest frame energy conservation gives
$$
 M_1c^2=ck+\sqrt{M_0^2c^4+c^2k^2}.
$$
With $G=(M_1-M_0)c^2$ the released rest energy, the unique positive solution and its energy partition are
$$
 k=\frac{(M_1^2-M_0^2)c}{2M_1},\qquad
 \epsilon_\gamma=ck=G\,\frac{M_1+M_0}{2M_1},\qquad
 K_{\rm d}=G-\epsilon_\gamma=\frac{(M_1-M_0)^2c^2}{2M_1}>0 .
$$
Indeed the daughter total energy is $(M_1^2+M_0^2)c^2/(2M_1)>0$, which verifies the unsquared equation. Both signs share precisely this energy. The normalized discrete modes and availability of this exact $k$ are stipulated. In $E$ and in every emitted branch the total energy is $M_1c^2$, total momentum is zero, and $Q_{\rm carrier}+N_\gamma=1$. In particular the emitted branch has carrier occupation zero and photon number one. The native births conserve carrier occupation. The appended conversion is a new physical interface.

## Dimension bound and its reverse

Let $F$ be the span of the available emitted states and $r=\dim F$, either 1 or 2. The model grants a fixed unitary $U$ on $E\oplus F$ and identity on spectators. It acts within the common total four-momentum and count block. An ideal click is projection onto $F$, equivalently one photon on these outputs. The input-sector effect for a click is $T^\dagger T$, with $T=\Pi_F U|_E$. Since $U$ is unitary, $0\le T^\dagger T\le I_E$ and its rank is at most $\min(2,r)$. Hence
$$
 p({\rm click}\mid Q=1)=\tfrac12{\rm tr}(T^\dagger T)
       \le\frac{\min(2,r)}{2},\qquad
 p({\rm click})=p_1\,p({\rm click}\mid Q=1).
$$
These formulas also hold conditional on any fixed native history. Every one-occupation state emits with certainty exactly when $T^\dagger T=I_E$. This requires $r\ge2$ because two orthogonal inputs must have two orthogonal outputs. Here each direction contributes exactly one joint photon–daughter output because the daughter label and its recoil momentum are fixed. The constructions below attain the trace bounds and establish sufficiency at $r=2$.

Reversibility also constrains absorption into $E$. Write $L=\Pi_EU|_E$, $S=\Pi_EU|_F$. The two unitarity identities $L^\dagger L+T^\dagger T=I_E$ and $LL^\dagger+SS^\dagger=I_E$ give
$$
 {\rm tr}(T^\dagger T)={\rm tr}(S^\dagger S).
$$
Thus for the same $U$, twice the forward probability on the uniform input in $E$ equals $r$ times the reverse-direction probability on the uniform input in $F$. For an individual transition $i\to f$, its probability under $U$ equals that of $f\to i$ under $U^\dagger$, by conjugation of the amplitude. The explicit controls below are their own inverses. A reverse input in $F$ includes the recoiling $A$ with momentum opposite the photon. Absorption of $\epsilon_\gamma$ by a *stationary* $A$ would have different initial four-momentum and would require the larger rest-frame photon energy $(M_1^2-M_0^2)c^2/(2M_0)$ to reach $M_1$.

## Attaining controls and full readout

**One sign.** Take the available direction to be $+$. Exchange $\lvert B\rangle\leftrightarrow\lvert F_+\rangle$, fix $\lvert C\rangle$, and leave the spectators fixed. This basis permutation is unitary on the entire specified space. $B$ emits certainly, $C$ stays in vacuum, and the reverse joint branch maps back to $B$.

More generally a swap can select any normalized vector $\lvert b\rangle\in E$ to emit and leave its orthogonal vector in vacuum. The sector click effect is then $\lvert b\rangle\langle b\rvert$. The mixture $I_2/2$ gives the same probability $1/2$ in any basis. A balanced choice gives $B$ and $C$ probability $1/2$ each, the greatest achievable minimum over those two labelled inputs. For every one-mode control some coherent sector input has zero click probability, since $T$ has a kernel. Even within the labelled input set, both labels cannot emit with certainty into this one complete outgoing state.

**Both signs.** Define orthonormal outgoing states
$$
 \lvert\Psi_B\rangle=(\lvert F_+\rangle+\lvert F_-\rangle)/\sqrt2,\qquad
 \lvert\Psi_C\rangle=(\lvert F_+\rangle-\lvert F_-\rangle)/\sqrt2 .
$$
Exchange $B\leftrightarrow\Psi_B$ and $C\leftrightarrow\Psi_C$ in this orthonormal basis and extend by identity on the spectators. This specifies the map on all four resonant states and gives $U^\dagger=U$. In the direction basis,
$$
 U\lvert F_+\rangle=(\lvert B\rangle+\lvert C\rangle)/\sqrt2,\qquad
 U\lvert F_-\rangle=(\lvert B\rangle-\lvert C\rangle)/\sqrt2 .
$$
The restriction from $E$ to $F$ is an isometry onto $F$. Every sector input emits one photon, including arbitrary coherent superpositions. The equal native mixture maps to $I_F/2$. Any complete-conversion unitary between these two spaces has that same output mixture, although its label-conditioned outputs can differ.

The entries below are joint probabilities of initial label and optical outcome given the setting, in units of $1/14$. They apply also given any complete native history. A zero in a no-click column means that emission is certain on that input. The first three columns use the $B$-selective one-mode swap, and the last three use the coherent two-mode swap.

| Input | One mode $+$ | One mode $-$ | One mode, no photon | Two modes $+$ | Two modes $-$ | Two modes, no photon |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| $A$ | 0 | 0 | 5 | 0 | 0 | 5 |
| $B$ | 4 | 0 | 0 | 2 | 2 | 0 |
| $C$ | 0 | 0 | 4 | 2 | 2 | 0 |
| $D$ | 0 | 0 | 1 | 0 | 0 | 1 |
| Total | 4 | 0 | 10 | 4 | 4 | 6 |

Each setting's total is $14/14=1$. For the complete joint law with $h=(t,b_1,b_2)$, multiply each normalized cell by $P(h)=q_t/4$, with $q_{\mathsf E}=2/3,\ q_{\mathsf F}=1/3$ and four labelled bit pairs for each second ideal $t$. The native path weights and forbidden paths are preserved before the optical interface. Sum label rows when only the optical outcome is read. Every no-photon trial remains in the denominator. The model supplies ideal number/direction effects with no separate instrument-fault outcome. In one-mode operation $4/14$ of all trials miss an occupied sector, and $6/14$ are spectators. Conditional on no click, $4/10$ are therefore occupied. In two-mode operation all $6/14$ no-click trials are spectators. A click certifies prior sector membership in either setting.

## Which information is in the photon?

For input $B$ or $C$ in the coherent two-mode construction, trace out the daughter. The two daughter momenta $-k,+k$ are orthogonal. Their inner product sets both photon off-diagonal terms to zero, yielding
$$
 \rho_{\gamma|B}=\rho_{\gamma|C}
  =\tfrac12\bigl(\lvert1_+\rangle\langle1_+\rvert+
                   \lvert1_-\rangle\langle1_-\rvert\bigr).
$$
Thus every photon-only measurement has the same distribution on the two labels, including direction-resolved or phase-sensitive measurements. For the conditional label-identification question the tag is a reference for scoring and is withheld from the observer. With equal priors the best photon-only guess succeeds with probability $1/2$. The two joint states have inner product zero. Projecting the joint system onto $\Psi_B,\Psi_C$, or applying the specified inverse and reading the restored carrier label, identifies either label with certainty. A joint measurement of momenta alone reveals the branch direction but misses the relative sign. The native input is an incoherent mixture. The unitary creates a definite relative phase on each labelled input. This joint discrimination requires coherent control of both correlated branches, a stable relative phase convention and access to both daughter and photon. Dephasing between the branches before the joint test removes the sign information. None of these capabilities follows from the native labels.

With a fixed classical reversible permutation of the same registered basis and full emission, the two occupied inputs must go to different members of $\{F_+,F_-\}$. For instance the two direct swaps $B\leftrightarrow F_+$, $C\leftrightarrow F_-$ attain the same full conversion, recoil ledger and unconditional table totals. In that case a direction-resolving photon observation and knowledge of the permutation identify the input label exactly. A number-only observation still reports just the sector. An unobserved random choice of permutation would introduce an extra resource outside the fixed control class. An ordinary quantum comparator granted the same coherent control, joint access and phase reference as the coherent construction yields the very same distinguishability results. The comparison concerns the encoding of the label under specified controls. The success bounds for counting the sector are attained already by basis permutations.

## Inferring sector population and released energy

At full conversion the one-photon probability equals the initial one-occupation probability for any input mixture on the admitted native labels. Both $A$ and $D$ are dark spectators here, so the count measures the one-occupation population specifically. With one saturated mode and the certified uniform $B,C$ mixture, twice the measured click frequency estimates that population across trials. A no-click outcome then leaves sector membership unresolved on that trial. If the within-sector state or conversion efficiency is unknown, the same correction is unjustified.

For either attaining control, let $p_{\rm c}$ be its all-trial click probability. The average released rest energy is $p_{\rm c}G$. The photon energy delivered on average is $p_{\rm c}\epsilon_\gamma$, and the corresponding daughter kinetic energy is $p_{\rm c}K_{\rm d}$. No-conversion trials carry zero changes in these three quantities. For a trial with click indicator $I_{\rm c}=0$ or $1$, the event ledger is $I_{\rm c}\epsilon_\gamma+I_{\rm c}K_{\rm d}=I_{\rm c}G$. Its expectation gives the all-trial energy balance. A frequency or energy measurement on a responding subset can calibrate a photon line under the independently supplied mass-shell and photon-energy laws. It does not certify how many native sector members failed to radiate. Inferring the released rest energy requires the recoil correction and a physical energy scale.

The CL073 preparation provides the native probabilities and multiplicity. The joint-store and mass-gap results use separate reversible interfaces and calibrated store spacings. The spring comparison uses an inertial attachment. E59 established recoil kinematics for a registered free transition. None of these supplies the resonant mode box, control of the unitary and its phases, a detector, or a calibration of $c$ or a physical action unit from DET. Preparation, detection efficiency, recoil access, any phase reference and restoration require their own physical accounting. The result is confined to this one mass step and the two specified settings.

## Scientific review

DET Energy Research supplied the derivation. DET Relational State Research independently checked the sharp click bounds, the complete all-trial law, the joint-state distinction and the free-recoil energy ledger. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `151dbff90125bfd02d0ab3a0864d0b278cc9fd6268a48cf8af661290e685ff34`.
- Author report SHA-256: `e9675a44ff56ee1f9c71251e642ff62efed4e6bc82f63ea7c244870cf42ab2ce`.
- Freeze SHA-256: `5eafe08005dbcb2a0bf3cfd1061cc4c09229210a2eaac21ad6666db8d165b328`.
- Independent scientific review SHA-256: `daeafac67d5f0bccc66276709c7d0eb42eb2f4987289d744e47abeb816610e35`.
