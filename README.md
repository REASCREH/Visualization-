Data Visualization and EDA App
Overview
This app simplifies the process of performing Exploratory Data Analysis (EDA) and creating visualizations from datasets. Users can upload CSV, Excel, or SQL files and explore their data without needing any programming skills. The app also generates comprehensive PDF reports summarizing both the EDA and the visualizations created.

Key Features
File Upload Support: Accepts CSV, Excel, and SQL file formats for easy data exploration.
Automated EDA: The app generates a summary of the dataset, including head of the data, data types, missing values, and descriptive statistics.
Multiple Visualization Options: Users can choose from a wide variety of plot types, including:
Line Plot
Bar Plot
Scatter Plot
Histogram
Box Plot
Pie Chart
Heatmap
Column Chart
Dot Plot
Graph Management: Save, view, and remove multiple visualizations.
PDF Report Generation: Export both the EDA results and generated plots into a professional PDF report.
Benefits
Why Use This App?
Ease of Use: No need to write code. Upload your data and start analyzing with just a few clicks.
Automated EDA: Quickly analyze data structures, spot missing values, and review descriptive statistics.
Data Visualization: Easily generate various types of charts to explore patterns, trends, and relationships within the data.
Report Generation: Create comprehensive PDF reports that compile EDA insights and visualizations in one place for easy sharing with stakeholders.
Who Is This App For?
Data Analysts: Quickly perform EDA and generate visualizations without the need for programming.
Business Analysts: Generate insights and visualize business data for decision-making or presentations.
Data Scientists: Speed up the initial data exploration phase.
Educators and Students: Use this app as a learning tool for understanding data analysis and visualization.
Researchers: Analyze experimental data and present findings in a concise PDF report.
Consultants: Easily share insights with clients through a visually appealing PDF report.
Business Decision Makers: Upload data, explore trends, and generate reports independently.
Installation and Setup
To run the app locally, follow these steps:


bash
Install the required dependencies:
streamlit==1.38.0
pandas==2.2.3
plotly==5.24.1
fpdf==1.7.2
sqlalchemy==2.0.35
openpyxl==3.1.5
kaleido==0.2.1
statsmodels==0.14.0
bash
pip install -r requirements.txt
Run the Streamlit app:
import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile
from io import BytesIO
from fpdf import FPDF
import tempfile
from sqlalchemy import create_engine
from statsmodels.tsa.seasonal import seasonal_decompose

# Helper function to handle .zip files
def load_data(file):
    if file.type == 'application/vnd.ms-excel':
        df = pd.read_excel(file)
    elif file.type == 'text/csv':
        df = pd.read_csv(file)
    elif file.type == 'application/x-zip-compressed':
        with zipfile.ZipFile(file) as z:
            # Assuming there's only one CSV or Excel file inside the zip
            for filename in z.namelist():
                if filename.endswith('.csv'):
                    df = pd.read_csv(z.open(filename))
                elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                    df = pd.read_excel(z.open(filename))
                else:
                    st.error('Unsupported file format inside zip. Please upload CSV or Excel.')
                    return None
    elif 'sql' in file.name:
        engine = create_engine('sqlite:///your_sql_database.db')  # Modify to match your database
        df = pd.read_sql(file.name, engine)
    else:
        st.error('Unsupported file format. Please upload CSV, Excel, SQL, or ZIP.')
        return None
    return df

# Perform EDA and capture the results as a string for PDF
def perform_eda(df):
    eda_output = ""

    # Capture the head of the dataset
    eda_output += "### Head of the dataset:\n"
    eda_output += df.head().to_string() + "\n\n"

    # Capture data types
    eda_output += "### Data Types:\n"
    eda_output += df.dtypes.to_string() + "\n\n"

    # Capture missing values
    eda_output += "### Missing Values:\n"
    eda_output += df.isnull().sum().to_string() + "\n\n"

    # Capture descriptive statistics
    eda_output += "### Descriptive Statistics:\n"
    eda_output += df.describe().to_string() + "\n\n"

    # Show the EDA results in Streamlit as before
    st.write("### Exploratory Data Analysis")
    st.write("Head of the dataset:")
    st.dataframe(df.head())

    st.write("Data Types:")
    st.write(df.dtypes)

    st.write("Missing Values:")
    st.write(df.isnull().sum())

    st.write("Descriptive Statistics:")
    st.write(df.describe())

    return eda_output

# Function to generate plot
def generate_plot(df, x_col, y_col, graph_type):
    st.write(f"### {graph_type} Plot")
    
    if graph_type == 'Line Plot':
        fig = px.line(df, x=x_col, y=y_col)
    elif graph_type == 'Bar Plot':
        fig = px.bar(df, x=x_col, y=y_col)
    elif graph_type == 'Scatter Plot':
        fig = px.scatter(df, x=x_col, y=y_col)
    elif graph_type == 'Histogram':
        fig = px.histogram(df, x=x_col)
    elif graph_type == 'Box Plot':
        fig = px.box(df, x=x_col, y=y_col)
    elif graph_type == 'Pie Chart':
        fig = px.pie(df, names=x_col, values=y_col, title='Pie Chart')
    elif graph_type == 'Heatmap':
        fig = px.imshow(df.corr(), title='Heatmap of Correlation')
    elif graph_type == 'Column Chart':
        fig = px.bar(df, x=x_col, y=y_col)
    elif graph_type == 'Dot Plot':
        fig = px.scatter(df, x=x_col, y=y_col, title='Dot Plot', opacity=0.6)
    
    st.plotly_chart(fig)
    
    return fig

# Function to handle Time Series Analysis and show trend/seasonality
def generate_time_series_plot(df, date_col, value_col):
    st.write(f"### Time Series Trend Plot")
    fig = px.line(df, x=date_col, y=value_col, title='Time Series Trend')
    st.plotly_chart(fig)
    return fig

