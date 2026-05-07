# Procedure-to-Test Traceability Matrix

| Procedure Area | Business Rule | Automated Coverage |
|---|---|---|
| Purpose | Track low yield lots and hold automatically | API and UI lot evaluation tests |
| SYL Definition | SYL controls yield characteristic to maximize | Unit test for SYL calculation |
| SBL Definition | SBL controls fail bin characteristic to minimize | Unit test for SBL calculation |
| Minimum data | Statistical limits use minimum 30 production lots | Unit test confirms 30 lots used |
| Standard Product | SYL = mean - 3 sigma, SBL = bin mean + 3 sigma | `test_standard_syl_sbl_calculation` |
| Automotive Product | SYL = mean - 2 sigma | API payload supports `automotive` |
| RP Product | SYL/SBL use 6 sigma | API payload supports `rp` |
| Hold Logic | Yield < SYL triggers LOW YIELD HOLD | `test_low_yield_hold_triggered` |
| Hold Logic | Bin fail rate > SBL triggers HIGH FAIL RATE BIN HOLD | `test_high_fail_bin_hold_triggered` |
| Maverick | Yield < SML triggers Maverick Yield Hold | `test_maverick_yield_hold_triggered` |
| Outlier Rule | Remove outliers using 3x IQR rule | `remove_outliers_iqr_3x` |
| Small Quantity Rule | Bin qty <= 8 and bin loss < 5% can auto release | `test_small_quantity_qdn_skip_rule_auto_release` |
| ASIC FT SBin | Qty <= 2 and SBin loss <= 0.5% can auto release | `test_asic_sbin_small_quantity_rule` |
| Limit Review | Shift ratio more than 2 sigma requires review | `test_shift_ratio_requires_review_when_more_than_2_sigma` |
