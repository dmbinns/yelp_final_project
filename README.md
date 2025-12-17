# Yelp Ice Cream Shops in Utah
STAT 386 Final Project

This repository contains a Python package and supporting materials for collecting, cleaning, analyzing, and visualizing Yelp data for ice cream shops in Utah County and Salt Lake County. The project uses the Yelp Fusion API to gather original data and examines how review volume, delivery options, price level, and city relate to business ratings.

The final project includes a reusable Python package, a Streamlit application, and full documentation with a tutorial hosted on GitHub Pages.

---

## Repository Structure

.
docs/
src/yelp_final_project/
src/yelp_final_project/__init__.py
src/yelp_final_project/cleaning.py
src/yelp_final_project/analysis.py
src/yelp_final_project/streamlit_app.py
tests/
yelp_data_collection.ipynb
data/yelp_icecream_shops_utah.csv
pyproject.toml
README.md


---

## Data Collection

The file `yelp_data_collection.ipynb` contains the code used to collect data from the Yelp Fusion API. This notebook handles API authentication, pagination, and searching for ice cream shops across multiple cities in Utah County and Salt Lake County.

The raw data collected from the API is saved as `yelp_icecream_shops_utah.csv`. Each row represents an ice cream business and includes information such as rating, review count, price level, services offered, and geographic location.

---

## Python Package

The Python package is located in:

src/yelp_final_project

This package provides functions for:
- Cleaning and preparing raw Yelp data
- Performing exploratory data analysis
- Supporting visualizations used in the Streamlit app

A full tutorial demonstrating how to install and use the package is available on the project’s GitHub Pages site.

---

## Documentation and Tutorial

Complete documentation, including function references, a step-by-step tutorial, and the written project report, is hosted on GitHub Pages.

Documentation and tutorial link:
https://dmbinns.github.io/yelp_final_project

---

## Testing

The `tests` directory contains unit tests for the data cleaning and analysis functions included in the Python package.

---

## Streamlit Application

The Streamlit application is located at:

src/yelp_final_project/streamlit_app.py

The app provides interactive visualizations of ice cream shop ratings across Utah County and Salt Lake County, allowing users to explore relationships between ratings and review volume, price level, service type, and city.

---

## Project Context

This project was completed as the STAT 386 Final Project and follows the full data science pipeline:
1. Data collection via an external API
2. Data cleaning and preparation
3. Exploratory data analysis
4. Communication through documentation, visualization, and reporting

---


