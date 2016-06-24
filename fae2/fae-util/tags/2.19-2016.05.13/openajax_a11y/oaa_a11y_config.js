var doc = window.document;

var rs = OpenAjax.a11y.RulesetManager.getRuleset("ARIA_STRICT"); 
 
var evaluator_factory = OpenAjax.a11y.EvaluatorFactory.newInstance();
evaluator_factory.setParameter('ruleset', rs); 
evaluator_factory.setFeature('eventProcessing', 'fae-util');
evaluator_factory.setFeature('groups', 7); 

var evaluator = evaluator_factory.newEvaluator();

var evaluation = evaluator.evaluate(doc, doc.title, doc.location.href);

var out = evaluation.toJSON(true);

out;
