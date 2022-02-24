const router = require('express').Router();
const { exec } = require('child_process');

router.get('/', (req, res) => {
  res.status(200).json({ message: 'You have reached the API endpoint' });
});

module.exports = router;
