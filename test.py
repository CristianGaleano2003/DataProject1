#!/usr/bin/env python
# coding: utf-8

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
zip_path = (r"./ZIP_file")

# Define the path to extract the files
extract_path = r"./data"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    files = zip_ref.namelist()
    #print("Archivos encontrados:", files)

    # Filter, exclude filed that begin with API
    files_to_extract = [f for f in files if f.startswith("API")]

    # To extract the files who fulfill the conditions
    for f in files_to_extract:
        zip_ref.extract(f, extract_path)
        #print(f"Extraído: {f}")

# Now we will convert each file to a dataframe and look the head of each one to see what we have in each file

# Path of the folder where we have the files downloaded from Data Bank
folder = r"./data"
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
df_Data1["Country Name"] = (df_Data1["Country Name"].str.strip().str.lower().replace(changes))
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
df_financeData = df_financeData.melt(id_vars= ["gender", "age"], var_name="Indicator Name", value_name="Value")
df_financeData["age"] = df_financeData["age"].astype(int)



df_OriginalData = pd.read_csv("./datos/Original_data.csv")
df_OriginalData = df_OriginalData.melt(id_vars= ["GENDER", "AGE"], var_name="Indicator Name", value_name="Value")
df_OriginalData["AGE"] = df_OriginalData["AGE"].astype(int)


df_country = pd.read_excel("./datos/countries.xlsx")
df_country["Country"] = df_country["Country"].str.strip().str.lower()

# Merge to know the region of each country
df_data_long = df_data_long.merge(
    df_country[["Country", "Region"]],
    left_on="Country Name",
    right_on="Country",
    how="left",
)

df_data_long["Group"] = (df_data_long["Country Name"] + " - " + df_data_long["Indicator Name"])

# Save the countries without region to an Excel file
df_data_long[["Country Name", "Region"]][df_data_long["Region"].isnull()].drop_duplicates().to_excel("./countries_without_region.xlsx", index=False)

# - Are there any relation ship between the indicators of the World Bank Data?

st.title("Indicators")

modo = st.radio("Do you want to group by:", ["Country", "Region"])

indicator = st.multiselect(
    "Select an indicator", df_data_long["Indicator Name"].unique()
)

if modo == "Country":
    st.subheader("Country")
    country = st.multiselect("Select a country", df_data_long["Country Name"].unique())
    df_plot = df_data_long[
        df_data_long["Country Name"].isin(country)
        & df_data_long["Indicator Name"].isin(indicator)
    ].copy()
    df_plot["Grupo"] = df_plot["Country Name"] + " - " + df_plot["Indicator Name"]
else:
    st.subheader("Region")
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

st.subheader("Finance Data")

min = df_financeData["age"].min()
max = df_financeData["age"].max()

ind = st.multiselect("Select indicators to see", df_financeData["Indicator Name"].unique(), key="Indicator")
gender = st.multiselect("Select gender to see", df_financeData["gender"].unique(), key="gender")
age = st.slider("Select age range",min_value=min,max_value=max,value=(min, max), key="age") 

df_finance = df_financeData[
    df_financeData["Indicator Name"].isin(ind) &
    df_financeData["gender"].isin(gender) &
    df_financeData["age"].isin(age)
].copy()

df_finance = df_finance.groupby(["gender","age","Indicator Name"], as_index=False)["Value"].count()

chart = (
    alt.Chart(df_finance)
    .mark_bar()
    .encode(
        x="Indicator Name:N",   # cada indicador será una barra
        y="Value:Q",            # altura de la barra
        color="Indicator Name:N", # color por indicador
        column="gender:N",      # divide el gráfico en columnas por género
        tooltip=["gender", "age", "Indicator Name", "Value"]
    )
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Original Data")

MIN = df_OriginalData["AGE"].min()
MAX = df_OriginalData["AGE"].max()

IND= st.multiselect("Select indicators to see", df_OriginalData["Indicator Name"].unique(), key="INDICATOR")
GENDER = st.multiselect("Select gender to see", df_OriginalData["GENDER"].unique(), key="GENDER")
AGE = st.slider("Select age range", min_value=MIN, max_value=MAX, value=(MIN, MAX), key="AGE")

df_original = df_OriginalData[
    df_OriginalData["Indicator Name"].isin(IND) &
    df_OriginalData["GENDER"].isin(GENDER) &
    df_OriginalData["AGE"].isin(AGE)
].copy()

df_original = df_original.groupby(["GENDER","AGE","Indicator Name"], as_index=False)["Value"].count()

chart = (
    alt.Chart(df_original)
    .mark_bar()
    .encode(
        x="Indicator Name:N",   # cada indicador será una barra
        y="Value:Q",            # altura de la barra
        color="Indicator Name:N", # color por indicador
        column="GENDER:N",      # divide el gráfico en columnas por género
        tooltip=["GENDER", "AGE", "Indicator Name", "Value"]
    )
)
st.altair_chart(chart, use_container_width=True)