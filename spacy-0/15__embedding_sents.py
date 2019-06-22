import spacy
from scipy import spatial

nlp = spacy.load('en_core_web_lg')
target = nlp("Cats are beautiful animals.")

doc1 = nlp("Dogs are awesome.")
doc2 = nlp("Some gorgeous creatures are felines.")
doc3 = nlp("Dolphins are swimming mammals.")

print(target.similarity(doc1))  # 0.8901765218466683
print(target.similarity(doc2))  # 0.9115828449161616
print(target.similarity(doc3))  # 0.7822956752876101 # 0.67148364 0.2427285
