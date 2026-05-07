{% extends "base.html" %}
{% block content %}
<h1>SYL/SBL Limit Calculator</h1>
<form method="post" class="card form-card">
<label>Product Type</label>
<select data-testid="product-type" name="product_type">
<option value="standard">Standard: SYL mean-3σ, SBL mean+3σ</option>
<option value="automotive">Automotive: SYL mean-2σ</option>
<option value="rp">RP: SYL mean-6σ, SBL mean+6σ</option>
</select>
<button data-testid="calculate-limits">Calculate</button>
</form>

<div class="cards">
<div class="card"><h2>Mean Yield</h2><p>{{ result.mean_yield }}</p></div>
<div class="card"><h2>Sigma Yield</h2><p>{{ result.sigma_yield }}</p></div>
<div class="card"><h2>SYL</h2><p data-testid="calculated-syl">{{ result.syl }}</p></div>
<div class="card"><h2>SBL</h2><p data-testid="calculated-sbl">{{ result.sbl }}</p></div>
<div class="card"><h2>SML</h2><p data-testid="calculated-sml">{{ result.sml }}</p></div>
</div>
{% endblock %}
