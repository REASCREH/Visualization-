import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Function to perform EDA (placeholder for your implementation)
def perform_eda(df):
    # This function should return the EDA summary
    eda_summary = {
        "shape": df.shape,
        "data_types": df.dtypes,
        "missing_values": df.isnull().sum(),
        "descriptive_stats": df.describe()
    }
    return eda_summary

# Function to generate plots based on user input
def generate_plot(df, x_col, y_col, graph_type, sample_size):
    if sample_size and sample_size > 0:
        df = df.sample(n=sample_size)

    plt.figure(figsize=(10, 6))

    if graph_type == 'Line Plot':
        sns.lineplot(data=df, x=x_col, y=y_col)
    elif graph_type == 'Bar Plot':
        sns.barplot(data=df, x=x_col, y=y_col)
    elif graph_type == 'Scatter Plot':
        sns.scatterplot(data=df, x=x_col, y=y_col)
    elif graph_type == 'Histogram':
        sns.histplot(data=df, x=x_col, bins=30)
    elif graph_type == 'Box Plot':
        sns.boxplot(data=df, x=x_col, y=y_col)
    elif graph_type == 'Pie Chart':
        df[x_col].value_counts().plot.pie(autopct='%1.1f%%')
    elif graph_type == 'Heatmap':
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
    elif graph_type == 'Column Chart':
        df[x_col].value_counts().plot(kind='bar')
    elif graph_type == 'Dot Plot':
        sns.stripplot(data=df, x=x_col, y=y_col)

    plt.title(f"{graph_type} of {y_col} vs {x_col}")
    plt.tight_layout()
    return plt

# Function to save graph as image
def save_graph_as_image(fig):
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)
    return img_buf

# Function to generate PDF report (placeholder for your implementation)
def generate_pdf_report(eda_output, graph_files):
    # Implement PDF generation logic
    pdf_path = "output_report.pdf"
    return pdf_path

# Streamlit App
st.title("Exploratory Data Analysis and Visualization")

# File Upload
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
        st.session_state['eda_output'] = eda_output

        # Initialize session state for graphs
        if 'graph_files' not in st.session_state:
            st.session_state['graph_files'] = []
        if 'graph_counter' not in st.session_state:
            st.session_state['graph_counter'] = 0

        # Function to add graphs
        def add_graph():
            st.session_state['x_col'] = st.selectbox("Select X-axis column:", df.columns, key=f"x_col_{st.session_state['graph_counter']}")
            st.session_state['y_col'] = st.selectbox("Select Y-axis column:", df.columns, key=f"y_col_{st.session_state['graph_counter']}")
            st.session_state['graph_type'] = st.selectbox("Select Graph Type:", 
                ['Line Plot', 'Bar Plot', 'Scatter Plot', 'Histogram', 'Box Plot', 'Pie Chart', 'Heatmap', 'Column Chart', 'Dot Plot'], 
                key=f"graph_type_{st.session_state['graph_counter']}")
            sample_size = st.number_input("Sample Size (leave blank for full dataset):", min_value=1, step=1, value=None, key=f"sample_size_{st.session_state['graph_counter']}")

            if st.button("Generate Plot", key=f"plot_button_{st.session_state['graph_counter']}"):
                fig = generate_plot(df, st.session_state['x_col'], st.session_state['y_col'], st.session_state['graph_type'], sample_size)
                
                # Save graph as image
                graph_file = save_graph_as_image(fig)
                st.session_state['graph_files'].append(graph_file)
                st.session_state['graph_counter'] += 1
                st.pyplot(fig)  # Display the generated plot

        # Add initial graph
        add_graph()

        # Loop to add more graphs
        while st.session_state['graph_counter'] < 5:  # Limit number of graphs for demonstration
            if st.button("Add Another Graph"):
                add_graph()
            else:
                break

        # Button to generate PDF report
        if st.button("Generate PDF Report"):
            pdf_output = generate_pdf_report(st.session_state['eda_output'], st.session_state['graph_files'])
            st.success(f"PDF report generated! [Download it here]({pdf_output})")

    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
