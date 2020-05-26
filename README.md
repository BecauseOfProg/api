<div align="center">
    <img src="https://cdn.becauseofprog.fr/logos/bop-transparent.png" width="100" />
    <h1>BecauseOfProg - API</h1>
    <a href="https://github.com/BecauseOfProg/api-docs">Documentation</a> - <a href="./LICENSE">License</a>
</div>

This is the main API for all the BecauseOfProg. It's an interface to interact with users, posts and to use authentification on other websites.

- [💻 Development](#-development)
  - [Project setup](#project-setup)
  - [Serve for development](#serve-for-development)
  - [Build for production](#build-for-production)
- [📜 Credits](#-credits)
- [🔐 License](#-license)

## 💻 Development

### Project setup

First, install Python 3.7 or higher, and install the dependencies like below.

#### Option 1 : use pipenv (recommended)

Install pipenv using pip and, with it, install the dependencies : `pipenv install`.

#### Option 2 : use pip (classic)

Use pip to install the dependencies listed in the `requirements.txt` file.

### Serve for development

If you use Pipenv, enter in your virtual environment : `pipenv shell`.

Configure the environment variables :

- `FLASK_APP` : path to main.py
- `FLASK_ENV` : "development"

Edit the configuration in `config-sample.json`, and rename this file to `config.json`.

Run the API using `flask run`.

### Build for production

Install the `flup` package. Then, edit the `api.fcgi` file to add path to Python folder, and the socket file that will be generated. Finaly, run the file and connect the socket on your web server !

If you use Pipenv, be careful to precise the path to the virtual environment !

## 📜 Credits

- Maintainer: [Théo Vidal (exybore)](https://github.com/exybore)

## 🔐 License

GNU GPL v3. See the [license file](./LICENSE).
