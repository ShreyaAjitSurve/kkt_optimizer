# kkt_optimizer
KKT Optimizer is a web-based application that solves constrained optimization problems using symbolic computation and displays step-by-step solutions.
This tool allows users to input an objective function and constraint, and it cmputes the optimal solution with step by step mathematical derivation, rendered cleanly using MathJax.

Features
- It suports minimization and maximization
- Only one constraint can be handled h(x) <= 0
- Steps:
    -Objective function
    -Constraint
    -Lagrangian
    -Stationarity Conditions(Partial derivative of L w.r.t. each variable and lambda)
    -KKT conditions
    -Case Analysis(λ = 0 and λ not equal to 0, i.e. h(x) = 0) -> Even if one condition of KKT is not satisfied then that case is rejected
    -Final Optimal Solution with conclusion(Whether Z is Minimum or Maximum for that value of Z and the variables)
-Clean UI with optimal solution for Z with n number of variables. There are 3 screens:
    -Splash Screen
    -Input Screen
    -Result Screen
-Mathematical equations rendered using MathJax

-Tech Stack:
  **Frontend**
* HTML
* CSS
* MathJax (for LaTeX rendering)

**Backend**
* Python
* Flask
* SymPy (for symbolic computation)

## 📁 Project Structure
kkt_fron/
├── backend/                # Logic and core processing
│   ├── kkt_solver.py       # SymPy implementation of KKT conditions
│   └── app.py              # Backend API/logic handler
├── static/                 # Frontend assets
│   └── style.css           # Custom UI styling (Figma-aligned)
├── templates/              # HTML files for the Flask/Web interface
│   ├── landing.html        # Initial entry page
│   ├── index.html          # Input form for optimization problems
│   └── result.html         # Output display for KKT solutions
├── venv0/                  # Python virtual environment
│   ├── .gitignore          # Git exclusion rules
│   └── pyvenv.cfg          # Virtual environment configuration
├── .vscode/                # Editor-specific settings
└── app.py                  # Main entry point for the application

---

## ⚙️ Setup Instructions

Prerequisites:
  Ensure the following are installed:
    Python (version 3.7 or above)
    pip (Python package manager)
    Visual Studio Code or any code editor
    Step 1: Download the Project

Download the project folder and extract it (if compressed) to a desired location on your system.

Step 2: Open the Project

Open the project folder in your code editor (e.g., VS Code).

Step 3: Set Up a Virtual Environment (Recommended)

Create a virtual environment to manage dependencies:

python -m venv venv

Activate the virtual environment:

Windows (PowerShell):

venv\Scripts\activate
Step 4: Install Dependencies

Install the required Python package:

pip install flask
Step 5: Verify Project Structure

Step 6: Run the Application

Start the Flask development server:

python app.py
Step 7: Access the Application

Open a web browser and navigate to:

http://127.0.0.1:5000/
Step 8: Using the Application
Enter the objective function, constraint, and constant value
Select the problem type (Maximization/Minimization)
Click Solve to view results
Step 9: Stopping the Server

To stop the application, press:

CTRL + C
Troubleshooting
Ensure Flask is installed correctly
Confirm that the templates folder contains index.html
Verify that the application is executed from the project root directory

Frontend communicates with Flask backend via HTTP requests
Backend processes input using SymPy and returns results

-Example Input
Objective:
8*x1 + 10*x2 - x1**2 - x2**2
Constraint:
3*x1 + 2*x2 - 6

-Limitations
Supports only one constraint
Assumes constraint in form:
h(x) ≤ 0
No inequality direction input (fixed as ≤ 0)






  
