Data Visualization and EDA App
Overview
This app simplifies the process of Exploratory Data Analysis (EDA) and creating visualizations from datasets. Users can upload CSV, Excel, or SQL files and explore their data without any programming skills. The app also generates comprehensive PDF reports summarizing both the EDA and the visualizations created.

Key Features
File Upload Support: Accepts CSV, Excel, and SQL file formats for easy data exploration.
Automated EDA: Generates a summary of the dataset, including:
Head of the data
Data types
Missing values
Descriptive statistics
Multiple Visualization Options:
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
Data Visualization: Easily generate various types of charts to explore patterns, trends, and relationships.
Report Generation: Create comprehensive PDF reports that compile EDA insights and visualizations in one place for easy sharing with stakeholders.
Who Is This App For?
Data Analysts: Quickly perform EDA and generate visualizations without programming.
Business Analysts: Generate insights and visualize business data for decision-making or presentations.
Data Scientists: Speed up the initial data exploration phase.
Educators and Students: Learn and understand data analysis and visualization through an easy-to-use tool.
Researchers: Analyze experimental data and present findings in a concise PDF report.
Consultants: Easily share insights with clients via professional PDF reports.
Business Decision Makers: Explore trends and generate reports independently.
Installation and Setup
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-repo-link.git
2. Install Dependencies
Install the required Python libraries by running the following command:

bash
Copy code
pip install -r requirements.txt
Here’s a list of the required dependencies:

text
Copy code
streamlit==1.38.0
pandas==2.2.3
plotly==5.24.1
fpdf==1.7.2
sqlalchemy==2.0.35
openpyxl==3.1.5
kaleido==0.2.1
statsmodels==0.14.0
3. Run the App
To run the app locally, execute the following command:

bash
Copy code
streamlit run app.py
The app will be available at http://localhost:8501.

How to Use the App
Step 1: Upload Data
Use the file uploader to upload a CSV, Excel, or SQL file.
Supported formats: .csv, .xlsx, .xls, .sql, .zip.
Step 2: Perform EDA
Click the Perform EDA button to see a summary of your dataset, including data types, missing values, and descriptive statistics.
Step 3: Generate Visualizations
Select the columns you want to visualize.
Choose the type of graph (e.g., line plot, bar chart, scatter plot, etc.).
Save the graph if needed.
Step 4: Create PDF Report
After performing EDA and generating graphs, click the Generate PDF Report button to compile everything into a downloadable PDF report.
Step 5: Manage Graphs
View, save, or remove graphs as needed using the interface.
Example Walkthrough
Here’s a brief example of how you can use the app to perform EDA and generate visualizations:

Upload your dataset.
Perform EDA to view data statistics.
Select columns and graph types to visualize the data.
Generate a PDF report to summarize your findings.
Dependencies
This app requires Python 3.12+ and the following key libraries:

Streamlit: For building the web app interface.
Pandas: For data manipulation and analysis.
Plotly: For generating interactive visualizations.
FPDF: For creating PDF reports.
SQLAlchemy: For handling SQL file uploads.
Openpyxl: For working with Excel files.
Kaleido: For saving visualizations as images.
Statsmodels: For time-series analysis.
Install all dependencies via the following command:

bash
pip install -r requirements.txt
App Architecture
File Upload Handling:

Accepts CSV, Excel, SQL, and ZIP formats.
Extracts data for analysis and visualization.
EDA Functionality:

Displays a summary of the dataset, such as data types, missing values, and descriptive statistics.
Visualization Generation:

Offers multiple graph types (Line, Bar, Scatter, etc.) and handles time series analysis.
PDF Report Generation:

Compiles both EDA insights and visualizations into a professional PDF report.
Conclusion
This Data Visualization and EDA App offers a powerful and easy-to-use interface for analyzing datasets without writing code. Whether you're an analyst, educator, or decision-maker, this tool streamlines the entire data exploration and reporting process into a few simple steps.
