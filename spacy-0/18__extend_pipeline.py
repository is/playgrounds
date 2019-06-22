import spacy
from nltk.corpus import wordnet as wn
from spacy.tokens import Token

def penn_to_wn(tag):
  if tag.startswith('N'):
    return 'n'

  if tag.startswith('V'):
    return 'v'

  if tag.startswith('J'):
    return 'a'

  if tag.startswith('R'):
    return 'r'

  return None

class WordnetPipeline(object):
  def __init__(self, nlp):
    Token.set_extension('synset', default=None)

  def __call__(self, doc):
    for token in doc:
      wn_tag = penn_to_wn(token.tag_)
      if wn_tag is None:
        continue

      ss = wn.synsets(token.text, wn_tag)[0]
      token._.set('synset', ss)

    return doc


nlp = spacy.load('en')
wn_pipeline = WordnetPipeline(nlp)
nlp.add_pipe(wn_pipeline, name='wn_synsets')
doc = nlp("Paris is the awesome capital of France.")

for token in doc:
    print(token.text, "-", token._.synset)
