require('module-alias/register');

const App = require('@src/app');

const app = new App();

const PORT = process.env.PORT || 5000;
app.run(PORT);
