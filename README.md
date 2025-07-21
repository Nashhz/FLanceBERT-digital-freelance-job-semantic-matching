# FLanceBERT — Digital Freelance Job Semantic Matching

An intelligent freelance job matching system that uses **Sentence-BERT** to match user profiles with freelance job descriptions based on semantic similarity.

---

## 📌 Overview

**FLanceBERT** combines state-of-the-art NLP with practical web scraping and database management to help match freelancers to relevant jobs more accurately than simple keyword searches.
⚠️ Note: This project is still a work in progress. New features and improvements will be added and documented over time.
---

## 🚀 Key Features

- Uses **Sentence-BERT Transformer** to compute semantic similarity between freelancer profiles and job descriptions.
- Backend built with **Flask**, enabling secure user authentication, API endpoints, and real-time responses.
- Stores and manages data efficiently with an **Oracle XE** database.
- Includes a **web scraper** for **Freelancer.com**, developed using Selenium:
  - Scrapes live job listings.
  - Extracts details such as:
    - Job title
    - Job description
    - Skills required
  - Cleans unnecessary or broken data to ensure high-quality datasets.
  - Saves the cleaned data in CSV/JSON format.
- Trained model published to **Hugging Face** for reuse by other developers.
- Selected for industrial presentation to demonstrate innovative use of NLP and AI in job recommendation systems.

---

## 🗂️ Project Structure

FLanceBERT/
├── backend/ # Flask backend for API and authentication
├── models/ # Sentence-BERT training and inference scripts
├── scraper/ # Selenium-based web scraper
├── data/ # Example scraped datasets (CSV, JSON)
├── requirements.txt # Python dependencies
├── README.md # Project documentation


---

## ⚙️ Tech Stack

- **Python**
- **Sentence-BERT**, **Transformers (Hugging Face)**
- **Flask**
- **Selenium**
- **Oracle XE**
- **VSCode**

---
