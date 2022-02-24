from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from models.models import Submission
from jobs.isolate import IsolateJob


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {'message': 'worker'}


@app.post('/run')
async def run_code(submission: Submission, response: Response):
    box_id = 17
    output = IsolateJob.perform(box_id=box_id, submission=submission)
    response.status_code = status.HTTP_200_OK
    return {'output': output}
