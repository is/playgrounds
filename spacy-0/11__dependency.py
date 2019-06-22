import spacy
nlp = spacy.load('en')

doc = nlp(
  'Wall Street Journal just published '
  'an interesting piece on crypto currencies')

for token in doc:
  print("{0}/{1} <--{2}--- {3}/{4}".format(
    token.text, token.tag_,
    token.dep_, token.head.text, token.head.tag_))

'''
Wall/NNP <--compound--- Street/NNP
Street/NNP <--compound--- Journal/NNP
Journal/NNP <--nsubj--- published/VBD
just/RB <--advmod--- published/VBD
published/VBD <--ROOT--- published/VBD
an/DT <--det--- piece/NN
interesting/JJ <--amod--- piece/NN
piece/NN <--dobj--- published/VBD
on/IN <--prep--- piece/NN
crypto/JJ <--compound--- currencies/NNS
currencies/NNS <--pobj--- on/IN
'''

# displacy.render(doc, style='dep', jupyter=True, options={'distance': 90})
