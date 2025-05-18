

class DisciplinaForm(FlaskForm):
    nome = StringField('Nome da Disciplina', validators=[DataRequired()])
    professor = StringField('Professor Responsável')
    turma_id = SelectField('Turma', coerce=int)
    submit = SubmitField('Salvar')


class MatriculaForm(FlaskForm):
    aluno_id = SelectField('Aluno', coerce=int)
    disciplina_id = SelectField('Disciplina', coerce=int)
    submit = SubmitField('Matricular')
