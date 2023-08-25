[![GitHub Stars](https://img.shields.io/github/stars/wjbmattingly/keyword-spacy?style=social)](https://github.com/wjbmattingly/keyword-spacy)
[![PyPi Version](https://img.shields.io/pypi/v/keyword-spacy)](https://pypi.org/project/keyword-spacy/0.0.1/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/keyword-spacy)](https://pypi.org/project/keyword-spacy/0.0.1/)

![keyword spacy](https://github.com/wjbmattingly/keyword-spacy/blob/main/images/keyword-spacy-logo.png?raw=true)

# 🔑 Keyword spaCy

Keyword spaCy is a spaCy pipeline component for extracting keywords from text using cosine similarity. The basis for this comes from [KeyBERT: A Minimal Method for Keyphrase Extraction using BERT](https://github.com/MaartenGr/KeyBERT), a transformer-based approach to keyword extraction. The methods employed by Keyword spaCy follow this methodology closely. It allows users to specify the range of n-grams to consider and can operate in a strict mode, which limits results to the specified n-gram range.

## Transformer Model Integration

Keyword spaCy has built-in support for spaCy's transformer models. When a transformer model is present in the pipeline, the component fetches the transformer's output vectors for tokens and uses them for keyword extraction. This ensures that you benefit from the contextual embeddings provided by models like BERT, leading to more accurate keyword extraction.

## Installation

Before using Keyword spaCy, ensure spaCy is installed:

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
nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10, "min_ngram": 3, "max_ngram": 3, "strict": True, "top_n_sent": 3})
```

Now you can process text and extract keywords:

```python
text = "Natural language processing is a fascinating domain of artificial intelligence. It allows computers to understand and generate human language."
doc = nlp(text)
print("Top Document Keywords:", doc._.keywords)
for sent in doc.sents:
    print(f"Sentence: {sent.text}")
    print("Top Sentence Keywords:", sent._.sent_keywords)
```

## Configuration

The `KeywordExtractor` can be configured using the following parameters:

- `top_n`: The number of top keywords to extract for the entire document.
- `min_ngram`: The minimum size for n-grams.
- `max_ngram`: The maximum size for n-grams.
- `strict`: If set to `True`, only n-grams within the `min_ngram` to `max_ngram` range are considered. If `False`, individual tokens and the specified range of n-grams are considered.
- `top_n_sent`: The number of top keywords to extract for each sentence.

## Methodology

Keyword spaCy employs cosine similarity between tokens (and n-grams) and the entire document or sentence, as specified, to determine the relevance of terms. The terms with the highest similarity scores are then considered as keywords. This methodology allows for efficient keyword extraction even from large documents and is especially potent when paired with transformer models.

## References

- [KeyBERT: A Minimal Method for Keyphrase Extraction using BERT](https://github.com/MaartenGr/KeyBERT)
