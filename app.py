from flask import Flask, request, jsonify
from solver import solve_equation
from plotter import plot_2d, plot_3d

app = Flask(__name__)

@app.route('/')
def home():
    return "Math Solver - Resolva equações, derivadas, integrais e veja gráficos 2D/3D!"

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    problem = data.get('problem', '')
    problem_type = data.get('type', 'equation')

    if not problem:
        return jsonify({'error': 'Problema não fornecido'}), 400

    if problem_type == '3d':
        graph_3d = plot_3d(problem)
        if graph_3d:
            return jsonify({
                'result': 'Superfície 3D gerada',
                'explanation': f"Plotando {problem} em 3D.",
                'graph_2d': None,
                'graph_3d': graph_3d
            })
        return jsonify({'error': 'Erro ao gerar gráfico 3D'}), 400

    solutions, explanation, expr = solve_equation(problem, problem_type)
    if solutions is None:
        return jsonify({'error': explanation}), 400

    graph_2d = plot_2d(expr, problem) if expr and problem_type in ['equation', 'derivative', 'integral'] else None
    graph_3d = None

    return jsonify({
        'result': str(solutions),
        'explanation': explanation,
        'graph_2d': graph_2d,
        'graph_3d': graph_3d
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)