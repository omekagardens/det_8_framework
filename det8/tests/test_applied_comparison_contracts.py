"""Independent arithmetic and refusal checks for descriptive applied comparisons."""

import math
from fractions import Fraction as F

import pytest

from det8.applied_physics import adversarial as adv
from det8.applied_physics import applied_tests as app
from det8.applied_physics import discriminator as disc


def test_unknown_variance_gaussian_likelihood_and_identifiable_parameter_penalty():
    n, rss = 8, 2.0
    expected = n * (math.log(2 * math.pi) + 1 + math.log(F(1, 4)))
    assert adv.gaussian_iid_unknown_variance(n, rss)["neg2_log_likelihood"] == pytest.approx(expected)
    assert adv.bic(2, n, rss) is None
    score = adv.bic(2, n, rss, regularity_confirmed=True)
    assert score == pytest.approx(expected + 3 * math.log(n))  # two mean + variance
    assert adv.bic(3, n, rss, regularity_confirmed=True) - score == pytest.approx(math.log(n))
    comparison = adv.compare_bic(2, rss, 3, rss, n, regularity_confirmed=True,
                                 families=("linear", "log_linear"))
    assert comparison["preferred_family"] == "linear"
    assert comparison["det_wins"] is None
    assert comparison["physical_mechanism_identified"] is False


def test_known_correlated_gaussian_likelihood_and_scaling_oracle():
    # R^-1=(1/3)[[2,-1],[-1,2]], r=(1,-1), so r^T R^-1 r=2.
    covariance = [[2, 1], [1, 2]]
    result = adv.gaussian_known_covariance([1, -1], covariance)
    expected = 2 + math.log(3) + 2 * math.log(2 * math.pi)
    assert result["quadratic"] == pytest.approx(2)
    assert result["log_determinant"] == pytest.approx(math.log(3))
    assert result["neg2_log_likelihood"] == pytest.approx(expected)
    scaled = adv.gaussian_known_covariance([3, -3], [[18, 9], [9, 18]])
    assert scaled["neg2_log_likelihood"] - expected == pytest.approx(4 * math.log(3))
    score = adv.bic_known_covariance(1, [1, -1], covariance, regularity_confirmed=True)
    assert score == pytest.approx(expected + math.log(2))  # no variance parameter
    tiny = adv.gaussian_known_covariance([1e-12, -1e-12], [[2e-24, 1e-24], [1e-24, 2e-24]])
    assert tiny["quadratic"] == pytest.approx(2)


def test_exact_zero_rss_refuses_unknown_noise_but_known_noise_is_finite():
    result = adv.gaussian_iid_unknown_variance(10, 0)
    assert not result["available"] and result["neg2_log_likelihood"] is None
    assert adv.bic(2, 10, 0, regularity_confirmed=True) is None
    comparison = adv.compare_bic(2, 0, 2, 1, 10, regularity_confirmed=True)
    assert not comparison["comparison_available"]
    assert comparison["preferred_family"] is None and comparison["delta_bic"] is None
    assert "zero RSS" in comparison["reason"]
    known = adv.gaussian_known_covariance([0, 0], [[1, 0], [0, 1]])
    assert known["neg2_log_likelihood"] == pytest.approx(2 * math.log(2 * math.pi))
    subnormal = adv.gaussian_iid_unknown_variance(2, math.nextafter(0, 1))
    assert math.isfinite(subnormal["neg2_log_likelihood"])
    assert subnormal["variance_mle"] is None
    assert not subnormal["variance_mle_representable"]


@pytest.mark.parametrize("rss", [-1, float("nan"), float("inf"), True, "1"])
def test_invalid_rss_never_becomes_a_winning_score(rss):
    with pytest.raises((ValueError, TypeError)):
        adv.bic(1, 10, rss, regularity_confirmed=True)


@pytest.mark.parametrize("parameters,n", [(-1, 10), (1.5, 10), (True, 10), (1, 0), (1, True), (2, 2)])
def test_sample_and_mean_parameter_counts_are_validated(parameters, n):
    with pytest.raises(ValueError):
        adv.bic(parameters, n, 1, regularity_confirmed=True)


@pytest.mark.parametrize("covariance", [
    [[1, 0], [0, 0]], [[1, 2], [2, 1]], [[1, 1], [0, 1]],
    [[1]], [[1, 0], [0, float("nan")]], [[True, 0], [0, 1]],
])
def test_invalid_or_singular_known_covariance_is_refused(covariance):
    with pytest.raises((ValueError, TypeError)):
        adv.gaussian_known_covariance([0, 0], covariance)


