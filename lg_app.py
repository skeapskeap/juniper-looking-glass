from flask import Flask, render_template
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
    form = JunQuery()
    if form.validate_on_submit():
        command = form.query.data
        ip = form.ip_address.data
        jun_response = reply_to_query(command, ip)
        return render_template('reply.html',
                                result=jun_response,
                                host=form.ip_address.data,
                                command=command)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
