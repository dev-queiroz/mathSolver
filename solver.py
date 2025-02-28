import sympy as sp
import numpy as np

def solve_equation(equation_str, problem_type='equation'):
    x, y = sp.Symbol('x'), sp.Symbol('y')
    try:
        if problem_type == 'equation':
            if ';' in equation_str:  # Sistema de equações
                eqs = [sp.sympify(eq.split('=')[0] + '-' + eq.split('=')[1]) for eq in equation_str.split(';')]
                solutions = sp.solve(eqs, (x, y))
                explanation = f"Resolvendo sistema {equation_str}: soluções são {solutions}."
                return solutions, explanation, None
            elif '=' in equation_str:
                left, right = equation_str.split('=')
                expr = sp.sympify(f"{left} - ({right})")
                solutions = sp.solve(expr, x)
                explanation = f"Resolvendo {equation_str} = 0: soluções são {solutions}."
            else:
                expr = sp.sympify(equation_str)
                solutions = [sp.N(expr)]
                explanation = f"Avaliando {equation_str}: resultado é {solutions[0]}."
            return solutions, explanation, expr

        elif problem_type == 'derivative':
            expr = sp.sympify(equation_str)
            result = sp.diff(expr, x)
            explanation = f"Derivada de {equation_str}: {result}."
            return result, explanation, result

        elif problem_type == 'integral':
            parts = equation_str.split(',')
            if len(parts) == 3:  # Integral definida: "x^2,0,1"
                expr, a, b = sp.sympify(parts[0]), float(parts[1]), float(parts[2])
                result = sp.integrate(expr, (x, a, b))
                explanation = f"Integral definida de {parts[0]} de {a} a {b}: {result}."
            else:  # Integral indefinida
                expr = sp.sympify(equation_str)
                result = sp.integrate(expr, x)
                explanation = f"Integral indefinida de {equation_str}: {result} + C."
            return result, explanation, result

        elif problem_type == 'matrix':
            matrix = sp.Matrix(eval(equation_str))
            det = matrix.det()
            eigenvals = list(matrix.eigenvals().keys())
            explanation = f"Matriz {equation_str}: determinante = {det}, autovalores = {eigenvals}."
            return {'det': det, 'eigenvals': eigenvals}, explanation, None

    except Exception as e:
        return None, f"Erro: {str(e)}", None