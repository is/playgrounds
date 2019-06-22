import spacy
nlp = spacy.load('en')
doc = nlp('Hello     World!')
for token in doc:
  print('"%s"' % token.text)

# "Hello"
# "    "
# "World"
# "!"
