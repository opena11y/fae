var evaluation = new OpenAjax.a11y.RulesetEvaluation("WCAG_2_0", "en-us", window.document, null);
evaluation.evaluate(true);

var out = evaluation.log.toString();
out += evaluation.ruleset_result.toString();
out += evaluation.dom_cache.color_contrast_cache.toString();

if ( window.getComputedStyle ) {
  out += "Can compute style\n";
}
else {
  out += "Can NOT compute style\n";
}
out;
