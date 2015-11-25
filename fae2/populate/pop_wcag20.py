import sys,os
import django
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

"""This file is for populating the database with WCAG 2.0 References"""

from wcag20.models import Principle, Guideline, SuccessCriterion

# Principle.objects.all().delete()
# Guideline.objects.all().delete()
# SuccessCriterion.objects.all().delete()

def create_wcag20(wcag20):
    print("wcag 2.0")
    for principle in wcag20:
        principle_url = 'http://www.w3.org/TR/WCAG20/#' + principle[2]
        try:
          wcag20_principle = Principle.objects.get(num=principle[0])
          print("  " +  wcag20_principle.title + " (found)")
          
          wcag20_principle.title = principle[1]
          wcag20_principle.url = principle_url
          print(principle[1] + " (updated)")
        
        except:
          wcag20_principle = Principle(num=principle[0], title=principle[1], url=principle_url)
          print(principle[1] + " (CREATED)")
          
        wcag20_principle.save()
        
        for guideline in principle[3]:
            guideline_url = 'http://www.w3.org/TR/WCAG20/#' + guideline[2]
            try:
              wcag20_guideline       = Guideline.objects.get(principle=wcag20_principle, num=guideline[0])
              print("  " +  wcag20_guideline.title + " (found)")
              wcag20_guideline.title = guideline[1]
              wcag20_guideline.url   = guideline_url
              print("  " + guideline[1] + " (updated)")
              
            except:  
              wcag20_guideline = Guideline(principle=wcag20_principle, num=guideline[0], title=guideline[1], url=guideline_url)
              print("  " + guideline[1] + " (CREATED)")
              
            wcag20_guideline.save()
            
            for requirement in guideline[3]:
                requirement_url = 'http://www.w3.org/TR/WCAG20/#' + requirement[2]
                meet_url        = 'http://www.w3.org/WAI/WCAG20/quickref/#qr-' + requirement[2] + '.html'
                understand_url  = 'http://www.w3.org/TR/WCAG20/' + requirement[2] + '.html'
                
                try: 
                  wcag20_requirement = SuccessCriterion.objects.get(guideline=wcag20_guideline, num=requirement[0])
                  print("  " +  wcag20_requirement.title + " (found)")
                  wcag20_requirement.title = requirement[1]
                  wcag20_requirement.url = requirement_url
                  wcag20_requirement.url_meet = meet_url
                  wcag20_requirement.url_understand = understand_url
                  wcag20_requirement.level = requirement[3]
                  print("    " + requirement[1] + " (updated)")
                except:
                  wcag20_requirement = SuccessCriterion(guideline=wcag20_guideline, num=requirement[0], title=requirement[1], url=requirement_url, url_meet=meet_url, url_understand=understand_url, level=requirement[3])
                  print("    " + requirement[1]  + " (CREATED)")
                  
                wcag20_requirement.save()

