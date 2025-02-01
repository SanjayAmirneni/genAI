import streamlit as st
import pandas as pd

## Configs
YEAR = 2023
CITIES = ['Tokyo', 'Osaka', 'Yokohama']


## Page Setup
st.set_page_config(page_title="Sales Dashboard", page_icon="📊")
st.title("Sales Dashboard")

## Load data

def load_data():
    return pd.read_csv("store_sales_2022-2023.csv").assign(
        date_of_sale = lambda df: pd.to_datetime(df["date_of_sale"]),
        month=lambda df: df["date_of_sale"].dt.month,
        year = lambda df: df["date_of_sale"].dt.year
    )

data = load_data()

# Calculate total revenue for each city and year, and then calculate the percentage change
city_revenues = data.groupby(['city',"year"])["sales_amount"].sum().unstack().assign(change=lambda x: x.pct_change(axis=1)[YEAR]*100)

## Key Metrics
# Display each city's data in separate columns
left_col,middle_col,right_col = st.columns(3)

with left_col:
    st.metric(label=CITIES[0], value=f" ${city_revenues.loc[CITIES[0], YEAR]:,.2f}", delta=f" ${city_revenues.loc[CITIES[0], 'change']:.2f}% vs. Last Year")
with middle_col:
    st.metric(label=CITIES[1], value=f" ${city_revenues.loc[CITIES[1],YEAR]:,.2f}", delta=f"${city_revenues.loc[CITIES[1],'change']:.2f}% vs.Last Year")
with right_col:
    st.metric(label=CITIES[2], value=f" ${city_revenues.loc[CITIES[2],YEAR]:,.2f}", delta=f"{city_revenues.loc[CITIES[2],'change']:.2f}% vs Last Year")

## Selection Fields
#City & Year selection
selected_city = st.selectbox("Select City", CITIES)
show_prev_year = st.toggle("Show Previous Year", False)
if show_prev_year:
    visualization_year = YEAR-1
else:
    visualization_year = YEAR
st.write(f"Visualizing data for {selected_city} in {visualization_year}")

## Tabs for analysis type
tab_month, tab_category = st.tabs(["Monthly Analysis", "Category Analysis"])

## Filter & Visulaize Data
with tab_month:
    filtered_data = data.query("city == @selected_city and year == @visualization_year").groupby("month")["sales_amount"].sum()
    st.bar_chart(filtered_data)

with tab_category:
    filtered_data = data.query("city == @selected_city and year == @visualization_year").groupby("product_category")["sales_amount"].sum()
    st.bar_chart(filtered_data)
