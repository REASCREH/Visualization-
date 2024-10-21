import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile
from sqlalchemy import create_engine

# Helper functions
def load_data(file):
    if file.type == 'application/vnd.ms-excel':
        df = pd.read_excel(file)
    elif file.type == 'text/csv':
        df = pd.read_csv(file)
    elif 'sql' in file.name:
        engine = create_engine('sqlite:///your_sql_database.db')  # Modify to match your database
        df = pd.read_sql(file.name, engine)
    else:
        st.error('Unsupported file format. Please upload CSV, Excel, or SQL.')
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

def generate_time_series_plot(df, date_col, value_col):
    st.write(f"### Time Series Trend Plot")
    fig = px.line(df, x=date_col, y=value_col, title='Time Series Trend')
    st.plotly_chart(fig)
    return fig

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
uploaded_file = st.file_uploader("Upload a file (CSV, Excel, SQL)", type=["csv", "xlsx", "xls", "sql"])

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.success("File uploaded successfully!")

        # EDA and Descriptive Statistics
        if st.button("Perform EDA"):
            eda_output = perform_eda(df)
        
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
                date_col = x_column
                value_col = y_column
                generate_time_series_plot(df, date_col, value_col)
            else:
                if graph_type in ['Line Plot', 'Bar Plot', 'Scatter Plot', 'Histogram', 'Box Plot', 'Pie Chart', 'Heatmap', 'Column Chart', 'Dot Plot']:
                    plot = generate_plot(df, x_column, y_column, graph_type)
                
                if st.button(f"Save Graph {graph_counter + 1}"):
                    graph_file = save_graph_as_image(plot)
                    st.success(f"Graph {graph_counter + 1} saved at: {graph_file}")
                    st.session_state['graph_files'].append(graph_file)
                    st.session_state['graph_counter'] += 1  # Increment graph counter

        # Button to add another graph
        if st.button(f"Add Another Graph"):
            st.session_state['graph_counter'] += 1  # Increment graph counter for a new graph

        # Generate PDF Report
        if st.button("Generate PDF Report") and len(st.session_state['graph_files']) > 0:
            graph_files = st.session_state['graph_files']
            pdf_file = generate_pdf_report(eda_output, graph_files)
            st.success(f"PDF Report generated: {pdf_file}")
            st.download_button("Download PDF", data=open(pdf_file, "rb"), file_name="eda_report.pdf")

# Remove existing graphs
if 'graph_files' in st.session_state and len(st.session_state['graph_files']) > 0:
    st.write("## Existing Graphs")
    for idx, graph_file in enumerate(st.session_state['graph_files']):
        st.image(graph_file, caption=f"Graph {idx + 1}")
        if st.button(f"Remove Graph {idx + 1}"):
            st.session_state['graph_files'].pop(idx)
            st.success(f"Graph {idx + 1} removed.")
            st.experimental_rerun()  # Refresh the app to show updated graph list
