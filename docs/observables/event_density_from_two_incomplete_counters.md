# Proper area per sampled event from two incomplete counters

Two counters can identify the mean number of events in a causal diamond even if both miss events in a position-dependent way. Of the possible pairs of sign settings for their detection masks, the four that change exactly one counter identify the mean for every population in the model. Changing both counters together or repeating a setting can give identical observed count laws at two different densities.

## Observation

Use a diamond of proper area $L^2$ and normalized area density $f_\theta(u,v)=1+\theta(2u-1)(2v-1)$ on $(0,1)^2$, with $|\theta|\le1/2$. Each independent exposure contains a Poisson count with mean $\mu=\rho L^2>0$. Given the count, candidate locations are independent draws from proper area. A labelled setting $(s,t)\in\{-1,1\}^2$ applies throughout an exposure. The two detection probabilities at each location are
$$
p_1=a(1+sF),\qquad p_2=b(1+tH),
$$
with stable $0<a,b\le1/2$ and smooth masks satisfying $|F|,|H|\le1/2$. For each candidate the counters act independently conditional on location and setting. Candidate marks are independent. Record the exact population law of the counts detected by only the first counter, only the second counter, and both counters. Coincidences are matched within an exposure, and empty exposures are retained.

Let $X,Y$ denote the two inclusive mean counts and $Z$ the matched mean. With brackets denoting the normalized proper-area average, these means are $\mu\langle p_1\rangle$, $\mu\langle p_2\rangle$ and $\mu\langle p_1p_2\rangle$. Independent Poisson marking makes the three recorded counts independent Poisson variables with rates $(X-Z,Y-Z,Z)$. Thus matching those rates matches the complete observed law. The inclusive counts have covariance $Z$. [Last and Penrose, Theorems 5.6 and 5.8, August 2017](https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf)

## Which counter to change

Flip the first counter's sign and hold the second fixed. The two first-counter efficiencies add pointwise to $2a$. As a result $Y_1=Y_2=Y$, $X_1+X_2=2a\mu$ and $Z_1+Z_2=2aY$. The positive summed overlap yields
$$
\mu=\frac{(X_1+X_2)Y}{Z_1+Z_2}.
$$
If the second counter flips, the corresponding expression is $X(Y_1+Y_2)/(Z_1+Z_2)$. These formulas use mean counts per labelled exposure. They give the missed-both intensity $\mu-X-Y+Z$ at each setting. A realized missed count remains hidden.

For either a repeated first setting $(s_0,t_0)$ or a simultaneous flip, compare two populations with the same shape, area and clock. At $\mu=48$ take $a=b=1/4$ and $F=H=0$. At $\mu=49$ take $a=b=12/49$, $F=s_0(2u-1)/4$ and $H=t_0(2u-1)/4$. The $u$ marginal is uniform, so both mask means vanish and $\langle FH\rangle=s_0t_0/48$. At either retained setting, both populations have $X=Y=12$ and $Z=3$. Their full observed laws are the product of three Poisson laws with rates $(9,9,3)$, including the same empty-exposure probability $e^{-21}$. Their missed-both intensities are 27 and 28. This covers all four repeated settings and both simultaneous-flip pairs. Some simultaneous-flip records with nonzero contrast can identify $\mu$ individually.

## Clock and curvature units

An independent order measurement supplies the shape via $\theta=9(p-1/2)$ and $R_cL^2=8\theta$, where $R_c$ is centre scalar curvature. The tip-to-tip maximizing clock gives $cN\Delta=\sqrt2\,LJ(\theta)$ with tick duration $\Delta$, exact elapsed reading $N>0$ and $J(\theta)=\int_0^1\sqrt{1+\theta z^2}\,dz$. Correct endpoint phases, the maximizing path and the matched geometry are required. [Order measurement](order_comparability_and_curvature.md) · [Tip clock and curvature](proper_time_and_curvature_of_a_diamond.md)

Define the mean area per latent event as $1/\rho=L^2/\mu$. Its associated length and the dimensionless centre curvature then satisfy
$$
\frac{\rho^{-1/2}}{c\Delta}=\frac{N}{\sqrt{2\mu}\,J(\theta)},\qquad
\frac{R_c}{\rho}=\frac{8\theta}{\mu}.
$$
A calibrated tick gives the absolute area and density. The two-counter proof uses exact population laws, including the possibility of zero events. A finite experiment needs its own sampling uncertainty and registration of the two detectors. Relating this density length to DET would also require evidence that native events correspond to these proper-area Poisson candidates.
