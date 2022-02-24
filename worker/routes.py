from  flask import Flask, jsonify, request
from jobs.isolate import IsolateJob

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({ 'message': 'worker' })

@app.route('/run', methods=['POST'])
def run_code():
    box_id = 8
    data = request.get_json()
    output = IsolateJob.perform(box_id=box_id, submission=data)
    
    return jsonify({ 'output': output })
    
    

