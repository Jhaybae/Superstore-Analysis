import streamlit as st              #install on your terminal using pip install streamlit
import pandas as pd                 #install on your terminal using pip install pandas
import matplotlib.pyplot as plt     #install on your terminal using pip install matplotlib
import plotly.express as px         #install on your terminal using pip install plotly
import os                           #install on your terminal using pip install xlrd
import warnings

warnings.filterwarnings("ignore")

#Gives tab a title and icon
st.set_page_config(page_title = "Superstore~~", page_icon = ":bar_chart:", layout = "wide")

# Gives the website a header
st.title(" :bar_chart: Sample Superstore EDA")

# Removes some spacing from the top
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

#Creating a file upload section
fl = st.file_uploader(":file_folder: Upload a file", type = ["csv", "txt", "xlsx", "xls"])\

# If a file is uploaded, display the file name
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
# If no file is uploaded, use default file
else:
    os.chdir(r"C:\Users\celes\OneDrive\Desktop\Data Analysis Workshop")
    df = pd.read_excel("Sample - Superstore.xls")

#Create filtering by date
col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date
startDate = pd.to_datetime(df["Order Date"].min())
endDate = pd.to_datetime(df["Order Date"]).max()

# Display start date
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

# Display end date
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Filter data by date
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# Create a sidebar for filtering
st.sidebar.header("Choose your filter: ")

# Create for Region
region = st.sidebar.multiselect("Pick the Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Create for State
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

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
category_df = filtered_data.groupby(by = ["Category"], as_index = False)["Sales"].sum()

# Create sales by category
with col1:
    st.subheader("Sales by Category")
    fig = px.bar(category_df, x = "Category", y = "Sales", color = "Category", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)

# Create sales by region
with col2:
    st.subheader("Sales by Region")
    fig = px.pie(filtered_data, values = "Sales", names = "Region", template = "seaborn", hole = 0.5)
    fig.update_traces(text= filtered_data["Region"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True, height = 200)

# Download the filtered data
# Create new columns
cl1, cl2 = st.columns(2)

# Create download button for category data
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name= "Category.csv", mime = "text/csv", help = "Click here to download the data as a csv file")

# Create download button for region data
with cl2:
    with st.expander("Region_ViewData"):
        # Filter by region then sum the sales by region
        region = filtered_data.groupby(by = ["Region"], as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name= "Region.csv", mime = "text/csv", help = "Click here to download the data as a csv file")

# Filter by Month and Year
filtered_data["month_year"] = filtered_data["Order Date"].dt.to_period("M")

# Create time series analysis
st.subheader("Time Series Analysis")
# Create a line chart for time series data
linechart = pd.DataFrame(filtered_data.groupby(filtered_data["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x ="month_year", y="Sales", labels={"Sales": "Amount"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

# Create download button for time series data
with st.expander("View Data of TimeSeries"):
    # Transposes the data and styles it
    st.write(linechart.T.style.background_gradient(cmap="Greens"))
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name="TimeSeries.csv", mime = "text/csv", help = "Click here to download the data as a csv file")

# Create a tree map based on Region, Category, Sub-Category
st.subheader("Hierarchical View of Sales using Tree Map")
fig3 = px.treemap(filtered_data, path = ["Region", "Category", "Sub-Category"], values = "Sales", color = "Sub-Category", hover_data = ["Sales"])
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

# Create a pie chart for Segment, Category, Ship Mode
# Create 3 charts
chart1, chart2, chart3 = st.columns(3)
with chart1:
    st.subheader("Sales by Segment")
    fig = px.pie(filtered_data, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_data["Segment"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Sales by Category")
    fig = px.pie(filtered_data, values = "Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_data["Category"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

with chart3:
    st.subheader("Sales by Ship Mode")
    fig = px.pie(filtered_data, values = "Sales", names = "Ship Mode", template = "seaborn")
    fig.update_traces(text = filtered_data["Ship Mode"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

# Create a table of sales by month and sub-category
import plotly.figure_factory as ff
st.subheader(":point_right: Table of Sales by Month and Sub-Category")

# Creates a table with the first 5 rows of the data
with st.expander("Summary Table"):
    df_sample = df[0:5][["Region","Category","Sub-Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)
    # Create Month by Sub-Category
    st.markdown("Month by Sub-Category Table")
    filtered_data["month"] = filtered_data["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(filtered_data, index="Sub-Category", columns="month", values="Sales")
    st.write(sub_category_Year.style.background_gradient(cmap="viridis"))

# Create a scatter plot
data1 = px.scatter(filtered_data, x="Sales", y="Profit", size="Quantity")
data1.update_layout(title="Relationship between Sales, Profit and Quantity", xaxis_title="Sales", yaxis_title="Profit", template="plotly_dark")
st.plotly_chart(data1, use_container_width=True)

# Create a download button
with st.expander("View Data"):
    st.write(filtered_data.iloc[:500,1:20:2].style.background_gradient(cmap = "Oranges"))

# Create a download button full dataset
csv = df.to_csv(index = False).encode('utf-8')
st.download_button("Download Full DataSet", data = csv, file_name = "Data.csv", mime = "text/csv",
                   help = "Click here to download the data as a csv file")
