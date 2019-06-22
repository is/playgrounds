import spacy
nlp = spacy.load('en')

doc = nlp("These are apples. These are oranges.")
for sent in doc.sents:
  print(sent)

# These are apples.
# These are oranges.
