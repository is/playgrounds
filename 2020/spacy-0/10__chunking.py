import spacy

nlp = spacy.load('en')
doc = nlp(
  "Wall Street Journal just published "
  "an interesting piece on crypto currencies")
for chunk in doc.noun_chunks:
  print(chunk.text, chunk.label_, chunk.root.text)

'''
Wall Street Journal NP Journal
an interesting piece NP piece
crypto currencies NP currencies
'''
