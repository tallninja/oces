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
  const submission = JSON.stringify(req.body);
  const submission_output = await client.get(md5(submission));
  if (submission_output !== null) {
    console.log('Fetched from cache...');
    res.status(200).json(JSON.parse(submission_output));
  } else {
    next();
  }
};

const runCode = async (req, res) => {
  const submission = req.body;
  const response = await axios.post('http://nginx/worker/run', submission);
  const output = response.data;
  await client.setEx(
    md5(JSON.stringify(submission)),
    3600,
    JSON.stringify(output)
  );
  res.status(200).json(output);
};

router.post('/run', cache, runCode);

module.exports = router;
