import spacy
nlp = spacy.load('en')

doc = nlp("Next week I'll be in Madrid.")
for ent in doc.ents:
    print(ent.text, ent.label_)

# Next week DATE
# Madrid GPE
