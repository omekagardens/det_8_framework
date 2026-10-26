# Relative clock rates from device exchange: a conditional finite-record theorem

Exchanging two devices between stations can identify their relative rates when the same path-delay slope applies before and after the exchange. Without that invariance, the complete prescribed record can agree between worlds with different rate ratios. This theorem states both conclusions for one fixed observation model; it supplies no physical calibration or native law of gravity.

## Model and retained observations

Use an auxiliary coordinate \(t\in[0,110]\), stations A, B, C, and clocks
\[
c_A(t)=t,\qquad c_D(t)=a_Dt+b_D,\qquad c_E(t)=a_Et+b_E,
\]
where \(a_D,a_E\in[9/10,11/10]\) and \(b_D,b_E\in[-5,5]\). The target is \(a_D/a_E\). These are stipulated affine readings, without a proper-time interpretation.

A emits the following identified packets at the exact commanded epochs:

| Block | Device at B | Device at C | Direct A→B→A sends | Relayed A→C→B→A sends |
|---|---|---|---|---|
| Before exchange | D | E | 0, 10 | 20, 30 |
| After exchange | E | D | 60, 70 | 80, 90 |

At the prescribed assignment boundary 50, D and E exchange stations. Their affine laws continue without reset. Correct reassociation, transport invariance and completion before the second block are supplied premises. No packet is emitted or in transit during the exchange. Transport trajectory and duration are unobserved and are not assumed to be zero. The boundary supplies no simultaneous D/E reading.

On each directed link \(e\in\{AB,AC,CB,BA\}\), departure at t leads to arrival
\[
F_e(t)=t+d_e(t)=(1+v_e)t+u_e.
\]
The delay is evaluated at departure, including intermediate departures on relayed routes. Every link law satisfies
\[
\tfrac12\le u_e+v_et\le4\quad(0\le t\le110),
\qquad |v_e|\le\tfrac1{100}.
\]
The **main family** uses one station-attached parameter pair per link across both blocks. Affine drift is allowed; unchanged parameters do not mean constant delays. The **negative-control family** instead permits separate before/after pairs per link, each satisfying those same bounds on the whole interval. All other premises remain fixed.

C forwards immediately upon receipt; B returns immediately upon receipt. Processing delays are stipulated zero. Receipt and send are distinct, causally ordered events with equal ideal local readings.

For a direct emission s, set \(t_B=F_{AB}(s)\), \(t_A=F_{BA}(t_B)\). The ordered ideal timestamp tuple is
\[
(s,c_B(t_B),c_B(t_B),t_A),
\]
representing A send, B receipt, B return-send and A return-receipt. Here \(c_B\) denotes the device assigned to B in that block, and \(c_C\) denotes the device at C. For a relay, set \(t_C=F_{AC}(s)\), \(t_B=F_{CB}(t_C)\), \(t_A=F_{BA}(t_B)\), and retain
\[
(s,c_C(t_C),c_C(t_C),c_B(t_B),c_B(t_B),t_A),
\]
representing A send, C receipt, C forward-send, B receipt, B return-send and A return-receipt. Add A's ideal closure reading 110: four direct and four relay packets give \(4\cdot4+4\cdot6+1=41\) timestamp fields.

Each event retains its unique identity, packet, block, route, station, reading device, event kind, local predecessor and causal-predecessor references. Copied references preserve identities and add no clock observation. Exchange-command identity, epoch 50 and assignment maps are retained as metadata. No transport timestamps, D/E exchange readings, B/C closure readings or record-access timings are observed.

Every displayed timestamp has arbitrary error of magnitude at most \(\epsilon=1/100\); errors may correlate. Exact execution of the commanded schedule is a separate premise. Missing required fields, unresolved duplicates or inconsistent identities require incomplete/invalid status and **ABSTAIN**, even if some useful timestamps remain. Identifiers do not authenticate truthful readings, bounded errors or successful exchange.

## Identification in the main family

