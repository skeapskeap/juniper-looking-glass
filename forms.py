from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import IPAddress, Optional


class JunQuery(FlaskForm):
    query       = SelectField(choices=[('show bgp summary', 'bgp summary'),
                                       ('show route protocol bgp terse', 'bgp route terse'),
                                       ('show route protocol bgp detail', 'bgp route detail'),
                                       ('traceroute', 'traceroute'),
                                       ('ping', 'ping')
                                       ],
                              default='ping')
    ip_address  = StringField('IP address', validators=[Optional(), IPAddress(message='incorrect IP')])
    submit      = SubmitField('submit query')