wcag20 = (
  ('1', 'Perceivable - Information and user interface components must be presentable to users in ways they can perceive.', 'perceivable',
   (
    ('1', 'Text Alternatives', 'text-equiv',
      (
        ('1', 'Non-text Content', 'text-equiv', '1',),
      ),
    ),
    ('2', 'Time-based Media', 'media-equiv', 
      (
        ('1', 'Audio-only and Video-only (Prerecorded)', 'media-equiv-av-only-alt','1',),
        ('2', 'Captions (Prerecorded)', 'media-equiv-captions','1',),
        ('3', 'Audio Description or Media Alternative (Prerecorded)', 'media-equiv-audio-desc','1',),
        ('4', 'Captions (Live)', 'media-equiv-real-time-captions','2',),
        ('5', 'Audio Description (Prerecorded)', 'media-equiv-audio-desc-only','2',),
        ('6', 'Sign Language (Prerecorded)', 'media-equiv-sign','3',),
        ('7', 'Extended Audio Description (Prerecorded)', 'media-equiv-extended-ad','3',),
        ('8', 'Media Alternative (Prerecorded)', 'media-equiv-text-doc','3',),
        ('9', 'Audio-only (Live)', 'media-equiv-live-audio-only','3',),
      ),
    ),
    ('3', 'Adaptable', 'content-structure-separation',
      (
        ('1', 'Info and Relationships', 'content-structure-separation-programmatic','1',),
        ('2', 'Meaningful Sequence', 'content-structure-separation-sequenc','1',),
        ('3', 'Sensory Characteristics', 'content-structure-separation-understanding','1',),
      ),
    ),
    ('4', 'Distinguishable', 'visual-audio-contrast',
      (
        ('1', 'Use of Color', 'visual-audio-contrast-without-color','1',),
        ('2', 'Audio Control', 'visual-audio-contrast-dis-audio','1',),
        ('3', 'Contrast (Minimum)', 'visual-audio-contrast-contrast','2',),
        ('4', 'Resize text', 'visual-audio-contrast-scale','2',),
        ('5', 'Images of Text', 'visual-audio-contrast-text-presentation','2',),
        ('6', 'Contrast (Enhanced)', 'visual-audio-contrast7','3',),
        ('7', 'Low or No Background Audio', 'visual-audio-contrast-noaudio','3',),
        ('8', 'Visual Presentation', 'visual-audio-contrast-visual-presentation','3',),
        ('9', 'Images of Text (No Exception)', 'visual-audio-contrast-text-images','3',),
      ),
    ),
   ), 
  ),
  ('2', 'Operable - User interface components and navigation must be operable.', 'perceivable',
   (
    ('1', 'Keyboard Accessible', 'keyboard-operation',
      (
        ('1', 'Keyboard', 'keyboard-operation-keyboard-operable', '1',),
        ('2', 'No Keyboard Trap', 'keyboard-operation-trapping', '1',),
        ('3', 'Keyboard (No Exception)', 'keyboard-operation-all-funcs', '3',),
      ),
    ),
    ('2', 'Enough Time', '',
      (
        ('1', 'Timing Adjustable', 'time-limits-required-behaviors', '1',),
        ('2', 'Pause, Stop, Hide', 'time-limits-pause', '1',),
        ('3', 'No Timing', 'time-limits-no-exceptions', '3',),
        ('4', 'Interruptions', 'time-limits-postponed', '3',),
        ('5', 'Re-authenticating', 'time-limits-server-timeout', '3',),
      ),
    ),
    ('3', 'Seizures', 'seizure',
      (
        ('1', 'Three Flashes or Below Threshold', 'seizure-does-not-violate', '1',),
        ('2', 'Three Flashes', 'seizure-three-times', '3',),
      ),
    ),
    ('4', 'Navigable', 'navigation-mechanisms',
      (
        ('1', 'Bypass Blocks', 'navigation-mechanisms-skip', '1',),
        ('2', 'Page Titled', 'navigation-mechanisms-title', '1',),
        ('3', 'Focus Order', 'navigation-mechanisms-focus-order', '1',),
        ('4', 'Link Purpose (In Context)', 'navigation-mechanisms-refs', '1',),
        ('5', 'Multiple Ways', 'navigation-mechanisms-mult-loc', '2',),
        ('6', 'Headings and Labels', 'navigation-mechanisms-descriptive', '2',),
        ('7', 'Focus Visible', 'navigation-mechanisms-focus-visible', '2',),
        ('8', 'Location', 'navigation-mechanisms-location', '3',),
        ('9', 'Link Purpose (Link Only)', 'navigation-mechanisms-link', '3',),
        ('10', 'Section Headings', 'navigation-mechanisms-headings', '3',),
      ),
    ),
   ), 
  ),
  ('3', 'Understandable - Information and the operation of user interface must be understandable.', 'understandable',
   (
    ('1', 'Readable', 'meaning',
      (
        ('1', 'Language of Page', 'meaning-doc-lang-id', '1',),
        ('2', 'Language of Parts', 'meaning-other-lang-id', '2',),
        ('3', 'Unusual Words', 'meaning-idioms', '3',),
        ('4', 'Abbreviations ', 'meaning-located', '3',),
        ('5', 'Reading Level', 'meaning-supplements', '3',),
        ('6', 'Pronunciation', 'meaning-pronunciation', '3',),
      ),
    ),
    ('2', 'Predictable', 'consistent-behavior',
      (
        ('1', 'On Focus', 'consistent-behavior-receive-focus', '1',),
        ('2', 'On Input', 'consistent-behavior-unpredictable-change', '1',),
        ('3', 'Consistent Navigation', 'consistent-behavior-consistent-locations', '2',),
        ('4', 'Consistent Identification', 'consistent-behavior-consistent-functionality', '2',),
        ('5', 'Change on Request', 'consistent-behavior-no-extreme-changes-context', '3',),
      ),
    ),
    ('3', 'Input Assistance', 'minimize-error',
      (
        ('1', 'Error Identification', 'minimize-error-identified', '1',),
        ('2', 'Labels or Instructions', 'minimize-error-cues', '1',),
        ('3', 'Error Suggestion', 'minimize-error-suggestions', '2',),
        ('4', 'Error Prevention (Legal, Financial, Data)', 'minimize-error-reversible', '2',),
        ('5', 'Help', 'minimize-error-context-help', '3',),
        ('6', 'Error Prevention (All)', 'minimize-error-reversible-all', '3',),
      ),
    ),
  ),  
 ),
  ('4', 'Robust - Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies.', 'robust',
   (
    ('1', ' Compatible', 'ensure-compat',
      (
        ('1', 'Parsing', 'ensure-compat-parses', '1',),
        ('2', 'Name, Role, Value', 'ensure-compat-rsv', '1',),
      ),
    ),
   )
  )
)

create_wcag20( wcag20 )
