import spacy
from scipy import spatial

nlp = spacy.load('en_core_web_lg')

banana = nlp.vocab['banana']
dog = nlp.vocab['dog']
fruit = nlp.vocab['fruit']
animal = nlp.vocab['animal']

print(dog.similarity(animal), dog.similarity(fruit)) # 0.6618534 0.23552845
print(banana.similarity(fruit), banana.similarity(animal)) # 0.67148364 0.2427285
