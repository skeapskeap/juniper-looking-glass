from flask import Flask, render_template, jsonify, request, url_for
from forms import JunQuery
from lg import reply_to_query
from settings import APP_SECRET_KEY

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


@app.route('/')
def index():
    form = JunQuery()
    return render_template('index.html', form=form)


@app.route('/query', methods=('GET', 'POST'))
def query():
    command = request.form['message']
    target = request.form['target']
    jun_response = reply_to_query(command, target)

    reply, message = jun_response
    if reply:
        reply = '<br>'.join(reply)
        return jsonify({'reply': reply,
                        'message': f'# {message}'})

    return jsonify({'error': message})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='88')
