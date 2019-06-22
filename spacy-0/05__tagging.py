import spacy
nlp = spacy.load('en')

doc = nlp("Next week I'll be in Madrid.")
print([(token.text, token.tag_) for token in doc])
