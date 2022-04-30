const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const routes = require('@routes');

class App {
  constructor() {
    this.app = express();
  }

  init = () => {
    let app = this.app;
    app.use(cors());
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    process.env.NODE_ENV == 'production'
      ? app.use(morgan('common'))
      : app.use(morgan('dev'));
  };

  run = (port) => {
    let app = this.app;
    this.init();
    app.get('/', (req, res) => {
      res.status(200).json({ message: 'Connected to server !' });
    });
    app.use('/api', routes);
    app.listen(port, (err) => {
      if (err) console.error('Error', err);
      else console.log(`Server listening on PORT: ${port}`);
    });
  };
}

module.exports = App;
