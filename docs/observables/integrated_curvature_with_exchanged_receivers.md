# Measuring integrated curvature with four portable frequency devices

Make two registered four-ray measurements. Between them, move both tip devices to side corners, and both side devices to tips. Either ordering within each destination pair works. If the devices keep their gains and the two diamonds have the same integrated scalar curvature $I$, then
$$
\boxed{I=\log Q_1+\log Q_2},\qquad
Q_r=\frac{r_{PA,r}\,r_{PB,r}}{r_{AF,r}\,r_{BF,r}} .
$$
Each $r_{XY,r}>0$ is the received frequency divided by the emitted frequency on the identified future ray $X\to Y$ in exposure $r$. Of the 24 possible second placements, exactly four identify $I$. The error interval below quantifies what transport stability and diamond reproducibility this exchange costs.

## What survives unknown observer velocities

Use the accepted optical law in a smooth conformal diamond $ds^2=-2L^2 f(u,v)\,du\,dv$, with $P=(0,0), A=(1,0), B=(0,1), F=(1,1)$, $L>0$, and $f>0$. Each ray is affinely propagated. The two readings at a corner share the same future unit velocity and multiplicative device gain; different corners and exposures have free rapidities. The curvature sign convention gives $I=2\log(f_P f_F/(f_A f_B))$. All logarithms are natural. Write $x_{i,r}=\log a_{i,r}$ for the four positive device gains in common reference units. For each placement define $d_{r,i}=+1$ when device $i$ is at side $A$ or $B$, and $-1$ when at tip $P$ or $F$. The single-exposure theorem gives
$$
q_r:=\log Q_r=\tfrac12 I_r+2d_r\cdot x_r .
$$

This equation characterizes the *full four-ratio record* at fixed geometry and gains. To see why, subtract the zero-rapidity prediction from the observed four log ratios in order $PA,PB,AF,BF$. Write their residuals as $z_1,z_2,z_3,z_4$. The contrast equation is exactly $z_1+z_2-z_3-z_4=0$. The rapidity contributions in that order are $(p-a,b-p,t-a,b-t)$, where $p,a,b,t$ are the rapidities at $P,A,B,F$. The choice $(p,a,b,t)=(0,-z_1,z_2,z_3-z_1)$ reproduces all four residuals. This construction can be made independently in each run. Also, $f(u,v)=\exp[(I_r/2)uv]$ is positive, smooth and realizes any desired real $I_r$ on the unit square. These facts allow complete-record witnesses below, without access to separately retained absolute frequency tags.

## All second placements

In the nominal protocol $x_2=x_1=x$ and $I_1=I_2=I$. Fix the labelled first placement. The count in each row includes all permutations within the second pair of tips and the second pair of side corners.

| Original tip devices that move to a side | Number | What the full pair of four-ratio records allows |
|---|---:|---|
| 0 | 4 | $d_2=d_1$. A record is compatible exactly when $q_1=q_2$. Every real $I$ is then feasible. |
| 1 | 16 | $d_1,d_2$ are linearly independent. Every positive eight-ratio record admits every real $I$. |
| 2 | 4 | $d_2=-d_1$. Every positive record is compatible and gives the unique $I=q_1+q_2$. |

For a complete exchange the unknown gain terms in the two equations have opposite signs. Given the measured $q_1,q_2$, select any $x$ satisfying $d_1\cdot x=(q_1-q_2)/4$. The two equations hold for the displayed inverse. The smooth metric and rapidities above then realize both full records. The scalar product of gains in log space is determined, even though the individual gains remain free.

For a partial exchange, precisely one original side device stays on a side and one original tip device stays at a tip. The two sign vectors agree in two entries and disagree in two, so their dot product is zero and each has squared length four. For every proposed $I$, define $b_r=(q_r-I/2)/2$; $x=(b_1d_1+b_2d_2)/4$ is a common set of log gains producing both contrasts. For unchanged roles, $q_1=q_2$ is necessary and $x=b_1d_1/4$ suffices. A single run already has this same freedom for every positive four-ratio record.

