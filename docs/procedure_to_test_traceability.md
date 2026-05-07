{% extends "base.html" %}
{% block content %}
<h1>Limit Review Shift Ratio</h1>
<form method="post" class="card form-card">
<label>Calculated Limit</label><input data-testid="calculated-limit" name="calculated_limit" required>
<label>Original Limit</label><input data-testid="original-limit" name="original_limit" required>
<label>Long Term Sigma</label><input data-testid="long-term-sigma" name="long_term_sigma" required>
<button data-testid="calculate-shift">Calculate Shift Ratio</button>
</form>

{% if result %}
<section class="card">
<h2>Result</h2>
<p>Shift Ratio: <span data-testid="shift-ratio">{{ result.shift_ratio }}</span></p>
<p>Requires Review: <span data-testid="requires-review">{{ result.requires_review }}</span></p>
</section>
{% endif %}
{% endblock %}
