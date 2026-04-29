import streamlit as st
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="NCQP Optimizer", layout="wide")

st.title("🧩 Non-Convex Quadratic Programming (NCQP) Simulator")

# --- Tabs Layout ---
tab_problem, tab_sim = st.tabs(["💡 Problem Formulation", "🚀 Interactive Simulator"])

# ==========================================
# TAB 1: Problem Formulation
# ==========================================
with tab_problem:
    st.header("Mathematical Model")
    st.markdown("""
    This application solves a **Mixed-Integer Non-Convex Quadratic Programming (MINCQP)** problem.
    The goal is to determine the optimal production quantities ($n_1, n_2, n_3$) that minimize the total cost, subject to a total production constraint.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Objective Function")
        st.markdown("""
        **Minimize Total Cost:**
        $$ \min \sum_{i=1}^{3} C_i $$
        """)
        
        st.subheader("⚖️ Constraints")
        st.markdown("""
        **1. Total Production Requirement:**
        $$ n_1 + n_2 + n_3 = \text{Target Total} $$
        
        **2. Integer Variables:**
        $$ n_1, n_2, n_3 \in \mathbb{Z}_{\ge 0} $$
        *(Production quantities must be non-negative integers)*
        """)

    with col2:
        st.subheader("💸 Cost Functions (The Challenge)")
        st.info("The complexity of this problem arises from the non-linear cost structures:")
        
        st.markdown("""
        - **$C_1$ (Quadratic Cost):**  
          $$ C_1 = a \cdot n_1^2 + 2n_1 $$
          *(Cost grows quadratically as $n_1$ increases)*
          
        - **$C_2$ (Bilinear / Non-Convex Cost):**  
          $$ C_2 = b \cdot n_1 \cdot n_2 $$
          *(This is the hardest part. The cost explodes if both $n_1$ and $n_2$ are produced simultaneously. The solver must find a way to balance or avoid this interaction.)*
          
        - **$C_3$ (Linear Cost):**  
          $$ C_3 = c \cdot n_3 $$
          *(Standard linear variable cost)*
        """)
        
    st.divider()
    st.markdown("""
    ### Why is this hard?
    Traditional local solvers (like `Ipopt`) cannot handle integer variables, and standard linear solvers (like `GLPK`) cannot handle variable multiplication ($n_1 \times n_2$). 
    To guarantee a global optimal solution, this simulator uses **SCIP**, an advanced spatial branch-and-bound global optimization solver.
    """)


# ==========================================
# TAB 2: Interactive Simulator
# ==========================================
with tab_sim:
    # --- Sidebar: Parameter Settings ---
    st.sidebar.header("⚙️ Simulation Settings")

    target_total = st.sidebar.slider(
        "Target Total Production", 
        min_value=1000, max_value=3000, value=2100, step=100,
        help="Constraint representing the required sum of n1 + n2 + n3"
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Cost Function Coefficients")
    c1_a = st.sidebar.slider("Coefficient a (Quadratic)", 0.001, 0.100, 0.010, format="%.3f")
    c2_b = st.sidebar.slider("Coefficient b (Bilinear)", 1.0, 20.0, 6.0, step=1.0)
    c3_c = st.sidebar.slider("Coefficient c (Linear)", 1.0, 20.0, 7.0, step=1.0)

    # --- Optimization Logic ---
    def solve_ncqp(total, a, b, c):
        model = pyo.ConcreteModel()
        model.C = pyo.Var(range(1,4))
        model.n = pyo.Var(range(1,4), within=pyo.Integers, bounds=(0, total))
        
        C = model.C
        n = model.n

        model.obj = pyo.Objective(expr = pyo.summation(C), sense=pyo.minimize)

        model.total = pyo.Constraint(expr = pyo.summation(n) == total)
        model.C1 = pyo.Constraint(expr = C[1] == a * n[1] * n[1] + 2 * n[1])
        model.C2 = pyo.Constraint(expr = C[2] == b * n[2] * n[1])
        model.C3 = pyo.Constraint(expr = C[3] == c * n[3])

        opt = SolverFactory('scip')
        
        start_time = time.time()
        results = opt.solve(model, tee=False)
        end_time = time.time()
        
        return model, end_time - start_time, results

    st.markdown("Adjust parameters in the sidebar and click the button below to solve.")
    
    if st.button("Run Optimization (SCIP)", type="primary"):
        with st.spinner("Searching for global optimal solution using SCIP..."):
            model, solve_time, results = solve_ncqp(target_total, c1_a, c2_b, c3_c)
            
            status = str(results.solver.termination_condition)
            
            if status == "optimal":
                st.success(f"Optimization Complete! Solve Time: {solve_time:.3f} sec")
                
                n1_val, n2_val, n3_val = pyo.value(model.n[1]), pyo.value(model.n[2]), pyo.value(model.n[3])
                c1_val, c2_val, c3_val = pyo.value(model.C[1]), pyo.value(model.C[2]), pyo.value(model.C[3])
                c_total = pyo.value(pyo.summation(model.C))
                
                st.subheader("🏆 Optimization Results")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Cost (Minimum)", f"{c_total:,.0f}")
                col2.metric("n1 Allocation", f"{n1_val:,.0f}")
                col3.metric("n2 Allocation", f"{n2_val:,.0f}")
                col4.metric("n3 Allocation", f"{n3_val:,.0f}")
                
                st.subheader("📊 Allocation & Cost Analysis")
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                n_data = {'n1 (Quadratic)': n1_val, 'n2 (Bilinear)': n2_val, 'n3 (Linear)': n3_val}
                ax1.bar(n_data.keys(), n_data.values(), color=['#4e79a7', '#f28e2b', '#e15759'])
                ax1.set_title("Production Allocation Balance")
                ax1.set_ylabel("Quantity")
                
                c_data = [c1_val, c2_val, c3_val]
                c_labels = ['C1 (Quadratic)', 'C2 (Bilinear)', 'C3 (Linear)']
                
                if sum(c_data) > 0:
                    ax2.pie(c_data, labels=c_labels, autopct='%1.1f%%', startangle=90, colors=['#4e79a7', '#f28e2b', '#e15759'])
                    ax2.set_title("Cost Breakdown")
                else:
                    ax2.text(0.5, 0.5, "Total Cost is 0", ha='center', va='center')
                    ax2.axis('off')
                
                st.pyplot(fig)
                
                with st.expander("View Detailed Data"):
                    df = pd.DataFrame({
                        "Item": ["1", "2", "3", "Total"],
                        "Production (n)": [n1_val, n2_val, n3_val, n1_val+n2_val+n3_val],
                        "Cost (C)": [c1_val, c2_val, c3_val, c_total]
                    })
                    st.dataframe(df, use_container_width=True)
                    
            else:
                st.error(f"No optimal solution found. Status: {status}")
    else:
        st.info("System is ready. Awaiting user execution.")
