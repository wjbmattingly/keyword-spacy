import spacy
from spacy.tokens import Doc, Token, Span
from spacy.language import Language
from collections import defaultdict

# Set extensions for tokens, doc, and sentence
Token.set_extension("keyword_value", default=0.0, force=True)
Doc.set_extension("keywords", default=[], force=True)
Span.set_extension("sent_keywords", default=[], force=True)

@Language.factory("keyword_extractor")
class KeywordExtractor:
    def __init__(self, nlp, name, top_n=5, top_n_sent=2, min_ngram=1, max_ngram=3, strict=False):
        self.top_n = top_n
        self.top_n_sent = top_n_sent
        self.min_ngram = min_ngram
        self.max_ngram = max_ngram
        self.strict = strict

    def valid_token(self, token):
        return not (token.is_punct or token.is_stop or token.like_num or not token.has_vector)

    def __call__(self, doc):
        keyword_freqs = defaultdict(int)
        keyword_similarities = defaultdict(float)

        # Process each sentence
        for sent in doc.sents:
            sent_keywords = self.extract_keywords(sent)
            for keyword, similarity in sent_keywords:
                keyword_freqs[keyword] += 1
                keyword_similarities[keyword] = similarity  # Store similarity score
            sent._.sent_keywords = sent_keywords

        # Sort keywords based on frequency for the entire document
        sorted_keywords = sorted(keyword_freqs.keys(), key=lambda x: keyword_freqs[x], reverse=True)
        
        # Convert the sorted keywords to tuples with their frequency and similarity scores
        doc._.keywords = [(keyword, keyword_freqs[keyword], keyword_similarities[keyword]) for keyword in sorted_keywords[:self.top_n]]
        
        return doc

    def extract_keywords(self, span):
        token_values = set()

        # Calculate the cosine similarity for individual tokens
        for token in span:
            if self.valid_token(token):
                token._.keyword_value = token.similarity(span)
                if not self.strict:
                    token_values.add((token.text, token._.keyword_value))

        # If min_ngram and max_ngram are not both 1, perform n-gram extraction
        if not (self.min_ngram == 1 and self.max_ngram == 1):
            for n in range(self.min_ngram, self.max_ngram + 1):
                for i in range(len(span) - n + 1):
                    ngram = span[i:i+n]
                    if all(self.valid_token(token) for token in ngram):
                        ngram_text = " ".join([token.text for token in ngram])
                        similarity = ngram.similarity(span)
                        token_values.add((ngram_text.strip(), similarity))

        # Sort based on similarity values
        sorted_tokens = sorted(token_values, key=lambda x: x[1], reverse=True)

        # Extract top keywords for the sentence based on `top_n_sent`
        sent_keywords = sorted_tokens[:self.top_n_sent]

        return sent_keywords
