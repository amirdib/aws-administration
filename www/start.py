from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/status')
def read_status():
    with open('../status.log','r') as fin:
        content = fin.read()
    return content.replace('\n','<br>')

@app.route('/conf')
def conf():
    with open('../instances.conf','r') as fin:
        content = fin.read()
    return jsonify(content.replace('\n',''))

@app.route('/ignore')
def ignore():
    with open('../instances.ignore','r') as fin:
        content = fin.read()
    return jsonify(content)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

