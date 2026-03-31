from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "kkt_secret_key"
BACKEND_URL = "http://127.0.0.1:5001/solve"

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/input')
def input_page():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_route():
    payload = {
        "n": int(request.form.get('n')),
        "objective": request.form.get('f'),
        "constraint": request.form.get('g'),
        "type": request.form.get('type')
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        session['data'] = response.json()
        return redirect(url_for('result_page'))
    except:
        return "Error: Ensure Backend (port 5001) is running!"

@app.route('/result')
def result_page():
    data = session.get('data')
    if not data: return redirect(url_for('input_page'))
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)