

class DisciplinaForm(FlaskForm):
    nome = StringField('Nome da Disciplina', validators=[DataRequired()])
    professor = StringField('Professor Responsável')
    turma_id = SelectField('Turma', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')


class MatriculaForm(FlaskForm):
    aluno_id = SelectField('Aluno', coerce=int, validators=[DataRequired()])
    disciplina_id = SelectField('Disciplina', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Matricular')

# No arquivo forms.py
class AlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email')
    telefone = StringField('Telefone')  # Adicione se necessário
    turma_id = SelectField('Turma', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')