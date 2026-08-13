import os
import io
import zipfile
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from config_engine import ConfigEngine

app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_project')
def new_project():
    return render_template('new_project.html')

@app.route('/open_project')
def open_project():
    return render_template('open_project.html')

@app.route('/new_project_submit', methods=['POST'])
def new_project_submit():
    folder = request.form.get('P_Folder', '').strip()
    if not folder:
        folder = os.path.join(os.getcwd(), 'default_project')
    ConfigEngine.create_project_workspace(folder)
    return redirect(url_for('workspace', path=folder))

@app.route('/open_project_submit', methods=['POST'])
def open_project_submit():
    folder = request.form.get('P_Folder', '').strip()
    if not folder:
        folder = os.path.join(os.getcwd(), 'default_project')
    ConfigEngine.load_project_workspace(folder)
    return redirect(url_for('workspace', path=folder))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
