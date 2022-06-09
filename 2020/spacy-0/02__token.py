import spacy
nlp = spacy.load('en')
doc = nlp('Hello     World!')
for token in doc:
  print('"%s" %d' % (token.text, token.idx))

# "Hello" 0
# "    " 6
# "World" 10
# "!" 15
