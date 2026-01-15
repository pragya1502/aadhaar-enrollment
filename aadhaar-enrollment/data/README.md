# Dataset Information

## Overview
This project uses Aadhaar enrolment-related data provided as part of the **UIDAI Data Hackathon**.  
The data is used to analyze enrolment patterns and identify regional and demographic enrolment coverage gaps.

Due to data sensitivity and hackathon guidelines, raw datasets are **not uploaded to this repository**.

---

## Folder Structure

### raw/
- Contains original, unmodified Aadhaar enrolment datasets
- Files may include CSV/Excel formats provided by UIDAI
- These files are excluded from version control using `.gitignore`

### processed/
- Contains cleaned and transformed datasets generated during analysis
- Includes filtered data, aggregated tables, or derived features
- Files in this folder are created programmatically from the raw data

---

## Expected Data Attributes
Depending on availability, the dataset may include:
- Geographic information (State, District)
- Temporal information (Month, Year)
- Demographic details (Age group, Gender)
- Enrolment counts or related metrics

---

## Data Usage
The data is used exclusively for:
- Exploratory data analysis (EDA)
- Identification of enrolment patterns and trends
- Highlighting underserved regions or demographic groups
- Generating actionable insights to support inclusive Aadhaar enrolment

---

## Notes
- No personal or individual-level Aadhaar data is used
- Analysis is performed at an aggregated level only
- Raw data remains unchanged to preserve data integrity
