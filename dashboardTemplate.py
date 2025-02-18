import streamlit as st              #install on your terminal using pip install streamlit
import pandas as pd                 #install on your terminal using pip install pandas
import matplotlib.pyplot as plt     #install on your terminal using pip install matplotlib
import plotly.express as px         #install on your terminal using pip install plotly
import os                           #install on your terminal using pip install xlrd
import warnings

warnings.filterwarnings("ignore")

#Gives tab a title and icon
--> Code Here

# Gives the website a header
--> Code Here

# Removes some spacing from the top
--> Code Here

#Creating a file upload section
--> Code Here

# If a file is uploaded, display the file name
--> Code Here
--> Code Here
--> Code Here
--> Code Here

# If no file is uploaded, use default file
else:
    os.chdir(r"C:\Users\celes\OneDrive\Desktop\Data Analysis Workshop")
    df = pd.read_excel("Sample - Superstore.xls")

#Create filtering by date
--> Code Here
--> Code Here

# Getting the min and max date
--> Code Here
--> Code Here

# Display start date
--> Code Here
--> Code Here

# Display end date
--> Code Here
--> Code Here

# Filter data by date
--> Code Here

# Create a sidebar for filtering
--> Code Here

# Create for Region
--> Code Here
--> Code Here
--> Code Here
--> Code Here
--> Code Here

# Create for State
--> Code Here
--> Code Here
--> Code Here
--> Code Here
--> Code Here

# Create for City
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())

# Filter the data based on Region, State and City
if not region and not state and not city:
    filtered_data = df
elif not state and not city:
    filtered_data = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_data = df[df["State"].isin(state)]
elif state and city:
    filtered_data = df3[df3["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_data = df3[df3["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_data = df3[df3["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_data = df3[df3["City"].isin(city)]
else:
    filtered_data = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Filter by category and get sum of sales for each category
--> Code Here

# Create sales by category
with col1:
    --> Code Here
    fig = px.bar(category_df, x = "Category", y = "Sales", color = "Category", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]], template = "seaborn")
    --> Code Here

# Create sales by region
with col2:
    --> Code Here
    --> Code Here
    --> Code Here
    --> Code Here

# Download the filtered data
# Create new columns
--> Code Here

# Create download button for category data
--> Code Here
    --> Code Here
    --> Code Here
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name= "Category.csv", mime = "text/csv", help = "Click here to download the data as a csv file")

# Create download button for region data
with cl2:
    --> Code Here
        # Filter by region then sum the sales by region
        --> Code Here
        --> Code Here
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name= "Region.csv", mime = "text/csv", help = "Click here to download the data as a csv file")

# Filter by Month and Year
--> Code Here

# Create time series analysis
--> Code Here
# Create a line chart for time series data
linechart = pd.DataFrame(filtered_data.groupby(filtered_data["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
--> Code Here
--> Code Here

# Create download button for time series data
with st.expander("View Data of TimeSeries"):
    # Transposes the data and styles it
    --> Code Here
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name="TimeSeries.csv", mime = "text/csv", help = "Click here to download the data as a csv file")

# Create a tree map based on Region, Category, Sub-Category
st.subheader("Hierarchical View of Sales using Tree Map")
--> Code Here
--> Code Here
--> Code Here

# Create a pie chart for Segment, Category, Ship Mode
# Create 3 charts
--> Code Here
with chart1:
    --> Code Here
    --> Code Here
    --> Code Here
    --> Code Here

with chart2:
    --> Code Here
    --> Code Here
    --> Code Here
    --> Code Here

with chart3:
    --> Code Here
    --> Code Here
    --> Code Here
    --> Code Here

# Create a table of sales by month and sub-category
import plotly.figure_factory as ff
st.subheader(":point_right: Table of Sales by Month and Sub-Category")

# Creates a table with the first 5 rows of the data
with st.expander("Summary Table"):
    df_sample = df[0:5][["Region","Category","Sub-Category","Sales","Profit","Quantity"]]
    --> Code Here
    --> Code Here
    # Create Month by Sub-Category 
    --> Code Here
    --> Code Here
    --> Code Here
    --> Code Here

# Create a scatter plot
--> Code Here
--> Code Here
--> Code Here

# Create a download button
with st.expander("View Data"):
    st.write(filtered_data.iloc[:500,1:20:2].style.background_gradient(cmap = "Oranges"))

# Create a download button full dataset
csv = df.to_csv(index = False).encode('utf-8')
st.download_button("Download Full DataSet", data = csv, file_name = "Data.csv", mime = "text/csv",
                   help = "Click here to download the data as a csv file")
