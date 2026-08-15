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

@app.route('/api/config/save', methods=['POST'])
def save_config():
    data = request.json or {}
    project_path = data.get('project_path', '').strip()
    config_data = data.get('config_data', {})

    if not project_path:
        return jsonify({'status': 'error', 'message': 'Missing project_path'}), 400

    try:
        os.makedirs(project_path, exist_ok=True)
        for category, params in config_data.items():
            file_name = f"{category}.dat"
            file_path = os.path.join(project_path, file_name)
            ConfigEngine.write_dat_file(file_path, params, header_comment=f"{category} Simulation Parameters")

        updated_config = ConfigEngine.load_project_workspace(project_path)
        validation = ConfigEngine.validate_parameters(updated_config)

        return jsonify({
            'status': 'success',
            'message': 'Configuration parameters saved successfully!',
            'validation': validation
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/validate', methods=['POST'])
def validate_route():
    data = request.json or {}
    config_data = data.get('config_data', {})
    validation = ConfigEngine.validate_parameters(config_data)
    return jsonify(validation)

@app.route('/api/export', methods=['GET'])
def export_workspace():
    project_path = request.args.get('path', '').strip()
    if not project_path or not os.path.exists(project_path):
        return jsonify({'status': 'error', 'message': 'Invalid project path'}), 400

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith('.dat'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, project_path)
                    zf.write(full_path, rel_path)
    memory_file.seek(0)
    folder_name = os.path.basename(os.path.normpath(project_path)) or 'simulation_config'
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{folder_name}_config.zip'
    )

if __name__ == '__main__':



    app.run(debug=True, port=8080)
