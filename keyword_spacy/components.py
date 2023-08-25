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
        return not (token.is_punct or token.is_stop or token.like_num or not token.has_vector)

    def __call__(self, doc):
        token_values = set()

        # Calculate the cosine similarity for individual tokens
        for token in doc:
            if self.valid_token(token):
                token._.keyword_value = token.similarity(doc)
                if not self.strict:
                    token_values.add((token.text, token._.keyword_value))

        # Calculate the cosine similarity for n-grams based on min_ngram and max_ngram
        for n in range(self.min_ngram, self.max_ngram + 1):
            for i in range(len(doc) - n + 1):
                ngram = doc[i:i+n]
                if all(self.valid_token(token) for token in ngram):
                    similarity = ngram.similarity(doc)
                    ngram_text = " ".join([token.text for token in ngram])
                    token_values.add((ngram_text.strip(), similarity))
                    # If ngram is ranked, suppress individual tokens from the ranking
                    for token in ngram:
                        token_values.discard((token.text, token._.keyword_value))
        
        # Sort based on similarity values
        sorted_tokens = sorted(token_values, key=lambda x: x[1], reverse=True)
        
        # Extract top keywords, ensuring they don't start or end with punctuation or whitespace
        top_keywords = [token[0] for token in sorted_tokens[:self.top_n] if not (token[0].startswith(('\n', ' ')) or token[0].endswith(('\n', ' ')))]
        doc._.keywords = top_keywords
        return doc
