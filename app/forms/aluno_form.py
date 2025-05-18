
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email
from app.models import Turma

class AlunoForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    telefone = StringField('Telefone')
    turma_id = SelectField('Turma', coerce=int, validators=[DataRequired()])
