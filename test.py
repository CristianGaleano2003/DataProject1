#!/usr/bin/env python
# coding: utf-8

# In[68]:


# We will extract our firs files
import os
import zipfile

import altair as alt
import pandas as pd
import streamlit as st
from kaggle.api.kaggle_api_extended import KaggleApi

# List with some values are error
errors = [
    "afghanistan & pakistan",
    "afghanistan & pakistan (excluding high income)",
    "afghanistan & pakistan (ida & ibrd)",
    "china",
    "china",
    "dominica",
    "early-demographic dividend",
    "east asia & pacific (excluding high income)",
    "east asia & pacific (ida & ibrd countries)",
    "east asia & pacific",
    "euro area",
    "europe & central asia",
    "europe & central asia (excluding high income)",
    "europe & central asia (ida & ibrd countries)",
    "european union",
    "heavily indebted poor countries (hipc)",
    "high income",
    "ida & ibrd total",
    "ida blend",
    "ida only",
    "ida total",
    "late-demographic dividend",
    "latin america & caribbean",
    "latin america & caribbean (excluding high income)",
    "latin america & the caribbean (ida & ibrd countries)",
    "least developed countries: un classification",
    "low & middle income",
    "low income",
    "lower middle income",
    "middle east",
    "middle east",
    "middle east",
    "middle income",
    "north africa",
    "north africa",
    "north africa",
    "oecd members",
    "post-demographic dividend",
    "pre-demographic dividend",
    "rb",
    "rep.",
    "rep.",
    "rep.",
    "south asia (ida & ibrd)",
    "sub-saharan africa (excluding high income)",
    "sub-saharan africa (ida & ibrd countries)",
    "the",
    "the",
    "africa eastern and southern",
    "africa western and central",
    "american samoa",
    "arab world",
    "aruba",
    "bermuda",
    "british virgin islands",
    "caribbean small states",
    "cayman islands",
    "central europe and the baltics",
    "channel islands",
    "curacao",
    "faroe islands",
    "fed. rep.",
    "fragile and conflict affected situations",
    "french polynesia",
    "gibraltar",
    "greenland",
    "guam",
    "hong kong sar",
    "ibrd only",
    "isle of man",
    "macao sar",
    "new caledonia",
    "north america",
    "northern mariana islands",
    "not classified",
    "other small states",
    "pacific island small states",
    "puerto rico (us)",
    "sint maarten (dutch part)",
    "small states",
    "south asia",
    "st. martin (french part)",
    "sub-saharan africa",
    "turks and caicos islands",
    "upper middle income",
    "virgin islands (u.s.)",
    "west bank and gaza",
    "world",
    "macao",
    "middle east north africa afghanistan & pakistan",
]

changes = {
    "bahamas the": "bahamas",
    "bahamas, the": "bahamas",
    "congo dem. rep.": "congo",
    "congo, rep.": "congo",
    "congo, dem. rep.": "congo",
    "gambia the": "gambia",
    "hong kong sar china": "hong kong",
    "iran islamic rep.": "iran islamic",
    "korea rep.": "korea",
    "middle east north africa afghanistan & pakistan": "middle east north africa afghanistan & pakistan",
    "middle east north africa afghanistan & pakistan (excluding high income)": "middle east north africa afghanistan & pakistan",
    "korea dem. people's rep.": "korea",
    "somalia fed. rep.": "somalia",
    "middle east north africa afghanistan & pakistan (ida & ibrd)": "middle east north africa afghanistan & pakistan",
    "venezuela rb": "venezuela",
    "cote d'ivoire": "ivory coast",
    "egypt, arab rep.": "egypt",
    "micronesia, fed. sts.": "micronesia",
    "hong kong sar, china": "hong kong",
    "gambia, the": "gambia",
    "iran, islamic rep.": "iran",
    "korea, rep.": "korea",
    "macao sar, china": "macao",
    "middle east, north africa, afghanistan & pakistan": "middle east north africa afghanistan & pakistan",
    "middle east, north africa, afghanistan & pakistan (excluding high income)": "middle east north africa afghanistan & pakistan",
    "korea, dem. people's rep.": "korea",
    "somalia, fed. rep.": "somalia",
    "middle east, north africa, afghanistan & pakistan (ida & ibrd)": "middle east north africa afghanistan & pakistan",
    "venezuela, rb": "venezuela",
}

# Path to the zip file
zip_path = (
    r"C:\Users\Cristian des\Downloads\API_VC.IHR.PSRC.P5_DS2_en_csv_v2_115572.zip"
)

