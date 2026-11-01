# RET034: describe fitted compatibility accurately

The `held_out_transport` helper estimates a direction from training probe rows. It then uses every supplied target-probe residual to fit that probe's scalar loading and scores the fitted projection against the same target vector. Excluding the target from direction estimation does not withhold its responses from loading estimation or scoring.

The function docstring, comments and returned `interpretation` now describe this fitted subspace compatibility. The signature, arithmetic, iteration, thresholds, Boolean calculation and return keys are unchanged. Legacy names remain for compatibility. Residual construction and centering are supplied by the caller; this description covers the declared matched-history vectors, not new general input validation.

Independent static review of the exact function excerpt passed before integration. Integration replaced the unique matching old function body in the current module and preserved every byte outside it, including the previously published RET033 likelihood repair. No import, syntax check, test execution or numerical recalculation was performed for this wording-only change. Static source preservation is the validation evidence.

The accepted CL006 finite synthetic comparison motivates this distinction. It does not rank forecasting methods with equal information, establish noisy target calibration, or supply a physical observation channel. Neither the helper's pass nor its fail establishes calibrated forecasting, universal scalar existence/nonexistence or physical history. No CL006 calibration predictor is implemented here; other callers' broader labels remain outside this correction and are not endorsed.

This note describes a scoped source wording correction. Its exact publication assembly is separately reviewed before release.
