import math
import statistics

def round_down_1_decimal(value):
    return math.floor(value * 10) / 10

def round_up_1_decimal(value):
    return math.ceil(value * 10) / 10

def remove_outliers_iqr_3x(values):
    if len(values) < 4:
        return values

    sorted_values = sorted(values)
    q1 = statistics.quantiles(sorted_values, n=4, method="inclusive")[0]
    q3 = statistics.quantiles(sorted_values, n=4, method="inclusive")[2]
    iqr = q3 - q1

    lower = q1 - (3 * iqr)
    upper = q3 + (3 * iqr)

    return [x for x in values if lower <= x <= upper]

def calculate_limits(yields, bin_rates, product_type="standard"):
    clean_yields = remove_outliers_iqr_3x(yields)
    clean_bins = remove_outliers_iqr_3x(bin_rates)

    mean_yield = statistics.mean(clean_yields)
    sigma_yield = statistics.pstdev(clean_yields)

    mean_bin = statistics.mean(clean_bins)
    sigma_bin = statistics.pstdev(clean_bins)

    if product_type == "automotive":
        syl = mean_yield - (2 * sigma_yield)
        sbl = mean_bin + (3 * sigma_bin)
    elif product_type == "rp":
        syl = mean_yield - (6 * sigma_yield)
        sbl = mean_bin + (6 * sigma_bin)
    else:
        syl = mean_yield - (3 * sigma_yield)
        sbl = mean_bin + (3 * sigma_bin)

    sml = mean_yield - (5 * sigma_yield)

    return {
        "mean_yield": round(mean_yield, 3),
        "sigma_yield": round(sigma_yield, 3),
        "mean_bin": round(mean_bin, 3),
        "sigma_bin": round(sigma_bin, 3),
        "syl": round_down_1_decimal(syl),
        "sbl": max(round_up_1_decimal(sbl), 0.2),
        "sml": round_down_1_decimal(sml),
        "input_lots": len(yields),
        "used_lots": len(clean_yields)
    }

def evaluate_lot(yield_percent, bin_rate_percent, bin_qty, syl, sbl, sml, small_quantity_rule=False, asic_sbin=False):
    reasons = []

    if yield_percent < sml:
        reasons.append("MAVERICK_YIELD_HOLD")

    if yield_percent < syl:
        reasons.append("LOW_YIELD_HOLD")

    if bin_rate_percent > sbl:
        reasons.append("HIGH_FAIL_RATE_BIN_HOLD")

    if not reasons:
        return {
            "decision": "RELEASE",
            "reasons": [],
            "qdn_skip_applied": False
        }

    if small_quantity_rule:
        if asic_sbin:
            if bin_qty <= 2 and bin_rate_percent <= 0.5:
                return {
                    "decision": "AUTO_RELEASE_QDN_SKIP",
                    "reasons": reasons,
                    "qdn_skip_applied": True
                }
        else:
            if bin_qty <= 8 and bin_rate_percent < 5:
                return {
                    "decision": "AUTO_RELEASE_QDN_SKIP",
                    "reasons": reasons,
                    "qdn_skip_applied": True
                }

    return {
        "decision": "HOLD",
        "reasons": reasons,
        "qdn_skip_applied": False
    }

def calculate_shift_ratio(calculated_limit, original_limit, long_term_sigma):
    if long_term_sigma == 0:
        return 0
    return (calculated_limit - original_limit) / long_term_sigma

def requires_limit_review(shift_ratio):
    return abs(shift_ratio) > 2
