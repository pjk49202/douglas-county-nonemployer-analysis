from pydoc import describe
import os, requests, pandas as pd, json, time, re

from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
load_dotenv()

API_KEY = os.environ["EIA_API_KEY"]
URL = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/"

CENSUS_API_KEY = os.environ["CENSUS_API_KEY"]

###Census API###
years = [2022, 2023, 2024]
data_frames_list = []

api_ready = True

if api_ready:
    for year in years:
        url = (
            f"https://api.census.gov/data/{year}/nonemp"
            "?get=NAME,NAICS2022,NAICS2022_LABEL,INDLEVEL,"
            "SECTOR,SUBSECTOR,NESTAB,NRCPTOT,NESTAB_F,NRCPTOT_F"
            f"&ucgid=0500000US08035"
            f"&key={CENSUS_API_KEY}"
            "&outputFormat=json"
        )

        try:
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                print(f"Skipping {year}: API error {response.status_code}")
                print(response.text[:500])
                continue

            yearly_data = response.json()

            # Census API returns column names in the first row.
            df_year = pd.DataFrame(
                yearly_data[1:],
                columns=yearly_data[0]
            )

            # Keep the reference year explicitly in our dataset.
            df_year["Year"] = year

            data_frames_list.append(df_year)
            #print(f"Successfully processed {year}: {len(df_year)} rows")

        except (requests.RequestException, ValueError) as error:
            print(f"Skipping {year}: {error}")

    if data_frames_list:
        final_df = pd.concat(data_frames_list, ignore_index=True)

        rename_map = {
            "NAME": "Geographic_Area",
            "NAICS2022": "NAICS_Code",
            "NAICS2022_LABEL": "Industry_Category",
            "NESTAB": "Establishment_Count",
            "NRCPTOT": "Total_Sales_Receipts",
            "NESTAB_F": "Establishment_Flag",
            "NRCPTOT_F": "Receipts_Flag",
        }

        final_df = final_df.rename(columns=rename_map)

        # Convert numeric measures while preserving unavailable values as NaN.
        for column in ["Establishment_Count", "Total_Sales_Receipts"]:
            final_df[column] = pd.to_numeric(
                final_df[column], errors="coerce"
            )

        print("\nCombined dataset created.")
        #print(f"Rows: {len(final_df)}")
        #print(final_df.head())

    else:
        final_df = pd.DataFrame()
        print("No data was retrieved.")

else:
    final_df = pd.DataFrame()
    print("API connection unavailable.")

# 3. View your newly cleaned schema
#print(final_df[['Geographic_Area', 'Industry_Category', 'NAICS_Code', 'Establishment_Count', 'Total_Sales_Receipts']].head(15))

# 1. Check total-row values by year
total_rows = final_df[final_df["NAICS_Code"] == "00"]

establishment_count_total = total_rows['Establishment_Count']
total_rows['Establishment_Count'] = establishment_count_total.round(0)
min_val = total_rows.loc[total_rows["Year"].idxmin(), "Establishment_Count"]
max_val = total_rows.loc[total_rows["Year"].idxmax(), "Establishment_Count"]
absolute_establishment_count_total = max_val  - min_val
percentage_establishment_count_total = (absolute_establishment_count_total / min_val) * 100
print(f"Absolute change in Establishment Count (2022-2024): {absolute_establishment_count_total:,}")
print(f"Percentage change in Establishment Count (2022-2024): {percentage_establishment_count_total:.2f}%")

#print(total_rows[['Year', 'Establishment_Count', 'Total_Sales_Receipts']].sort_values("Year"))

sales_recp_per_est_total = total_rows['Total_Sales_Receipts'] / total_rows['Establishment_Count']
total_rows['Sales_Receipts_Per_Establishment'] = sales_recp_per_est_total.round(1)

'''print(
    total_rows[
        ["Year", "Establishment_Count", "Total_Sales_Receipts", "Sales_Receipts_Per_Establishment"]
    ].sort_values("Year")
)'''

'''print("Average Sales Receipts per Establishment by Year:")
plt.plot(total_rows["Year"], total_rows["Sales_Receipts_Per_Establishment"])
plt.ylabel("Avg Sales Receipts per Establishment ($)")
plt.show()'''

# 2. Check how many rows exist at each industry level
'''print(
    final_df.groupby(["Year", "INDLEVEL"], dropna=False)
    .size()
    .unstack(fill_value=0)
)'''

