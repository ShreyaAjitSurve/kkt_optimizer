from sympy import symbols, diff, solve, sympify, latex, N, nsolve

def solve_kkt(n, objective_str, constraint_str, problem_type):
    problem_type = problem_type.lower()
    
    # 1. Dynamically create n symbols: x1, x2, ..., xn
    var_names = [f"x{i+1}" for i in range(n)]
    vars = symbols(var_names)
    lam = symbols("lambda")  

    f = sympify(objective_str)
    h = sympify(constraint_str)

    # Lagrangian sign depends on problem type
    # Max: L = f - λh | Min: L = f + λh
    L = f - lam*h if problem_type == "max" else f + lam*h

    # Create dynamic labels like "x_1, x_2" for the LaTeX output based on n
    vars_display = ", ".join([f"x_{{{i+1}}}" for i in range(n)])
    
    steps = []
    valid_points = []

    # Step 1: Problem Formulation
    steps.append({
        "title": "Step 1: Problem Formulation",
        "explanation": f"Identify the {problem_type} function and express the constraint in h(x) ≤ 0 form.",
        "latex": [
            f"Z_{{{problem_type}}} = f({vars_display}) = {latex(f)}",
            f"h({vars_display}) = {latex(h)} \\leq 0"
        ]
    })

    # Step 2: KKT Conditions
    steps.append({
        "title": "Step 2: KKT Conditions",
        "explanation": "The necessary Karush-Kuhn-Tucker (KKT) conditions for the optimization are defined as follows:",
        "latex": [
            r"(a) \text{ Stationarity: } \frac{\partial L}{\partial x_i} = 0",
            r"(b) \text{ Complementary Slackness: } \lambda \cdot h(x) = 0",
            r"(c) \text{ Primal Feasibility: } h(x) \leq 0",
            r"(d) \text{ Dual Feasibility: } " + (r"\lambda \geq 0" if problem_type == "max" else r"\lambda \leq 0"),
            # Use fr"" to allow both variables and LaTeX backslashes
            fr"(e) \text{{ Non-negativity: }} {vars_display} \geq 0"
        ]
    })

    # Step 3: Lagrangian & Stationarity
    grad_L = [diff(L, v) for v in vars]
    
    steps.append({
        "title": "Step 3: Lagrangian & Stationarity",
        "explanation": "Construct the Lagrangian and compute partial derivatives for all variables.",
        "latex": [
            f"L = {latex(L)}",
        ] + [f"\\frac{{\\partial L}}{{\\partial {latex(v)}}} = {latex(e)} = 0" for v, e in zip(vars, grad_L)]
    })

    # ===== CASE 1: λ = 0 (Interior Optimum) =====
    # Initialize status and latex early to avoid "not accessed" or scope errors
    status1 = "Rejected"
    case1_latex = [r"\text{From equation set (a), when } \lambda = 0:"]

    try:
        # 1. Solve stationarity equations (Equation set a) assuming λ = 0
        sols_case1 = solve([diff(f, v) for v in vars], vars, dict=True)

        if sols_case1:
            sol = sols_case1[0]
            # Format the derivation: e.g., "8 - 2x1 = 0, and 10 - 2x2 = 0"
            deriv_eqs = ", \\text{ and } ".join([f"{latex(diff(f, v))} = 0" for v in vars])
            case1_latex.append(deriv_eqs)

            # Format the solved points: e.g., "x1 = 4, and x2 = 5"
            points_str = ", \\text{ and } ".join([f"{latex(v)} = {round(float(N(sol[v])), 3)}" for v in vars])
            case1_latex.append(f"\\therefore {points_str}")

            # 2. Constraint checking section
            h_val = float(N(h.subs(sol)))
            case1_latex.append(r"\text{Now, checking constraint condition (c):}")
            
            # Show the substitution result
            case1_latex.append(f"{latex(h)} = {round(h_val, 3)}")

            if h_val <= 0.001:
                status1 = "Accepted"
                sol_with_lam = sol.copy()
                sol_with_lam[lam] = 0
                valid_points.append(sol_with_lam)
                case1_latex.append(f"{round(h_val, 3)} \\leq 0 \\text{{ (Satisfied!)}}")
            else:
                # Use double braces {{ }} to escape f-string for LaTeX \mathbf
                case1_latex.append(f"\\mathbf{{{round(h_val, 3)} \\not\\leq 0 \\text{{ (Constraint violated!)}}}}")
                case1_latex.append(r"\text{Conclusion: Case 1 is rejected.}")
        else:
            case1_latex.append(r"\text{No interior solution found.}")

    except Exception as e:
        status1 = "Rejected"
        case1_latex.append(f"\\text{{{{Error in Case 1: {str(e)}}}}}")

    # Now status1 is guaranteed to be accessed here
    steps.append({
        "title": "Step 4: Case Analysis (λ = 0)", 
        "status": status1, 
        "latex": case1_latex
    })

    # ===== CASE 2: h(x) = 0 (Boundary Optimum) =====
    status2 = "Rejected"
    case2_latex = [r"\text{From equation set (a):}"]
    
    try:
        # 1. Express variables in terms of lambda (Equation 2)
        sub_exprs = []
        for v in vars:
            # Solve dL/dv = 0 for variable v
            expr = solve(diff(L, v), v)
            if expr:
                sub_exprs.append(fr"{latex(v)} = {latex(expr[0])}")
        
        case2_latex.append(", \\text{ and } ".join([fr"{latex(diff(L, v))} = 0" for v in vars]))
        case2_latex.append(fr"\therefore " + ", \\text{ and } ".join(sub_exprs) + r" \dots (2)")

        # 2. Constraint logic (Equation 3)
        case2_latex.append(r"\text{Since } \lambda \neq 0, \text{ from equation (b):}")
        case2_latex.append(fr"({latex(h)}) = 0 \Rightarrow {latex(h)} = 0 \dots (3)")

        # 3. Solve the actual system
        sols_case2 = solve(grad_L + [h], list(vars) + [lam], dict=True)
        
        if sols_case2:
            sol = sols_case2[0]
            lam_val = float(N(sol[lam]))
            
            # Show substitution and lambda result (Equation 4)
            case2_latex.append(r"\text{Substituting equation (2) into (3):}")
            dual_sign = "\\geq 0" if problem_type == "max" else "\\leq 0"
            is_dual_feasible = (lam_val >= -0.001 if problem_type == "max" else lam_val <= 0.001)
            
            check_mark = r" \checkmark" if is_dual_feasible else ""
            case2_latex.append(fr"\Rightarrow \lambda = {round(lam_val, 3)} {dual_sign}{check_mark} \dots (4)")

            if is_dual_feasible:
                case2_latex.append(fr"\checkmark \text{{ KKT condition (d) is satisfied: }} \lambda {dual_sign}")
                
                # Primal values calculation
                case2_latex.append(r"\text{From equations (2) and (4), we get:}")
                point_details = [fr"{latex(v)} = {round(float(N(sol[v])), 3)}" for v in vars]
                case2_latex.append(", ".join(point_details))

                # Non-negativity Check (e) and Primal Feasibility (c)
                if all(float(N(sol[v])) >= -0.001 for v in vars):
                    status2 = "Accepted"
                    valid_points.append(sol)
                    case2_latex.append(fr"\checkmark \text{{ KKT condition (e) is satisfied: }} " + ", ".join([fr"{latex(v)} \geq 0" for v in vars]))
                    case2_latex.append(r"\checkmark \text{ KKT condition (c) is satisfied}")
                    case2_latex.append(r"\mathbf{\text{All KKT conditions are satisfied in Case 2!}}")
                    case2_latex.append(r"\text{Therefore, we have found a valid solution.}")
                else:
                    case2_latex.append(r"\text{Rejected: Condition (e) violated.}")
            else:
                case2_latex.append(fr"\text{{Rejected: Condition (d) violated (}} \lambda \not{dual_sign} \text{{).}}")
        else:
            case2_latex.append(r"\text{No boundary solution found.}")

    except Exception as e:
        status2 = "Rejected"
        case2_latex.append(fr"\text{{{{Error in Case 2: {str(e)}}}}}")

    steps.append({"title": "Step 5: Case Analysis (h(x) = 0)", "status": status2, "latex": case2_latex})

    # ===== STEP 6: FINAL ANSWER =====
    if not valid_points:
        steps.append({"title": "Final Solution", "is_final": True, "z": "Infeasible", "point": ["No Solution"]})
    else:
        best = valid_points[0]
        best_val = float(N(f.subs(best)))
        for pt in valid_points[1:]:
            v_val = float(N(f.subs(pt)))
            if (problem_type == "max" and v_val > best_val) or (problem_type == "min" and v_val < best_val):
                best = pt
                best_val = v_val
        
        # Format strings for Final Solution UI
        res_points = [fr"{latex(v)} = {round(float(N(best[v])), 3)} \approx {round(float(N(best[v])), 3)}" for v in vars]
        
        steps.append({
            "title": "Final Solution",
            "is_final": True,
            "point": res_points,
            "lambda": fr"\lambda = {round(float(N(best[lam])), 3)}",
            "z": fr"Z_{{{problem_type}}} = {round(best_val, 3)}",
            "explanation": fr"{problem_type.capitalize()} value successfully found at the optimal point"
        })

    return {"steps": steps}