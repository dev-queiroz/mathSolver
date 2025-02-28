from flask import Flask, request, jsonify
import logging
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Acessando a rota inicial")
    return "Math Solver - Resolva equações, derivadas, integrais e veja gráficos 2D/3D!"

@app.route('/solve', methods=['POST'])
def solve():
    from solver import solve_equation  # Importação sob demanda
    from plotter import plot_2d, plot_3d  # Importação sob demanda
    
    logger.info("Recebendo requisição para /solve")
    data = request.json
    problem = data.get('problem', '')
    problem_type = data.get('type', 'equation')

    if not problem:
        logger.error("Problema não fornecido")
        return jsonify({'error': 'Problema não fornecido'}), 400

    if problem_type == '3d':
        logger.info(f"Gerando gráfico 3D para: {problem}")
        graph_3d = plot_3d(problem)
        if graph_3d:
            return jsonify({
                'result': 'Superfície 3D gerada',
                'explanation': f"Plotando {problem} em 3D.",
                'graph_2d': None,
                'graph_3d': graph_3d
            })
        logger.error("Erro ao gerar gráfico 3D")
        return jsonify({'error': 'Erro ao gerar gráfico 3D'}), 400

    logger.info(f"Resolvendo {problem_type}: {problem}")
    solutions, explanation, expr = solve_equation(problem, problem_type)
    if solutions is None:
        logger.error(f"Erro na resolução: {explanation}")
        return jsonify({'error': explanation}), 400

    graph_2d = plot_2d(expr, problem) if expr and problem_type in ['equation', 'derivative', 'integral'] else None
    graph_3d = None

    logger.info("Requisição processada com sucesso")
    return jsonify({
        'result': str(solutions),
        'explanation': explanation,
        'graph_2d': graph_2d,
        'graph_3d': graph_3d
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa a porta da Render ou 5000 localmente
    logger.info(f"Iniciando o servidor Flask na porta {port}")
    app.run(host='0.0.0.0', port=port)