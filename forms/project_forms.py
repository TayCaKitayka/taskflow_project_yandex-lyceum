from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    title = StringField(
        "Название проекта",
        validators=[DataRequired(), Length(min=2, max=100)],
    )
    description = TextAreaField("Описание")
    submit = SubmitField("Сохранить")
