from  flask import Flask, jsonify, request
from utils import create_sandbox, cleanup, create_run_script, create_compile_script, compile_code, create_source_file, run

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({ 'message': 'worker' })

@app.route('/run', methods=['POST'])
def run_code():
    box_id = 36
    workdir = create_sandbox(box_id=box_id)
    boxdir = f'{workdir}/box'
    tmpdir = f'{workdir}/tmp'
    data = request.get_json()
    create_source_file(boxdir=boxdir, data=data.get('code'))
    create_compile_script(boxdir=boxdir, compile_cmd=data.get('compile_cmd'))
    compile_code(box_id=box_id, boxdir=boxdir)
    create_run_script(boxdir=boxdir, run_cmd=data.get('run_cmd'))
    output = run(box_id=box_id, boxdir=boxdir)
    cleanup(box_id=box_id, boxdir=boxdir, tmpdir=tmpdir)
    return jsonify({ 'output': output })
    
    

