# Data Visualization and EDA (Exploratory Data Analysis)
This app provides an easy-to-use platform for users to perform Exploratory Data Analysis (EDA) and generate data visualizations by uploading various types of data files (CSV, Excel, SQL). Users can also create comprehensive PDF reports that compile both the results of the EDA and the visualizations created, making it useful for sharing and presentations.





## Features
1-File Upload: Supports CSV, Excel, SQL, and ZIP file formats for uploading datasets up to 200MB.


2-Exploratory Data Analysis (EDA): Performs EDA with detailed insights like head of the dataset, data types, missing values, and descriptive statistics.

3-Graphical Visualization: Provides multiple visualization options such as Line Plot, Bar Plot, Scatter Plot, Histogram, Pie Chart, Heatmap, and more.

4-Time Series Analysis: Automatically detects time-related columns and displays trends, seasonality, and residual components.

5-PDF Report Generation: Generates a PDF report with both the EDA results and graphs.


## Live Demo


You can access and use the app without any local installation via the Streamlit platform: [Data Visualization and EDA App on Streamlit](https://dashview.streamlit.app/)





## Benefits
No coding required: Upload your dataset and start analyzing instantly.

Visual Exploration: Create various types of graphs for exploring trends and relationships in your data.

Automated Reports: Generate professional PDF reports for easy sharing and decision-making.







2- Perform EDA (Exploratory Data Analysis)

Click on the Perform EDA button to analyze the structure of your dataset. The app will display:

The head (first rows) of your dataset

Data types of each column

Missing values, if any

Descriptive statistics

3- Create Visualizations

Select the columns you want to visualize and choose the graph type (e.g., Bar Plot, Scatter Plot). You can save the graph and manage multiple visualizations.


4-Generate a PDF Report
Once you've performed EDA and created visualizations, click Generate PDF Report to download a comprehensive report, including both the EDA summary and the graphs you've generated.



## Run Locally
If you prefer to run the app locally, follow the steps below to set up the environment and start the app on your machine:

1. Clone the Repository
Start by cloning the GitHub repository to your local machine. Open a terminal and run the following command:









  git clone https://github.com/REASCREH/Visualization-/blob/main/app.py

```
Navigate to the folder where the app is located:



```bash
  cd Visualization-

```

Install dependencies

```bash
  pip install streamlit==1.38.0 pandas==2.2.3 plotly==5.24.1 fpdf==1.7.2 sqlalchemy==2.0.35 openpyxl==3.1.5 kaleido==0.2.1 statsmodels==0.14.0

```

5. Run the App


```bash
  streamlit run app.py

```


## Dependencies
Streamlit: Web application framework for data apps.

Pandas: Data manipulation and analysis library.

Plotly: Visualization library for creating interactive
plots.
 
FPDF: Library to create PDF documents.

Kaleido: Required to save Plotly figures as images.
SQLAlchemy: For SQL file support.

Statsmodels: Used for advanced statistical models and tests.




## Beneficiaries of This Data Exploration Tool
Data Analysts


Unlock rapid, code-free exploratory data analysis (EDA) and generate insightful visualizations with just a few clicks. This tool accelerates the data exploration phase, allowing analysts to gain actionable insights without writing any code.

Business Analysts

Empower your business decisions by analyzing datasets effortlessly. This app helps business analysts quickly visualize and interpret data trends, uncover hidden patterns, and create compelling data stories for stakeholders.

Researchers & Students

Simplify the analysis of experimental or academic datasets. Whether you're working on research projects or coursework, this tool offers an easy way to perform data exploration, visualize findings, and generate publication-ready reports.

Educators

Enhance the learning experience in data analysis courses. With its intuitive interface, educators can use this tool to teach students the fundamentals of data exploration and visualization, helping them understand complex concepts with practical, hands-on examples.

