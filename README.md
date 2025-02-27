# Mapua University Canteen Ordering System

## Introduction
Greetings! The **Mapua University Canteen Ordering System** is a web-based platform designed to streamline food ordering within the university. Built using the **Python** programming language and **Streamlit** web framework, this system enables store owners to manage menus and discounts while allowing users to browse and place orders conveniently.

## Prerequisites
Before running the application, ensure you have the following installed:

1. **Python (>= 3.8)**  
   - Download and install Python from [python.org](https://www.python.org/downloads/).  
   - Ensure `pip` is installed (comes with Python).

2. **Visual Studio Code (VS Code)**  
   - Download and install [VS Code](https://code.visualstudio.com/).  
   - Install the **Python extension** in VS Code.

3. **Required Python Packages**  
   - Install dependencies using:
     ```
     pip install streamlit
     pip install pandas
     ```

## Running the Application

### 1. Clone the Repository (Optional)
If using Git, you can clone the project:
```
git clone https://github.com/your-repo-link.git
cd your-repo-folder
```


### 2. Open the Project in VS Code
- Launch **VS Code**.
- Open the project folder:
  - Click **File** > **Open Folder**
  - OR use the shortcut: **Ctrl + K, Ctrl + O**

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Run the Application
```
streamlit run Login.py
```
- This will open the application in your default web browser.

## Troubleshooting Common Issues

### For 1. and 2., make sure you run these commands in the same directory!

### 1. ModuleNotFoundError: No module named 'streamlit'
- Run:
  ```
  pip install streamlit
  ```  

### 2. ModuleNotFoundError: No module named 'pandas'
- Run:
  ```
  pip install pandas
  ```

### 3. File Read/Write Issues (e.g., PermissionError)
- Ensure the application has write access to "samplemenu.txt" and "discounts.txt".
- Try running VS Code as an **administrator** (Windows) or using `sudo` (Linux/macOS).

### 4. Database not found!
- Make sure that after downloading the "SoftwareLabWebApp", you must bring out the files and place those files in the main folder.


