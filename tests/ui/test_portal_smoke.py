def test_low_yield_hold(page):
    page.goto("http://127.0.0.1:5000")

    page.get_by_test_id("yield").fill("93.0")
    page.get_by_test_id("bin").fill("0.8")

    page.get_by_test_id("evaluate-btn").click()

    assert "LOW_YIELD_HOLD" in page.text_content("body")


def test_high_fail_rate_hold(page):
    page.goto("http://127.0.0.1:5000")

    page.get_by_test_id("yield").fill("96.0")
    page.get_by_test_id("bin").fill("2.0")

    page.get_by_test_id("evaluate-btn").click()

    assert "HIGH_FAIL_RATE_BIN_HOLD" in page.text_content("body")


def test_release_good_lot(page):
    page.goto("http://127.0.0.1:5000")

    page.get_by_test_id("yield").fill("96.0")
    page.get_by_test_id("bin").fill("0.8")

    page.get_by_test_id("evaluate-btn").click()

    assert "RELEASE" in page.text_content("body")