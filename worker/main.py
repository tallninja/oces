from datetime import date
import json
import hashlib
import aioredis
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from models.submission import Submission
from jobs.isolate import IsolateJob


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = aioredis.from_url('redis://redis:6379')


@app.get('/')
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {'message': 'worker'}


@app.post('/run')
async def run_code(submission: Submission, response: Response):
    key_str = json.dumps({'language': submission.language,
                         'code': submission.code, 'stdin': submission.stdin})
    key = hashlib.md5(key_str.encode()).hexdigest()
    output = await redis.get(key)
    if output:
        print(f'{date.today()} Fetched from cache... !')
    else:
        print(f'{date.today()} Performing Job...')
        output = json.dumps(IsolateJob.perform(
            submission=submission), indent=4)
        await redis.set(name=key, value=output, ex=3600)

    submission.output = json.loads(output)

    response.status_code = status.HTTP_200_OK
    return {'submission': submission}