@pytest.mark.parametrize("first,second", [([], []), ([1], []), ([1], [1, 2]), ([float("nan")], [1])])
def test_fit_and_rss_inputs_do_not_zip_truncate(first, second):
    for function in (adv.rss_between, adv.least_squares_fit_linear, app._fit_ieee, disc.fit_kww):
        with pytest.raises(ValueError):
            function(first, second)


def test_roughness_iid_moments_and_shared_difference_covariance():
    result = adv.iid_roughness_moments(20, 0.1)
    assert result["mean"] == pytest.approx(0.38)
    assert result["variance"] == pytest.approx(0.0224)
    assert result["difference_covariance"][0][0] == pytest.approx(0.02)
    assert result["difference_covariance"][0][1] == pytest.approx(-0.01)
    assert result["difference_covariance"][0][2] == 0
    assert adv.iid_roughness_moments(20, 0.01)["noise_contribution"] == pytest.approx(0.0038)
    one = adv.iid_roughness_moments(1, 0.1)
    assert one["mean"] == one["variance"] == 0


@pytest.mark.parametrize("sigma", [-1, float("nan"), float("inf"), True, "0.1"])
def test_declared_noise_scale_is_finite_nonnegative_and_typed(sigma):
    with pytest.raises((ValueError, TypeError)):
        adv.iid_roughness_moments(2, sigma)


def test_zero_noise_and_common_mode_covariance_have_zero_path_noise():
    assert adv.iid_roughness_moments(3, 0)["variance"] == 0
    result = adv.gaussian_roughness_moments([0, 0, 0], [[1] * 3 for _ in range(3)])
    assert result["mean"] == result["variance"] == 0
    subnormal = app.descriptive_fit_report({"family": {"rss": math.nextafter(0, 1)}}, 2)
    assert subnormal["fits"]["family"]["rmse"] > 0


def test_derived_kappa_coordinates_refuse_nonfinite_products():
    with pytest.raises(ValueError):
        app.kappa_output_coordinates(1e308, 0, 0, 2, 1)


def test_general_gaussian_roughness_has_independent_exact_oracle():
    # D mu=(1,0), D Sigma D^T=[[2,-5/4],[-5/4,5/2]].
    covariance = [[1, F(1, 2), 0], [F(1, 2), 2, F(1, 4)], [0, F(1, 4), 1]]
    result = adv.gaussian_roughness_moments([0, 1, 1], covariance)
    assert result["mean"] == pytest.approx(float(F(11, 2)))
    assert result["variance"] == pytest.approx(float(F(139, 4)))
    common = [[value + 2 for value in row] for row in covariance]
    shifted = adv.gaussian_roughness_moments([0, 1, 1], common)
    assert shifted["mean"] == pytest.approx(result["mean"])
    assert shifted["variance"] == pytest.approx(result["variance"])
    assert result["p_value"] is None


def test_derived_nonfinite_rss_and_roughness_are_refused():
    with pytest.raises(ValueError):
        adv.rss_between([1e308], [-1e308])
    with pytest.raises(ValueError):
        adv.roughness([1e308, -1e308])
    with pytest.raises((ValueError, OverflowError)):
        adv.gaussian_roughness_moments([0, 0], [[1e308, 0], [0, 1e308]])


@pytest.mark.parametrize("function", [
    lambda: adv.rss_between([1e-200], [0]),
    lambda: adv.roughness([0, 1e-200]),
    lambda: adv.iid_roughness_moments(2, 1e-200),
    lambda: adv.iid_roughness_moments(2, 1e-100),
    lambda: adv.gaussian_roughness_moments([0, 1e-200], [[0, 0], [0, 0]]),
    lambda: adv.gaussian_known_covariance([1e-200], [[1]]),
    lambda: adv.gaussian_known_covariance([1e-300], [[1e308]]),
])
def test_positive_squared_terms_must_not_underflow_to_exact_zero(function):
    with pytest.raises(ValueError, match="underflow"):
        function()


def test_representability_guards_preserve_exact_zero_controls():
    assert adv.rss_between([1, 1], [1, 1]) == 0
    assert adv.roughness([1, 1]) == 0
    assert adv.iid_roughness_moments(2, 0)["variance"] == 0
    assert adv.gaussian_known_covariance([0], [[1]])["quadratic"] == 0


