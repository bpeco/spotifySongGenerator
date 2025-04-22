# 🎵 Spotify Song Generator

This project is an educational experiment that explores the use of large language models (LLMs) to generate new songs based on existing lyrics. The pipeline processes real songs, enriches them with thematic and emotional metadata, and generates new lyrics with the help of an LLM.

---

## ⚙️ Pipeline Overview

### 1. Data Extraction
- **Lyrics source:** `letras.com` (manual scraping)
- **Metadata source:** Spotify audio features were not used due to API deprecation.
- The current version processes 10 songs from a fixed artist (**Jorge Drexler**).

### 2. Enriching with LLM
Each song is processed to extract:
- Thematic tags (e.g., `"Love"`, `"Transformation"`)
- Mood classification (e.g., `"romantic"`)
- Structural metrics (lines, paragraphs)

### 3. Song Generation
- The user defines desired attributes.
- The system selects similar songs.
- A new song is generated using the LLM.

---

## 📁 Project Structure

- `01-get_connection.py`: handles secrets (excluded from Git)
- `02-process_songs.py`: scrapes and prepares raw lyrics
- `03-main.py`: runs the full pipeline
- `llm_helper.py`: prompt engineering and LLM helpers
- `song_generator.py`: generates the new lyrics
- `few_shot.py`: few-shot examples for prompting
- `raw_songs.json`: input lyrics
- `processed_songs.json`: enriched song data

---

## 🚧 Current Limitations

- Only supports one fixed artist.
- No audio features are used due to deprecated Spotify API.
- No user interface yet (inputs are hardcoded).

---

## 📌 Roadmap

- [ ] Allow user to choose artist (from 10 preselected ones).
- [ ] Let the user define how many songs to process.
- [ ] Add semantic similarity filtering (clustering, vector DBs).
- [ ] Provide web interface for interaction.

---

## 🛑 Legal Notice

- This is a **non-commercial** educational project.
- All rights for the lyrics belong to their **authors and publishers**.
- Lyrics and data were obtained from `letras.com` and `Spotify`.
- No redistribution or commercial use of derived works is intended.

---

## 🧠 Inspired by

- Creative potential of LLMs
- Intersection of music and generative AI
- Personalized content generation projects

---