**Explicit full-record control.** Start with all eight ratios equal to one, unit gains, flat metrics and zero rapidities. For any unsuccessful placement there is a device $k$ with the same role sign $s$ in both exposures. Change both integrals to any $\lambda\ne0$ using $f=\exp[(\lambda/2)uv]$; set that device's log gain to $-s\lambda/4$ in both runs and keep the other three at zero. Both contrast equations still give zero. In each run take $z$ to be minus its four zero-rapidity log predictions and apply the rapidity formula above. Each of the eight labelled ratios is again exactly one, with the same device movements. For example exchanging $P$ with $A$ alone leaves the device at $B$ on a side and it can serve as $k$. The one-run version uses any device in the same construction.

## Sharp tolerance for the first diamond

Use a complete exchange and put $d=d_1=-d_2$. Allow $\rho_i=\log(a_{i,2}/a_{i,1})$ to satisfy $|\rho_i|\le\epsilon_i$ with all sign patterns independently allowed. Let $\Delta=I_2-I_1$ satisfy $|\Delta|\le\delta$, independently of the drift. The positive frequency ratios are otherwise exact. Adding their two log contrasts gives
$$
S=q_1+q_2=I_1+\tfrac12\Delta-2d\cdot\rho .
$$
Thus for the given eight-ratio record the **entire feasible interval** is
$$
\boxed{I_1\in[S-B,S+B]},\qquad B=\tfrac12\delta+2\sum_{i=1}^4\epsilon_i .
$$
A common multiplicative drift of all devices has zero effect because $\sum d_i=0$; the radius above is sharp under the stipulated independent bounds. The sign is strictly positive if $S>B$ and strictly negative if $S<-B$. When zero lies in the interval the data allow zero integrated curvature.

For the upper endpoint take $\Delta=-\delta,\ \rho_i=d_i\epsilon_i$, and for the lower endpoint reverse these signs. Multiplying the upper choices by any $v\in[-1,1]$ gives $I_1=S+vB$, including the singleton when $B=0$. Set $I_2=I_1+\Delta$, $x_1=d(q_1-I_1/2)/8$ and $x_2=x_1+\rho$. Both scalar equations hold, and exponentiating the log gains gives positive device gains. Choose $f_r=\exp[(I_r/2)uv]$ and apply the explicit independent rapidities to match the *given* four ratios in each run. This proves attainability at both ends and throughout, including for non-unit or unequal individual links.

With unrestricted mismatch and stable portable gains, $S=(I_1+I_2)/2$ identifies the mean, while each individual integral can vary over the real line. With unrestricted mismatch and bounded drift, even that mean can differ from $S$ by $2\sum_i\epsilon_i$ in either direction. With unknown stationary gains attached to the four corner roles, moving devices leaves the same gain contrast in both runs; the unchanged-role row applies for equal integrals. An additional unknown station gain on top of portable gains also leaves an uncancelled common station contrast.

## Readout and physical scope

The exchange spends a second exposure, four additional identified null rays, and registered transport or reassignment of all four devices across the tip/side division. For each exposure one must recognize the same four corner roles, measure both ends of every ray with compatible local frequency readouts, and retain which device occupied each corner. The record comprises eight ratios and both placements. Transport must preserve, or bound changes in, the effective gains as used at the endpoints. Geometry must reproduce the integrated curvature to the stated tolerance. Neither condition requires repeating individual link ratios, velocities, wavelengths or phases. Independent evidence is needed for those stability bounds, the conformal metric and geometric-optics frequency law. The separate clock-exchange result assumes an unchanged packet-delay slope to compare affine device rates; using it as an optical gain calibration would require an additional device-to-frequency correspondence.

The signed integral and its tolerance are dimensionless. Rescaling $L$ on either diamond preserves its four ratios. A physical area or length calibration is still needed to express average curvature in inverse-length-squared units, and a curvature profile requires more geometric information. This is a conditional optical inference, with no native propagation law or material validation supplied.

[Four null-link frequency ratios](integrated_curvature_from_four_frequency_ratios.md) · [Device exchange under a packet-delay model](device_exchange_clock_ratio.md)
