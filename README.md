Good day!

We are Group 7 of CPE106L-4, section E02.

Welcome to the Mapua University Canteen Ordering System Application!

Here are the instructions on how to run the application inside an IDE like Visual Studio Code:

Prerequisites:
Before running the application, make sure you have the following installed:  

1. Python (>= 3.8) 
   - Download and install Python from [python.org](https://www.python.org/downloads/).  
   - Ensure pip is installed (comes with Python).  

2. Visual Studio Code (VS Code) 
   - Download and install [VS Code](https://code.visualstudio.com/).  
   - Install the Python extension in VS Code.  

3. Install Required Python Packages
  - pandas

Running the Application
1. Open the Project in VS Code
- Launch VS Code.
- Go to the top left and there should be a button there that reads "File"
- Click the button and choose the option "Open Folder"
  Note: you can also open a folder quickly by using the shortuct Ctrl K + Ctrl O
- Open the folder where the project files are located.  

2. Run the Main Application
- Open the VS Code terminal  
- Navigate to the project directory (if needed):  
- Run the Streamlit application in the terminal:  
  streamlit run Login.py
- This will launch the application in your default web browser.  


Troubleshooting Common Issues
ModuleNotFoundError: No module named streamlit
- pip install streamlit

ModuleNotFoundError: No module named pandas
- pip install pandas

File Read/Write Issues (e.g., PermissionError) 
- Ensure the application has write permissions to samplemenu.txt and discounts.txt.

