---
name: poetic_hymn_translator
description: Performs poetic and singable translations of Church Slavonic hymns (Sessional Hymns, Exapostilaria) to English, using Byzantine Greek as a semantic anchor while preserving Slavonic meter, phrasing, and syllable counts.
---

# Poetic Hymn Translator Skill Guidelines

When translating liturgical hymns poetically:

## 1. UTF-8 Strictness
All binary-to-text conversions (e.g., loading hymn plain-text from legacy file formats, reading API responses) must use `encoding='utf-8'` with `errors='strict'`. If a file is suspected of non-UTF-8 encoding, the translator must fall back to `chardet.detect()` or abort and log an explicit warning. Under no circumstances may an empty string or garbled text be silently substituted.

## 2. API Key and Configuration Loading
API key loader functions must exclusively read credentials from environment variables or a configuration file whose location is set via environment variable. Hardcoded filesystem paths for secrets are strictly prohibited and will be flagged by the anti-pattern searcher.

## 3. The Dual-Source Principle
* **Greek Source**: Use the Greek Menaion to establish the exact theological and semantic meaning, metaphors, and doctrinal nuances.
* **Slavonic Source**: Use the Church Slavonic text (e.g. Pochaiv 1761) to map English syllables, accentuation patterns, and sentence lengths. The target English text should align with the Slavonic structure to preserve singability and rhythm.

## 4. Metrical & Chant Formatting
* Do not force literal translations if they compromise poetic meter or rhythm.
* Insert musical breath marks and phrasing indicators (`*`) to show where cantors should pause or breathe.
* Translate the standard doxology exactly as: *"Glory be to the Father and to the Son and to the Holy Spirit, now and forever and unto the ages of ages. Amen."*
