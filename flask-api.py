from flask import Flask
import subprocess

venv_python = "venv/Scripts/python"

app = Flask(__name__)

@app.route('/road')
def run_script3():
    subprocess.Popen([venv_python, 'script-road.py'])
    return 'Script Road executed.'

@app.route('/public')
def run_script2():
    subprocess.Popen([venv_python, 'script-public.py'])
    return 'Script Public executed.'

@app.route('/domestic')
def run_script1():
    subprocess.Popen([venv_python, 'script-domestic.py'])
    return 'Script Domestic executed.'

if __name__ == '__main__':
    app.run(debug=True)

