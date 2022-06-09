import spacy
nlp = spacy.load('en')
doc = nlp("Next week I'll   be in Madrid.")
for token in doc:
  print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
    token.text,
    token.idx,
    token.lemma_,
    token.is_punct,
    token.is_space,
    token.shape_,
    token.pos_,
    token.tag_
  ))

# Next    0       next    False   False   Xxxx    ADJ     JJ
# week    5       week    False   False   xxxx    NOUN    NN
# I       10      -PRON-  False   False   X       PRON    PRP
# 'll     11      will    False   False   'xx     VERB    MD
#         15              False   True            SPACE   _SP
# be      17      be      False   False   xx      VERB    VB
# in      20      in      False   False   xx      ADP     IN
# Madrid  23      madrid  False   False   Xxxxx   PROPN   NNP
# .       29      .       True    False   .       PUNCT   .
