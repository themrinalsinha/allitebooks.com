from flask   import Flask, render_template
from sqlite3 import connect
from os      import path


@app.route('/')
def index():
    return render_template('index.html', result = data)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')