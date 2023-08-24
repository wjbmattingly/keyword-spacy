[![GitHub Stars](https://img.shields.io/github/stars/wjbmattingly/keyword?style=social)](https://github.com/wjbmattingly/keyword-spacy)
[![PyPi Version](https://img.shields.io/pypi/v/keyword-spacy)](https://pypi.org/project/keyword-spacy/0.0.1/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/keyword-spacy)](https://pypi.org/project/keyword-spacy/0.0.1/)

# 🔑 Keyword spaCy

![keyword spacy](https://github.com/wjbmattingly/keyword-spacy/blob/main/images/keyword-spacy-logo.png?raw=true)

Keyword spaCy is a spaCy pipeline component for extracting keywords from text using cosine similarity. The basis for this comes from [KeyBERT: A Minimal Method for Keyphrase Extraction using BERT](https://github.com/MaartenGr/KeyBERT), a transformer-based approach to keyword extraction. The methods employed by Keyword spaCy follow this methodology closely. It allows users to specify the range of n-grams to consider and can operate in a strict mode, which limits results to the specified n-gram range.

## Installation

Before using Keyword spaCy, make sure you have spaCy installed:

```
pip install keyword-spacy
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
nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10, "min_ngram": 3, "max_ngram": 3, "strict": True})
```

Now you can process text and extract keywords:

```python
text = "Natural language processing is a fascinating domain of artificial intelligence. It allows computers to understand and generate human language."
doc = nlp(text)
print("Top Keywords:", doc._.keywords)
```
Output:
```
Top Keywords: ['generate human language', 'Natural language processing']
```

Each token that is not a punctuation also receives a special attribute `._.keyword_value`, this is the value of a given word's similarity to the `doc.vector`. This may be helpful for other downstream tasks.

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
