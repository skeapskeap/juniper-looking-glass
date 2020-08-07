from flask import Flask, render_template
from lg import connect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reply')
def reply():
    jun_response = connect('show bgp summary')
    return render_template('reply.html', result=jun_response)


if __name__ == '__main__':
    app.run(debug=True)
