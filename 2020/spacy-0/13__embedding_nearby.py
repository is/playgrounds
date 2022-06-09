import spacy
from scipy import spatial

nlp = spacy.load('en_core_web_lg')
cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)

man = nlp.vocab['man'].vector
woman = nlp.vocab['woman'].vector
queen = nlp.vocab['queen'].vector
king = nlp.vocab['king'].vector

# We now need to find the closest vector in the vocabulary to the result of "man" - "woman" + "queen"
maybe_king = man - woman + queen
computed_similarities = []

for word in nlp.vocab:
  # Ignore words without vectors
  if not word.has_vector:
    continue

  similarity = cosine_similarity(maybe_king, word.vector)
  computed_similarities.append((word, similarity))

computed_similarities = sorted(computed_similarities, key=lambda item: -item[1])
print([w[0].text for w in computed_similarities[:10]])

'''
['Queen', 'QUEEN', 'queen', 'King', 'KING', 'king', 'KIng', 'Kings', 'KINGS', 'kings']
'''
