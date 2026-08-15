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


@app.route('/workspace')
def workspace():
    project_path = request.args.get('path', '').strip()
    if not project_path:
        project_path = os.path.join(os.getcwd(), 'default_project')
    config_data = ConfigEngine.load_project_workspace(project_path)
    validation = ConfigEngine.validate_parameters(config_data)
    return render_template(
        'workspace.html',
        project_path=project_path,
        config_data=config_data,
        validation=validation
    )

if __name__ == '__main__':

    app.run(debug=True, port=8080)