# 3. Inspect the sector-level records (two-digit NAICS)
sector_df = final_df[
    (final_df["INDLEVEL"] == "2") &
    (final_df["NAICS_Code"] != "00")
].copy()

sales_recp_per_est = sector_df['Total_Sales_Receipts'] / sector_df['Establishment_Count']
sector_df['Sales_Receipts_Per_Establishment'] = sales_recp_per_est.round(1)
s_min_val = sector_df.loc[sector_df["Year"].idxmin(), "Total_Sales_Receipts"]
s_max_val = sector_df.loc[sector_df["Year"].idxmax(), "Total_Sales_Receipts"]
category_counts = sector_df.groupby(["Industry_Category", "Year"]).agg({"Establishment_Count": sum, "Total_Sales_Receipts": sum}).unstack("Year")

establishments = category_counts["Establishment_Count"]
receipts = category_counts["Total_Sales_Receipts"]

est_pct_change = (
    (establishments[2024] - establishments[2022])
    / establishments[2022]
) * 100

est_abs_change = establishments[2024] - establishments[2022]
#print("Absolute change in Establishment Count (2022-2024):", est_abs_change)
#print("Percentage change in Establishment Count (2022-2024):", est_pct_change)

receipts_pct_change = (
    (receipts[2024] - receipts[2022])
    / receipts[2022]
) * 100

receipts_abs_change = receipts[2024] - receipts[2022]
#print("Absolute change in Total Sales Receipts (2022-2024):", receipts_abs_change)
#print("Percentage change in Total Sales Receipts (2022-2024):", receipts_pct_change)

receipts_per_establishment_22 = receipts[2022] / establishments[2022]
receipts_per_establishment_24 = receipts[2024] / establishments[2024]
percent_change_in_receipts_per_establishment = (
    (receipts_per_establishment_24 - receipts_per_establishment_22)
    / receipts_per_establishment_22
) * 100
#print("Percentage Change in Receipts per Establishment (2022-2024):", percent_change_in_receipts_per_establishment)
#print("Receipts per Establishment (2022):", receipts_per_establishment_22)
#print("Receipts per Establishment (2024):", receipts_per_establishment_24)
#print("Change in Receipts per Establishment (2022-2024):", receipts_per_establishment_24 - receipts_per_establishment_22)
#print("Percentage Change in Receipts per Establishment (2022-2024):", percent_change_in_receipts_per_establishment )

per_category_change = ((establishments[2024] - establishments[2022]) / establishments[2022]) * 100
abs_category_change = ((establishments[2024] - establishments[2022]))

#print("Percentage change in Establishment Count by Industry Category (2022-2024):")
#print(per_category_change.sort_values(ascending=False).round(1))
#print("Absolute change in Establishment Count by Industry Category (2022-2024):")
#print(abs_category_change.sort_values(ascending=False).round(1))

industry_df = pd.DataFrame({
    "Industry_Category": category_counts.index,
    "Percentage_Change": per_category_change.values.round(1),
    "Receipts_Per_Establishment_2022": receipts_per_establishment_22.values.round(1),
    "Receipts_Per_Establishment_2024": receipts_per_establishment_24.values.round(1),
    "Absolute_Change": abs_category_change.values,
    "Receipts_Percentage_Change": receipts_pct_change.values.round(1),
    "Receipts_Absolute_Change": receipts_abs_change.values,
    "Percentage_Change_in_Receipts_per_Establishment": percent_change_in_receipts_per_establishment.values.round(1)
})

print(industry_df.sort_values("Receipts_Absolute_Change", ascending=False))
print(industry_df.to_excel("industry_df.xlsx", index=False))
industry_df.sort_values(
    "Receipts_Absolute_Change",
    ascending=False
).to_excel("Douglas_County_NES_Industry_Analysis.xlsx", index=False)

with pd.ExcelWriter("Douglas_County_NES_Analysis.xlsx") as writer:
    industry_df.to_excel(writer, sheet_name="Industry Changes", index=False)
    sector_df.to_excel(writer, sheet_name="Annual Industry Data", index=False)



total_receipts = total_rows.groupby("Year")["Total_Sales_Receipts"].sum()
total_receipts_change = total_receipts[2024] - total_receipts[2022]
print(f"Total Sales Receipts Change (2022-2024): ${total_receipts_change:,.0f}")
print(f"Total Sales Receipts (2022): ${total_receipts[2022]:,.0f}")
print(f"Total Sales Receipts (2024): ${total_receipts[2024]:,.0f}")








