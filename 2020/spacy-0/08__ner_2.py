import spacy
nlp = spacy.load('en')

doc = nlp("I just bought 2 shares at 9 a.m. because the stock went up 30% in just 2 days according to the WSJ")
for ent in doc.ents:
  print(ent.text, ent.label_)

"""
2 CARDINAL
9 a.m. TIME
30% PERCENT
just 2 days DATE
WSJ ORG
""
