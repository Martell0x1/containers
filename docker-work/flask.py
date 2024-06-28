from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/Sel3awee')
def test():
        return 'A7la mesa 3alek ya 2albe <3'

if __name__ == '__main__':
        app.run(debug=False,host='0.0.0.0',port=5000)