def test_fit_bank_cannot_silently_discard_an_unrepresentable_better_loss():
    # tau=1 predicts (1,0,0) to float precision. Its positive RSS underflows;
    # silently skipping that candidate would incorrectly name tau=1000 best.
    with pytest.raises(ValueError, match="underflow"):
        app._fit_exp_decay([0, 1000, 2000], [1, 1e-200, 0], tau_grid=(1, 1000))


def test_relaxation_grid_refuses_nonzero_shape_square_underflow():
    times = [500, 501, 502]
    observed = [1, math.exp(-1), math.exp(-2)]
    shape = [math.exp(-value) for value in times]
    # The tau=1 shape remains positive and a finite amplitude recovers the
    # observations, but its unscaled squared norm rounds to zero. Skipping it
    # would silently select the worse tau=1000 candidate.
    assert all(value > 0 for value in shape)
    assert sum(value * value for value in shape) == 0
    assert [math.exp(500) * value for value in shape] == pytest.approx(observed)
    with pytest.raises(ValueError, match="shape norm underflows"):
        disc.fit_kww(times, observed, tau_grid=(1, 1000), beta_grid=(1,))


def test_relaxation_tail_square_underflow_preserves_a_representable_total_norm():
    times = list(range(0, 400, 4))
    shape = [math.exp(-value) for value in times]
    assert shape[-1] > 0 and shape[-1] * shape[-1] == 0
    fit = disc.fit_kww(times, [1] * len(times), tau_grid=(1,), beta_grid=(1,))
    # Independent geometric-series amplitude and projection-loss identities.
    r = math.exp(-4)
    s1 = (1 - r ** 100) / (1 - r)
    s2 = (1 - r ** 200) / (1 - r * r)
    assert fit["A"] == pytest.approx(s1 / s2, rel=1e-14)
    assert fit["rss"] == pytest.approx(100 - s1 * s1 / s2, rel=1e-14)
    assert fit["tau"] == fit["beta"] == 1
    assert not fit["physical_mechanism_identified"]


@pytest.mark.parametrize("bank", [(1, 1000), (1000, 1)])
def test_relaxation_bank_does_not_skip_an_entirely_underflowed_shape(bank):
    times = [1000, 1001, 1002]
    assert all(math.exp(-value) == 0 for value in times)
    with pytest.raises(ValueError, match="shape norm underflows"):
        disc.fit_kww(times, [1, math.exp(-1), math.exp(-2)],
                     tau_grid=bank, beta_grid=(1,))


def test_relaxation_norm_accumulates_individually_underflowed_squares():
    time = -math.log(1.5e-162)
    shape = math.exp(-time)
    assert shape * shape == 0
    assert float(4 * F.from_float(shape) ** 2) > 0
    fit = disc.fit_kww([time] * 4, [0] * 4, tau_grid=(1,), beta_grid=(1,))
    assert fit["A"] == fit["rss"] == 0
    assert fit["degenerate"] and fit["tau"] is None


def test_linear_baseline_recovers_an_intercept_and_log_linear_can_turn():
    slope, intercept, rss = adv.least_squares_fit_linear([1, 2, 3, 4], [5, 8, 11, 14])
    assert (slope, intercept, rss) == pytest.approx((3, 2, 0))
    t = [0, 1, 2, 4, 8]
    y = [2 * math.log1p(value) - value + 3 for value in t]
    fit = app._fit_ieee(t, y)
    assert fit["params"] == pytest.approx({"a": 2, "b": -1, "c": 3})
    assert fit["design_rank"] == 3
    assert y[0] < y[1] and y[1] > y[-1]  # derivative changes sign at t=1
    assert not fit["monotonicity_assumed"]
    assert app._fit_ieee([0, 0, 0], [1, 2, 3])["design_rank"] == 1
    with pytest.raises(ValueError):
        adv.least_squares_fit_linear([1, 1], [1, 2])


def test_unclipped_scale_confounded_pairs_produce_the_same_outputs():
    t = list(range(12))
    temperature = [280 + 5 * (i % 4) for i in t]
    flux = [i % 3 for i in t]
    first = app._det_drift(t, temperature, flux, 0.2, 0.1, 20, 0.01, 0.001, 1, 1)
    second = app._det_drift(t, temperature, flux, 0.1, 0.05, 20, 0.01, 0.0005, 1, 2)
    assert first == pytest.approx(second)
    assert all(0 < value < 1 for value in first)
    assert app.kappa_output_coordinates(0.2, 0.1, 0.001, 1, 20) == app.kappa_output_coordinates(0.1, 0.05, 0.0005, 2, 20)
    fit = app._fit_det_grid(t, first, iter(temperature), iter(flux), 1,
                            kappa0_grid=(0.1, 0.2), kappa_eq_grid=(0.1,),
                            tau0_grid=(20,), damage_grid=(0.001,), scale_grid=(1,))
    assert fit["rss"] == pytest.approx(0)
    assert fit["identifiable_mean_parameters"] is None and not fit["bic_available"]
    with pytest.raises(ValueError):
        app._det_drift([0, 1, 3], [300] * 3, [0] * 3, 0.2, 0.1, 10, 0, 0, 1, 1)


