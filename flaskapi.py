from flask import Flask
import subprocess

venv_python = "C:/Users/Martin Joseph Juneie/Documents/cctvBack/venv/Scripts/python"

app = Flask(__name__)

@app.route('/road')
def run_script3():
    # Execute script3.py
    subprocess.Popen([venv_python, 'Road/trialrun.py'])
    return 'Script 3 executed.'

@app.route('/public')
def run_script2():
    # Execute script2.py
    subprocess.Popen([venv_python, 'Public/weaponfire.py'])
    return 'Script 2 executed.'

@app.route('/domestic')
def run_script1():
    # Execute script1.py
    subprocess.Popen([venv_python, 'Domestic/TestRun.py'])
    return 'Script 1 executed.'

if __name__ == '__main__':
    app.run(debug=True)

