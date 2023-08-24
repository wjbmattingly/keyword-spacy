# Keyword spaCy

Keyword spaCy is a spaCy pipeline component for extracting keywords from text using cosine similarity. The basis for this comes from [KeyBERT: A Minimal Method for Keyphrase Extraction using BERT](https://github.com/MaartenGr/KeyBERT), a transformer-based approach to keyword extraction. The methods employed by Keyword spaCy follow this methodology closely. It allows users to specify the range of n-grams to consider and can operate in a strict mode, which limits results to the specified n-gram range.

## Installation

Before using Keyword spaCy, make sure you have spaCy installed:

```
pip install spacy
```

Then, download the `en_core_web_md` model:

```
python -m spacy download en_core_web_md
```

## Usage

To use the Keyword Extractor, first, create a spaCy `nlp` object:

```python
import spacy
nlp = spacy.load("en_core_web_md")
```

Then, add the `KeywordExtractor` to the pipeline:

```python
nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10, "min_ngram": 1, "max_ngram": 3, "strict": False})
```

Now you can process text and extract keywords:

```python
text = "Your sample text here."
doc = nlp(text)
print("Top Keywords:", doc._.keywords)
```

## Configuration

The `KeywordExtractor` can be configured using the following parameters:

- `top_n`: The number of top keywords to extract.
- `min_ngram`: The minimum size for n-grams.
- `max_ngram`: The maximum size for n-grams.
- `strict`: If set to `True`, only n-grams within the `min_ngram` to `max_ngram` range are considered. If `False`, individual tokens and the specified range of n-grams are considered.

## Methodology

The methodology employed by Keyword spaCy is inspired by [KeyBERT](https://github.com/MaartenGr/KeyBERT). It utilizes cosine similarity between tokens (and n-grams) and the entire document to determine the relevance of terms. The most similar terms are then considered as keywords.

## References

- [KeyBERT: A Minimal Method for Keyphrase Extraction using BERT](https://github.com/MaartenGr/KeyBERT)