def test_relaxation_fits_describe_shapes_without_mechanism_or_false_identifiability():
    t = list(range(10))
    for beta, expected in ((1, "single_exponential"), (0.5, "stretched_exponential"), (2, "compressed_exponential")):
        y = [math.exp(-((value / 5) ** beta)) for value in t]
        fit = disc.fit_kww(t, y, tau_grid=(5,), beta_grid=(beta,))
        assert fit["classification"] == expected
        assert not fit["bic_available"] and not fit["physical_mechanism_identified"]
    zero = disc.fit_kww(t, [0] * len(t))
    assert zero["classification"] == "unclassified" and zero["tau"] is None
    constant = app._fit_exp_decay(t, [2] * len(t))
    assert constant["tau"] is None and constant["rss"] == 0
    insufficient = disc.fit_kww([0, 1], [1, 0.5])
    assert insufficient["degenerate"] and insufficient["beta"] is None
    assert app._fit_exp_decay([0, 1], [1, 0], tau_grid=(1e30,))["rss"] is None


def records_for_days(days, system="GPS"):
    return [{"start_epoch": f"2024-01-{day:02d}-00-00-00.000000",
             "end_epoch": f"2024-01-{day:02d}-00-00-30.000000",
             "time_system": system, "drift_s_per_s": float(day * day) * 1e-12}
            for day in days]


def test_missing_days_preserve_elapsed_time_and_aging_refuses_bic(monkeypatch):
    records = records_for_days([1, 2, 4, 6, 7, 8, 9, 10, 11, 12])
    report = app.aging_fit_report(records)
    assert report["elapsed_days"] == [0, 1, 3, 5, 6, 7, 8, 9, 10, 11]
    assert report["span_days"] == 11
    assert not report["bic_available"] and report["best"] is None
    assert set(report["fits"]) == {"exponential_offset_grid", "log_linear"}
    assert report["source_records"] == records
    from det8.applied_physics import ingest
    monkeypatch.setattr(ingest, "run_clock_aging", lambda *_: records)
    assert app.run_aging_adversarial("unused", "G01")["elapsed_days"] == report["elapsed_days"]
    monkeypatch.setattr(ingest, "run_clock_aging", lambda *_: [{"drift_s_per_s": 1}] * 10)
    assert "unsupported chronology" in app.run_aging_adversarial("unused", "G01")["error"]


def test_clock_timescales_and_leap_seconds_reuse_ingestion_contract():
    first = {"start_epoch": "2016-12-31-00-00-00.000000", "end_epoch": "2016-12-31-00-00-30.000000", "drift_s_per_s": 0}
    second = {"start_epoch": "2017-01-01-00-00-00.000000", "end_epoch": "2017-01-01-00-00-30.000000", "drift_s_per_s": 0}
    def elapsed(system):
        return app.clock_aging_coordinates([{**row, "time_system": system} for row in (first, second)])[0][-1]
    assert elapsed("UTC") == pytest.approx(1 + 1 / 86400)
    assert elapsed("GPS") == 1
    with pytest.raises(ValueError, match="TIME SYSTEM ID"):
        elapsed(None)
    mixed = records_for_days([1, 2])
    mixed[1]["time_system"] = "UTC"
    with pytest.raises(ValueError, match="inconsistent"):
        app.clock_aging_coordinates(mixed)
    with pytest.raises(ValueError):
        app.clock_aging_coordinates(records_for_days([1, 1]))


def test_roughness_generator_declares_noise_confound_and_has_no_fake_bic():
    high = app.test_qubit_drift("standard")
    low = app.test_qubit_drift("det")
    assert high["declared_generator_null"]["mean"] == pytest.approx(0.38)
    assert low["declared_generator_null"]["noise_contribution"] == pytest.approx(0.0038)
    for row in (high, low):
        assert row["score_type"] == "descriptive_path_roughness"
        assert row["bic_det"] is row["bic_std"] is row["det_wins"] is None
        assert row["correct_identification"] is None
