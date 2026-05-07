def calculate_syl(mean_yield, sigma):
    return mean_yield - (3 * sigma)

def calculate_sbl(mean_bin, sigma):
    return mean_bin + (3 * sigma)

def evaluate_lot(yield_percent, bin_rate, syl, sbl):
    if yield_percent < syl:
        return "LOW_YIELD_HOLD"
    if bin_rate > sbl:
        return "HIGH_FAIL_RATE_BIN_HOLD"
    return "RELEASE"

def test_syl_calculation():
    assert calculate_syl(97.0, 1.0) == 94.0

def test_sbl_calculation():
    assert round (calculate_sbl(0.7, 0.3),1) == 1.6

def test_low_yield_hold():
    decision = evaluate_lot(
        yield_percent=93.5,
        bin_rate=0.8,
        syl=94.0,
        sbl=1.6
    )
    assert decision == "LOW_YIELD_HOLD"

def test_high_fail_rate_bin_hold():
    decision = evaluate_lot(
        yield_percent=96.0,
        bin_rate=2.0,
        syl=94.0,
        sbl=1.6
    )
    assert decision == "HIGH_FAIL_RATE_BIN_HOLD"

def test_release_good_lot():
    decision = evaluate_lot(
        yield_percent=96.0,
        bin_rate=0.8,
        syl=94.0,
        sbl=1.6
    )
    assert decision == "RELEASE"