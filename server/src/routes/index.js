const md5 = require('md5');
const redis = require('redis');
const axios = require('axios').default;
const router = require('express').Router();

const client = redis.createClient({
  url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`,
});

(async () => {
  await client.connect();
  console.log('Redis Connected !');
})();

router.get('/', (req, res) => {
  res.status(200).json({ message: 'You have reached the API endpoint' });
});

const cache = async (req, res, next) => {
  const submission = req.body;
  const submission_output = await client.get(
    md5(
      JSON.stringify({
        language: submission.language,
        code: submission.code,
        stdin: submission.stdin,
      })
    )
  );
  if (submission_output !== null) {
    console.log('Fetched from cache...');
    res.status(200).json({
      submission: { ...submission, output: JSON.parse(submission_output) },
    });
  } else {
    next();
  }
};

const runCode = async (req, res) => {
  const submission = req.body;
  const response = await axios.post('http://nginx/worker/run', submission);
  const response_data = response.data;
  await client.setEx(
    md5(
      JSON.stringify({
        language: submission.language,
        code: submission.code,
        stdin: submission.stdin,
      })
    ),
    3600,
    JSON.stringify(response_data.submission.output)
  );
  res.status(200).json(response_data);
};

router.post('/run', cache, runCode);

module.exports = router;
