import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for

os.system("pip install psycopg2")

import os
import psycopg2

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DBNAME")
user = os.getenv("POSTGRES_USER")
 # If using Key Vault, retrieve password from there
password = os.getenv("POSTGRES_PASSWORD")  # Or retrieve from Key Vault

app = Flask(__name__)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template("frontend/index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
