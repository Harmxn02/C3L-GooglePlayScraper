# C3L - Google Play Scraper

A collection of code to fetch the Google Play Store data using the `google-play-scraper` library. The data is then preprocessed and exported to various formats.

## Overview

In this repository, you will find a Python script that scrapes Google Play Store data for the category "Health & Fitness". The script collects the information of 30 apps. The Jupyter notebook then preprocesses the data and exports it to:

- CSV
- JSON
- Excel
- Parquet
- Pickle

## Requirements

- Python

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Harmxn02/C3L-GooglePlayScraper.git
    cd C3L-GooglePlayScraper
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The datasets are already available in the `data/fetched` folder. However, if you want to scrape the data again, follow these steps:

### Run the scraper

```bash
python main.py
```

This will scrape the data, and export a CSV file to `data/fetched/health_and_fitness_apps.csv`

### Run the Jupyter notebook

Open it, and run the cells

This will preprocess the data and export it to the following formats:

- CSV
- JSON
- Excel
- Parquet
- Pickle

## License

Feel free to use this code for your own projects, however you like.

Follow the license of the `google-play-scraper` library for any restrictions. Same applies to the `pandas` library.
