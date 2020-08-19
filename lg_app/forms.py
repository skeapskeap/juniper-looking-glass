from lg_app.config import INPUT_CHOICE
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField


class JunQuery(FlaskForm):
    query       = SelectField(choices=INPUT_CHOICE, default=INPUT_CHOICE[-1],
                              render_kw={'class': 'form-control',
                                         'id': 'command_input'})
    target      = StringField('IP address',
                              render_kw={'class': 'form-control',
                                         'id': 'target_input'})
    submit      = SubmitField('submit query',
                              render_kw={'class': 'form-control',
                                         'id': 'show_reply'})
