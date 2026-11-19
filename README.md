# douglas-county-nonemployer-analysis

# Douglas County Nonemployer Business Analysis (2022–2024)

## Project Overview

This project examines nonemployer business activity in Douglas County, Colorado, using data from the U.S. Census Bureau's Nonemployer Statistics (NES) program.

The objective is to identify industry-level trends in establishment counts, total business receipts, and receipts per establishment between 2022 and 2024.

Nonemployer businesses are establishments without paid employees, including many freelancers, independent contractors, and self-employed individuals.

## Tools and Technologies

- **Python:** Census API data extraction and processing
- **pandas:** Data cleaning, transformation, aggregation, and analysis
- **Excel:** Data visualization and charts
- **U.S. Census Bureau API:** Nonemployer Statistics data source

## Key Findings

- Douglas County gained **2,142 nonemployer establishments (+5.45%)** between 2022 and 2024.
- Total nominal business receipts increased by **$227.3 million (+9.5%)**.
- Professional, scientific, and technical services experienced the largest absolute increase in establishments (+538) and receipts (+$38.4 million).
- Educational services experienced particularly strong receipts growth (+34.5%), outpacing establishment growth (+6.1%).
- Manufacturing and mining were the only two industry sectors to experience declines in establishment counts, total receipts, and receipts per establishment.

## Methodology

Data for 2022–2024 was retrieved using the Census Bureau API and processed with Python and pandas.

Industry comparisons were conducted at the two-digit NAICS sector level. The analysis calculated absolute and percentage changes in establishment counts, total receipts, and average receipts per establishment.

The 2022–2024 period was selected to maintain consistent industry classifications under the 2022 NAICS system and avoid comparability issues with earlier datasets.

## Project Files

- `Census_SBA.py` — Python script for retrieving and analyzing Census data.
- `SmallBus_analysis_project.pdf` — Full analytical report, including Excel visualizations and conclusions.
- `Douglas_County_NES_Analysis.xlsx` — Supporting industry data and calculations.

## Limitations

The analysis covers only Douglas County and does not compare results with neighboring counties. Receipts are reported in nominal dollars without adjustment for inflation. The three-year period also limits conclusions about longer-term economic trends.

Establishment counts and receipts are indicators of business activity, not direct measures of profitability or overall business health.

## Data Source

U.S. Census Bureau — [Nonemployer Statistics (NES)](https://www.census.gov/programs-surveys/nonemployer-statistics.html)

**Geographic scope:** Douglas County, Colorado  
**Period:** 2022–2024

*This is an independent analytical project and is not affiliated with or endorsed by the U.S. Census Bureau.*
