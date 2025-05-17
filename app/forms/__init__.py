
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class InstituicaoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sigla = StringField('Sigla', validators=[DataRequired(), Length(max=10)])
    cidade = StringField('Cidade')
    tipo = SelectField('Tipo', choices=[('pública', 'Pública'), ('privada', 'Privada')])
    media_minima = FloatField('Média Mínima', validators=[NumberRange(min=0, max=10)])
    submit = SubmitField('Salvar')

class TurmaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    turno = StringField('Turno')
    instituicao_id = SelectField('Instituição', coerce=int)
    submit = SubmitField('Salvar')

class AlunoForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    telefone = StringField('Telefone')
    turma_id = SelectField('Turma', coerce=int)
    submit = SubmitField('Salvar')

class NotaForm(FlaskForm):
    p1 = FloatField('P1', validators=[NumberRange(min=0, max=10)])
    p2 = FloatField('P2', validators=[NumberRange(min=0, max=10)])
    lt = FloatField('ATV', validators=[NumberRange(min=0, max=10)])
    projeto = FloatField('Trabalho', validators=[NumberRange(min=0, max=10)])
    submit = SubmitField('Salvar')
