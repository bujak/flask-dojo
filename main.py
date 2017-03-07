from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

DATABASE = 'flask_dojo.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def main():
    return ''

@app.route('/request-counter', methods=['GET', 'POST'])
def request_counter():

    values = (request.method, )
    query = """SELECT request_counter from requests where request_name =?"""
    curr = get_db().cursor()
    curr.execute(query, values)
    counter = curr.fetchall()[0][0]
    counter += 1

    query_update = """UPDATE requests set request_counter =? WHERE request_name = ?"""
    values = (counter, request.method)
    curr.execute(query_update, values)
    get_db().commit()

    return render_template('request-counter.html')

if __name__ == '__main__':
    app.run(debug=True)