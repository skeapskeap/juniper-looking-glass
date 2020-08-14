from flask_wtf import FlaskForm
from lg import COMMAND_LIST
from wtforms import SelectField, StringField, SubmitField


class JunQuery(FlaskForm):
    query       = SelectField(choices=COMMAND_LIST, default='ping',
                              render_kw={'class': 'form-control',
                                         'id': 'query_input'})
    target      = StringField('IP address',
                              render_kw={'class': 'form-control',
                                         'id': 'target_input'})
    submit      = SubmitField('submit query',
                              render_kw={'class': 'form-control',
                                         'id': 'show_reply'})
