from flask import Flask, request, jsonify
from kkt_solver import solve_kkt

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_api():
    data = request.json
    n = data.get('n', 2)
    obj_str = data.get('objective')
    const_str = data.get('constraint')
    p_type = data.get('type', 'max')
    
    result = solve_kkt(n, obj_str, const_str, p_type)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True)