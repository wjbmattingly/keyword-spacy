import spacy
from spacy.tokens import Doc, Token, Span
from spacy.language import Language

# Set extensions for tokens and doc
Token.set_extension("keyword_value", default=0.0, force=True)
Doc.set_extension("keywords", default=[], force=True)

@Language.factory("keyword_extractor")
class KeywordExtractor:
    def __init__(self, nlp, name, top_n=5, min_ngram=1, max_ngram=3, strict=False):
        self.top_n = top_n
        self.min_ngram = min_ngram
        self.max_ngram = max_ngram
        self.strict = strict

    def valid_token(self, token):
        return not (token.is_punct or token.is_stop)

    def __call__(self, doc):
        token_values = []

        # if not self.strict:
            # Calculate the cosine similarity for individual tokens
        for token in doc:
            if self.valid_token(token):
                token._.keyword_value = token.similarity(doc)
                if not self.strict:
                    token_values.append((token.text, token._.keyword_value))

        # Calculate the cosine similarity for n-grams based on min_ngram and max_ngram
        for n in range(self.min_ngram, self.max_ngram + 1):
            for i in range(len(doc) - n + 1):
                ngram = doc[i:i+n]
                if all(self.valid_token(token) for token in ngram):
                    similarity = ngram.similarity(doc)
                    token_values.append((" ".join([token.text for token in ngram]), similarity))
        
        # Sort based on similarity values
        sorted_tokens = sorted(token_values, key=lambda x: x[1], reverse=True)
        
        # Extract top keywords
        top_keywords = [token[0] for token in sorted_tokens[:self.top_n]]
        doc._.keywords = top_keywords
        return doc