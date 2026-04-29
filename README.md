# 🧩 Non-Convex Quadratic Programming (NCQP) Simulator

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Optimization](https://img.shields.io/badge/Optimization-Pyomo%20%7C%20SCIP-success.svg)](http://www.pyomo.org/)

An interactive web application built with **Streamlit** and **Pyomo** that simulates resource allocation under complex, non-linear cost structures. This project demonstrates how to solve a **Mixed-Integer Non-Convex Quadratic Programming (MINCQP)** problem using the **SCIP** global optimization solver.

---

## 📖 Overview

In real-world business scenarios (e.g., chemical blending, economies of scale, portfolio optimization), cost structures are rarely purely linear. They often involve:
*   **Quadratic Costs:** Cost grows exponentially as quantity increases ($x^2$).
*   **Bilinear Costs (Variable Multiplication):** The cost of producing product $A$ depends on the quantity of product $B$ ($x \times y$). 

These non-linearities create multiple "valleys" (local minima) in the solution space. Standard local solvers like `Ipopt` may get trapped in a local minimum. To mathematically guarantee the **true global optimal solution**, this simulator utilizes **SCIP**, an advanced spatial branch-and-bound global solver.

## ✨ Features

*   **Interactive Simulation:** Adjust the total production target and the cost coefficients via sidebar sliders.
*   **Real-time Global Optimization:** The backend dynamically builds a Pyomo model and calls the SCIP solver.
*   **Data Visualization:** Instantly see the optimal production allocation (Bar Chart) and cost breakdown (Pie Chart).
*   **Educational Context:** A dedicated "Problem Formulation" tab explaining the mathematics and the challenge of non-convexity.

## 🧮 The Mathematical Model

**Objective:**
Minimize Total Cost $\sum_{i=1}^{3} C_i$

**Constraints:**
1.  **Total Target:** $n_1 + n_2 + n_3 = \text{Target}$
2.  **Quadratic Cost:** $C_1 = a \cdot n_1^2 + 2n_1$
3.  **Bilinear Cost (Non-Convex):** $C_2 = b \cdot n_1 \cdot n_2$
4.  **Linear Cost:** $C_3 = c \cdot n_3$
5.  **Integer Bounds:** $n_i \in \mathbb{Z}_{\ge 0}$

## 🚀 How to Run Locally

Because this project relies on an external C-based solver (SCIP), it is highly recommended to use **Conda** for environment management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/ncqp-simulator.git
   cd ncqp-simulator
   ```

2. **Create the Conda environment:**
   This will install Python, Streamlit, Pyomo, and the SCIP solver binaries automatically.
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment:**
   ```bash
   conda activate ncqp-streamlit
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment on Streamlit Community Cloud

This repository is ready to be deployed on Streamlit Community Cloud. 
Because we included an `environment.yml` file, Streamlit Cloud will automatically detect it, build a Linux-based Conda environment, and install the SCIP binaries behind the scenes. 

1. Push this code to a public GitHub repository.
2. Go to Streamlit Community Cloud.
3. Select "New app" and point it to your repository and `app.py`.
4. Click **Deploy** (The first build may take 3-5 minutes to install SCIP).

---
*Developed as a showcase for Mathematical Optimization, Operations Research, and MLOps/DevOps practices.*