Let \(y_s\) be the ideal B-receipt reading for direct send s, and put \(k=1+v_{AB}\). Then
\[
X=\frac{y_{10}-y_0}{10}=a_Dk,
\qquad
Y=\frac{y_{70}-y_{60}}{10}=a_Ek.
\]
Offsets and the path intercept cancel within each block. Since
\[
Y\ge\frac9{10}\frac{99}{100}=\frac{891}{1000}>0,
\qquad \boxed{\frac{a_D}{a_E}=\frac{X}{Y}},
\]
any two main-family worlds with the same complete noiseless record have the same target ratio. The four B-receipt fields suffice for this proof; the other required observations still constrain feasibility. No identification of every parameter is asserted.

The contrast needs a common AB delay slope and a consistent device-rate identity across the exchange. It needs neither a known slope nor synchronized offsets. The fixed protocol's common intercept and other shared path parameters are stronger conditions than this contrast uses; they remain part of the admitted model.

## Complete-record ambiguity without path invariance

World U has both rates one, offsets zero and all link delays one. World V has \(a_D=r=401/400\), \(a_E=1\), offsets zero, and
\[
f(t)=\frac{400-t}{401},\qquad g(t)=1+\frac{t}{400}.
\]
Its link delays are:

| Link | Before exchange | After exchange |
|---|---|---|
| AB | f | 1 |
| AC | 1 | f |
| CB | f | g |
| BA | g | 1 |

Throughout \([0,110]\),
\[
f(t)\in[290/401,400/401],\quad g(t)\in[1,51/40].
\]
These lie in \([1/2,4]\); slopes \(-1/401\), \(1/400\) and zero satisfy the slope bound. Rates and offsets also satisfy their domains.

The arrival maps for f, g and unit delay are respectively
\[
t\mapsto(t+1)/r,\qquad t\mapsto rt+1,\qquad t\mapsto t+1.
\]
Before exchange, direct packets reach D at \((s+1)/r\), giving reading s+1 and A return s+2. Relays reach E at s+1, then D at \((s+2)/r\), giving readings s+1 and s+2 and A return s+3. After exchange, direct paths have unit delays and B holds E. Relays reach D at \((s+1)/r\), then E at \(r((s+1)/r)+1=s+2\), and return at s+3.

Thus, with zero display errors, both worlds yield every required timestamp:

| Record | Sends | Complete tuple |
|---|---|---|
| Direct | 0, 10, 60, 70 | \((s,s+1,s+1,s+2)\) |
| Relayed | 20, 30, 80, 90 | \((s,s+1,s+1,s+2,s+2,s+3)\) |
| A closure | — | \((110)\) |

All prescribed identities, references and assignment metadata can coincide. Positive delays and increasing arrival maps respect causal edges and local event order. Equal receipt/send readings still belong to distinct events. Pre-block packets finish by 33 and post-block packets by 93; none crosses the exchange.

The target ratios nevertheless differ: 1 versus 401/400. Common admissible display errors preserve the equality. This proves one complete-record ambiguity, not ambiguity for every record. Since U also belongs to the main family, compatibility with that family cannot itself certify unchanged paths.

## Bounded-error outer interval

In the main family, use displayed B-receipt readings to form \(\widehat X,\widehat Y\) with the same exact denominator 10. Arbitrary correlated errors imply
\[
|\widehat X-X|,|\widehat Y-Y|\le\delta=2\epsilon/10=1/500.
\]
Let \(J=[891/1000,1111/1000]\) and
\[
I_X=[\widehat X-\delta,\widehat X+\delta]\cap J,
\qquad I_Y=[\widehat Y-\delta,\widehat Y+\delta]\cap J.
\]
An empty intersection signals inconsistency and ABSTAIN. Otherwise write endpoints \(x_-,x_+,y_-,y_+\). Every feasible ratio lies in
\[
\boxed{\Theta_{\rm out}=
[x_-/y_+,x_+/y_-]\cap[9/11,11/9].}
\]
Every divisor is at least 891/1000; a raw near-zero displayed difference is never divided by. An empty final interval also signals inconsistency. A nonempty interval is only necessary: shared k, other timestamps, offsets and whole-interval constraints may further restrict feasibility. It is neither a confidence interval nor an exact characterization of the full-record feasible set.

The theorem relies on supplied transport continuity, station/path invariance, correct identities, zero turnaround, exact schedule execution and truthful bounded displays. Model fit does not establish these premises. No metric, invariant propagation speed, physical clock calibration, empirical gravity result or native DET prediction follows.
