import spacy
from spacy import displacy

nlp = spacy.load('en')
doc = nlp('I just bought 2 shares at 9 a.m. because the stock went up 30% in just 2 days according to the WSJ')
displacy.serve(doc, style="ent")
#displacy.render(doc, style='ent')

