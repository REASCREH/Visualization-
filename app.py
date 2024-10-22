import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile
import os

# Function to perform EDA
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

    # Store the EDA output in session state
    st.session_state['eda_output'] = eda_output

    # Show the EDA results in Streamlit
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
def generate_plot(df, x_col, y_col, graph_type, sample_size=None):
    if sample_size:
        df = df.sample(n=sample_size)  # Sample the data if required

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

# Save graph as image
def save_graph_as_image(fig):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            fig.write_image(temp_file.name)
            return temp_file.name
    except Exception as e:
        st.error(f"Error saving graph image: {str(e)}")
        return None

# Generate PDF Report with EDA output and graphs
def generate_pdf_report(eda_output, graph_files):
    pdf = FPDF()
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Exploratory Data Analysis Report", ln=True, align='C')

    # Add EDA output as text
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, eda_output)

    # Add graphs to PDF
    for graph_file in graph_files:
        if graph_file and os.path.exists(graph_file):
            pdf.image(graph_file, x=10, w=190)

    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(pdf_output)

    return pdf_output

# Streamlit App
st.title("Data Visualization and EDA App")

# Initialize session state variables
if 'eda_done' not in st.session_state:
    st.session_state['eda_done'] = False
if 'graph_files' not in st.session_state:
    st.session_state['graph_files'] = []
if 'graph_counter' not in st.session_state:
    st.session_state['graph_counter'] = 0

# File Upload# File Upload
uploaded_file = st.file_uploader("Upload a file (CSV, Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # Load DataFrame based on file extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Perform EDA and store the output
        eda_output = perform_eda(df)
        st.session_state['eda_done'] = True

        # Select columns for plotting
        x_col = st.selectbox("Select X-axis column:", df.columns)
        y_col = st.selectbox("Select Y-axis column:", df.columns)
        graph_type = st.selectbox("Select Graph Type:", 
            ['Line Plot', 'Bar Plot', 'Scatter Plot', 'Histogram', 'Box Plot', 'Pie Chart', 'Heatmap', 'Column Chart', 'Dot Plot'])
        sample_size = st.number_input("Sample Size (leave blank for full dataset):", min_value=1, step=1, value=None)

        # Button to generate plot
        if st.button("Generate Plot"):
            fig = generate_plot(df, x_col, y_col, graph_type, sample_size)

            # Save graph as image
            graph_file = save_graph_as_image(fig)
            if graph_file:
                st.session_state['graph_files'].append(graph_file)
                st.session_state['graph_counter'] += 1

        # Display previously generated graphs
        if st.session_state['graph_files']:
            st.write("### Previously Generated Graphs:")
            for graph_file in st.session_state['graph_files']:
                st.image(graph_file)

        # Button to generate PDF report
        if st.button("Generate PDF Report"):
            pdf_output = generate_pdf_report(st.session_state['eda_output'], st.session_state['graph_files'])
            st.success(f"PDF report generated! [Download it here]({pdf_output})")

    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