def show_seasonality_trend(df, date_col, value_col):
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)
    
    # Decompose the time series into trend, seasonality, and residuals
    result = seasonal_decompose(df[value_col], model='additive', period=12)  # Adjust period for your data

    st.write("### Decomposed Time Series Components:")
    
    # Plotting trend
    st.write("#### Trend")
    trend_fig = px.line(result.trend, title="Trend Component")
    st.plotly_chart(trend_fig)
    
    # Plotting seasonality
    st.write("#### Seasonality")
    seasonality_fig = px.line(result.seasonal, title="Seasonality Component")
    st.plotly_chart(seasonality_fig)
    
    # Plotting residuals
    st.write("#### Residuals")
    residual_fig = px.line(result.resid, title="Residuals Component")
    st.plotly_chart(residual_fig)

# Save graph as image
def save_graph_as_image(fig):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        fig.write_image(temp_file.name)
        return temp_file.name

# Generate PDF Report with EDA output and graphs
def generate_pdf_report(eda_output, graph_files):
    pdf = FPDF()
    pdf.add_page()
    
    # Set title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Exploratory Data Analysis Report", ln=True, align='C')

    # Add EDA output as text
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, eda_output)  # Add the EDA text here

    # Add graphs to PDF
    for graph_file in graph_files:
        pdf.image(graph_file, x=10, w=190)  # Adjust width as needed
    
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(pdf_output)
    
    return pdf_output

# Streamlit App
st.title("Data Visualization and EDA App")

# File Upload
uploaded_file = st.file_uploader("Upload a file (CSV, Excel, SQL, ZIP)", type=["csv", "xlsx", "xls", "sql", "zip"])

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.success("File uploaded successfully!")

        # EDA and Descriptive Statistics
        if st.button("Perform EDA"):
            eda_output = perform_eda(df)
            st.session_state['eda_output'] = eda_output  # Store the EDA output in session state
        
        # Initialize session state for graph storage if not already done
        if 'graph_files' not in st.session_state:
            st.session_state['graph_files'] = []
        
        if 'graph_counter' not in st.session_state:
            st.session_state['graph_counter'] = 0
        
        # Graph Input Logic
        graph_counter = st.session_state['graph_counter']

        st.write(f"## Graph {graph_counter + 1}")

        selected_columns = st.multiselect(f"Select Columns for Graph {graph_counter + 1}", df.columns, key=f"multiselect_{graph_counter}")

        if len(selected_columns) >= 1:
            x_column = selected_columns[0]
            y_column = selected_columns[1] if len(selected_columns) > 1 else None
            
            graph_type = st.selectbox(f"Select Graph Type for Graph {graph_counter + 1}", 
                                       ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", 
                                        "Box Plot", "Pie Chart", "Heatmap", 
                                        "Column Chart", "Dot Plot"], key=f"selectbox_{graph_counter}")

            # Check for Time Series Data
            if 'date' in x_column.lower() or 'time' in x_column.lower():  # Simple check for date column
                if y_column is not None and pd.api.types.is_numeric_dtype(df[y_column]):
                    date_col = x_column
                    value_col = y_column
                    generate_time_series_plot(df, date_col, value_col)
                    
                    # Show seasonality and trend
                    show_seasonality_trend(df, date_col, value_col)
                else:
                    st.warning("Sorry, the selected dataset does not contain suitable numeric data for time series analysis.")
            else:
                if graph_type in ['Line Plot', 'Bar Plot', 'Scatter Plot', 'Histogram', 'Box Plot', 'Pie Chart', 'Heatmap', 'Column Chart', 'Dot Plot']:
                    plot = generate_plot(df, x_column, y_column, graph_type)
                
                if st.button(f"Save Graph {graph_counter + 1}"):
                    graph_file = save_graph_as_image(plot)
                    st.success(f"Graph {graph_counter + 1} saved at: {graph_file}")
                    st.session_state['graph_files'].append(graph_file)
                    st.session_state['graph_counter'] += 1  # Increment graph counter

        # Button to add another graph
        if st.button("Add Another Graph"):
            st.session_state['graph_counter'] += 1

# Generate PDF Report
if st.button("Generate PDF Report"):
    if 'eda_output' in st.session_state and st.session_state['graph_files']:
        pdf_file = generate_pdf_report(st.session_state['eda_output'], st.session_state['graph_files'])
        st.success(f"PDF Report generated: {pdf_file}")
    else:
        st.warning("Please perform EDA and generate at least one graph to create a PDF report.")
bash
streamlit run app.py
Open your browser and navigate to the URL provided by Streamlit (typically http://localhost:8501).

How to Use the App
Upload Data:

Use the file uploader to upload a CSV, Excel, or SQL file.
Supported formats: .csv, .xlsx, .xls, .sql.
Perform EDA:

Click the Perform EDA button to see a summary of your dataset, including data types, missing values, and descriptive statistics.
Generate Visualizations:

Select the columns you want to visualize.
Choose the type of graph (e.g., line plot, bar chart, scatter plot, etc.).
Save the graph if needed.
Create PDF Report:

Once you have performed the EDA and generated graphs, click the Generate PDF Report button to compile everything into a downloadable PDF report.
Manage Graphs:

View, save, or remove graphs as needed using the interface.
Dependencies
Python 3.12+
Streamlit
Plotly
Pandas
FPDF
Install dependencies via pip install -r requirements.txt.

Example
Here’s a brief example of how you can use the app to perform EDA and generate visualizations:

Upload your dataset.
Perform EDA to view data statistics.
Select columns and graph types to visualize the data.
Generate a PDF report to summarize your findings.
