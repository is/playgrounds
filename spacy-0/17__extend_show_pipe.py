import spacy
from spacy.tokens import Doc
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentiment_analyzer = SentimentIntensityAnalyzer()

def polarity_scores(doc):
  return sentiment_analyzer.polarity_scores(doc.text)

Doc.set_extension('polarity_scores', getter=polarity_scores)
nlp = spacy.load('en')

print(nlp.pipeline)

'''
[('tagger', <spacy.pipeline.Tagger object at 0x1a16916128>),
('parser', <spacy.pipeline.DependencyParser object at 0x1a17f8b938>),
('ner', <spacy.pipeline.EntityRecognizer object at 0x1a17f8b990>)]
'''
