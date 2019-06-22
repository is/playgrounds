import spacy
from nltk.chunk import conlltags2tree

nlp = spacy.load('en')

doc = nlp("Next week I'll be in Madrid.")
iob_tagged = [
  (token.text, token.tag_,
    "{0}-{1}".format(token.ent_iob_, token.ent_type_)
      if token.ent_iob_ != 'O' else token.ent_iob_
  ) for token in doc
]

print(conlltags2tree(iob_tagged))

"""
(S
  (DATE Next/JJ week/NN)
  I/PRP
  'll/MD
  be/VB
  in/IN
  (GPE Madrid/NNP)
  ./.)
"""