# Define the path to extract the files
extract_path = r"C:\Users\Cristian des\OneDrive\Documentos\Programación\Proyecto_propios_Data\Python\DataProject1\data"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    files = zip_ref.namelist()
    print("Archivos encontrados:", files)

    # Filter, exclude filed that begin with API
    files_to_extract = [f for f in files if f.startswith("API")]

    # To extract the files who fulfill the conditions
    for f in files_to_extract:
        zip_ref.extract(f, extract_path)
        print(f"Extraído: {f}")


# In[69]:


# Now we will convert each file to a dataframe and look the head of each one to see what we have in each file

# Path of the folder where we have the files downloaded from Data Bank
folder = r"C:\Users\Cristian des\OneDrive\Documentos\Programación\Proyecto_propios_Data\Python\DataProject1\data"
archivos = os.listdir("./datos")

# Definite the appi in Kaggle and get the data from the dataset
api = KaggleApi()
api.authenticate()
api.dataset_download_files("nitindatta/finance-data", path="./datos", unzip=True)

# List all fields in the Data carpet.
Tabla = [
    pd.read_csv(os.path.join(folder, f), skiprows=4)
    for f in os.listdir(folder)
    if f.endswith(".csv")
]

# Create a single DataFrame by concatenating all the individual DataFrames
df_Data = pd.concat(Tabla, ignore_index=True)
df_Data1 = df_Data[~df_Data["Country Name"].str.strip().str.lower().isin(errors)]
df_Data1["Country Name"] = (
    df_Data1["Country Name"].str.strip().str.lower().replace(changes)
)
df_data_long = df_Data1.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="Value",
)
df_data_long["Country Name"] = df_data_long["Country Name"].str.strip().str.lower()
df_data_long = df_data_long[df_data_long["Year"] != "Unnamed: 70"]
df_data_long["Year"] = pd.to_numeric(df_data_long["Year"], errors="coerce")
df_data_long = df_data_long.dropna(subset=["Year"])
df_data_long["Year"] = df_data_long["Year"].astype(int)


# Create a dataframe from the files obtained from Kaggle's dataset
df_financeData = pd.read_csv("./datos/Finance_data.csv")
df_OriginalData = pd.read_csv("./datos/Original_data.csv")
df_country = pd.read_excel("./datos/countries.xlsx")
df_country["Country"] = df_country["Country"].str.strip().str.lower()

# Merge to know the region of each country
df_data_long = df_data_long.merge(
    df_country[["Country", "Region"]],
    left_on="Country Name",
    right_on="Country",
    how="left",
)

df_data_long["Group"] = (
    df_data_long["Country Name"] + " - " + df_data_long["Indicator Name"]
)

# Save the countries without region to an Excel file
df_data_long[["Country Name", "Region"]][
    df_data_long["Region"].isnull()
].drop_duplicates().to_excel("./countries_without_region.xlsx", index=False)

# In[70]:


print(df_data_long.head(5))


# In[72]:


""" 
We will define the questions to answer:

- Are there any relation ship between the indicators of the World Bank Data?
- Wich is the country with the best economic performance in the last 10 years?
- Are there a relationship between the economic performance and security indicators? 
- Are there any relaionship between the indicators of the World Bank Data and the Data's dataframe?
"""

# - Are there any relation ship between the indicators of the World Bank Data?

st.title("Countries indicators")

modo = st.radio("Do you want to group by:", ["Country", "Region"])

indicator = st.multiselect(
    "Select an indicator", df_data_long["Indicator Name"].unique()
)

if modo == "Country":
    country = st.multiselect("Select a country", df_data_long["Country Name"].unique())
    df_plot = df_data_long[
        df_data_long["Country Name"].isin(country)
        & df_data_long["Indicator Name"].isin(indicator)
    ].copy()
    df_plot["Grupo"] = df_plot["Country Name"] + " - " + df_plot["Indicator Name"]
else:
    region = st.multiselect("Select a region", df_data_long["Region"].unique())
    df_region = df_data_long[
        df_data_long["Region"].isin(region)
        & df_data_long["Indicator Name"].isin(indicator)
    ].copy()
    df_region = df_region.groupby(["Year", "Region", "Indicator Name"], as_index=False)[
        "Value"
    ].mean()
    df_region["Grupo"] = df_region["Region"] + " - " + df_region["Indicator Name"]
    df_plot = df_region

chart = (
    alt.Chart(df_plot)
    .mark_line(point=True)
    .encode(
        x="Year:O", y="Value:Q", color="Grupo:N", tooltip=["Year", "Grupo", "Value"]
    )
)

st.altair_chart(chart, use_container_width=True)
