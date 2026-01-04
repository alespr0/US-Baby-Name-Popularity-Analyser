# US Baby Name Popularity Analyser

## Overview

The **US Baby Name Popularity Analyser** is an interactive data application built with **Python** and **Streamlit** that allows users to explore how baby name popularity in the United States has evolved over time. By entering a name and a year of birth, users can access national-level statistics on name popularity, gender distribution, and historical trends.

## Key Questions

The application helps answer questions such as:

- How popular was a given name in the United States in a specific year?
- What was the national ranking of that name compared to others?
- How was the name used across genders in that year?
- How has the popularity of the name changed over time?


## App Launch
### On your browser:
[Click here](https://us-baby-name-popularity-analyser.streamlit.app/)
### On your machine:
1. Clone this repository
2. Make sure Python 3.10+ and Streamlit are installed
3. Type in your terminal

```console
streamlit run baby_app.py
```
---
## Data Source and Preparation

The data is based on [publicly available U.S. baby name records](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-state-and-district-of-columbia-data), originally reported at the **state, year, and sex** level and containing several million observations.

For this project, the data was preprocessed to create a **national-level dataset**:

- Counts are aggregated across all states
- Data is retained by:
  - `name`
  - `year`
  - `sex`
  - `name_count`

The processed dataset is stored in **Parquet format**, which significantly improves loading speed and reduces storage size compared to CSV.

> State-level data is excluded from this repository to keep the project lightweight and suitable for cloud deployment.


## Features

- **National popularity ranking** by year  
- **Gender usage breakdown** for selected names  
- **Popularity change over time**  
- **Interactive trend visualization**  


## Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **PyArrow / Parquet**
