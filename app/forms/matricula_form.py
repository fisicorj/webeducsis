
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class MatriculaForm(FlaskForm):
    aluno_id = SelectField('Aluno', coerce=int, validators=[DataRequired()])
    disciplina_id = SelectField('Disciplina', coerce=int, validators=[DataRequired()])
