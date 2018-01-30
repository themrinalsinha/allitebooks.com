from flask   import Flask, render_template
from sqlite3 import connect
from os      import path

path = path.dirname(path.realpath(__file__))
app  = Flask(__name__, static_folder = path, template_folder = path)
db   = path + '/allitebooks.db'

connection = connect(db)
cursor     = connection.cursor()
data       = cursor.execute("SELECT category, book_name, cover_img, authors, pages, \
                             description, file_size, download_link FROM ebooks_index LIMIT 100").fetchall()

@app.route('/')
def index():
    return render_template('index.html', result = data)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')