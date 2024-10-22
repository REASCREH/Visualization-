import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile
import os

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

    # Store the EDA output in session state
    st.session_state['eda_output'] = eda_output  # Store EDA in session

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
    pdf.multi_cell(0, 10, eda_output)  # Add the EDA text here

    # Add graphs to PDF
    for graph_file in graph_files:
        if graph_file and os.path.exists(graph_file):
            pdf.image(graph_file, x=10, w=190)  # Adjust width as needed
    
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(pdf_output)
    
    return pdf_output

# Streamlit App
st.title("Data Visualization and EDA App")

# File Upload
uploaded_file = st.file_uploader("Upload a file (CSV, Excel, SQL, ZIP)", type=["csv", "xlsx", "xls", "sql", "zip"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)  # Add support for other file formats as needed
        st.success("File uploaded successfully!")

        # EDA and Descriptive Statistics
        if st.button("Perform EDA"):
            eda_output = perform_eda(df)  # Perform EDA and store results
            st.session_state['eda_done'] = True  # Set flag to indicate EDA is done

        # Display EDA if it has already been performed
        if 'eda_done' in st.session_state and st.session_state['eda_done']:
            with st.expander("View EDA Results"):
                st.write(st.session_state['eda_output'])  # Show stored EDA results

        # Initialize session state for graph storage if not already done
        if 'graph_files' not in st.session_state:
            st.session_state['graph_files'] = []
        
        if 'graph_counter' not in st.session_state:
            st.session_state['graph_counter'] = 0

        # Graph Input Logic
        graph_counter = st.session_state['graph_counter']

        st.write(f"## Graph {graph_counter + 1}")

        # Use Streamlit columns to organize layout
        with st.expander(f"Configure Graph {graph_counter + 1}"):
            selected_columns = st.multiselect(f"Select Columns for Graph {graph_counter + 1}", df.columns)

            if len(selected_columns) >= 1:
                x_column = selected_columns[0]
                y_column = selected_columns[1] if len(selected_columns) > 1 else None
                
                graph_type = st.selectbox(f"Select Graph Type for Graph {graph_counter + 1}", 
                                           ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", 
                                            "Box Plot", "Pie Chart", "Heatmap", 
                                            "Column Chart", "Dot Plot"])

                plot = generate_plot(df, x_column, y_column, graph_type)

                # Save and automatically show the graph when "Save Graph" is clicked
                if st.button(f"Save Graph {graph_counter + 1}"):
                    graph_file = save_graph_as_image(plot)
                    if graph_file:
                        st.success(f"Graph {graph_counter + 1} saved and displayed!")
                        st.session_state['graph_files'].append((plot, graph_file))
                        st.session_state['graph_counter'] += 1  # Increment graph counter

        # Show saved graphs
        if st.session_state['graph_files']:
            st.write("### Saved Graphs")
            for idx, (plot, file_path) in enumerate(st.session_state['graph_files']):
                with st.expander(f"Graph {idx + 1}"):
                    st.plotly_chart(plot)  # Show the graph
                    if st.button(f"Remove Graph {idx + 1}"):
                        st.session_state['graph_files'].pop(idx)
                        st.experimental_rerun()  # Rerun to update the UI after graph removal

        # Generate PDF Report
        if st.button("Generate PDF Report"):
            if 'eda_output' in st.session_state and st.session_state['graph_files']:
                pdf_file = generate_pdf_report(st.session_state['eda_output'], [f for _, f in st.session_state['graph_files']])
                st.success(f"PDF Report generated.")
                with open(pdf_file, 'rb') as f:
                    st.download_button("Download PDF", data=f, file_name="EDA_Report.pdf")
            else:
                st.warning("Please perform EDA and generate at least one graph to create a PDF report.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
