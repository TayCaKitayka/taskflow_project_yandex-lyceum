from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    title = StringField(
        "Название задачи",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    description = TextAreaField("Описание")
    status = SelectField(
        "Статус",
        choices=[
            ("Новая", "Новая"),
            ("В работе", "В работе"),
            ("Готово", "Готово"),
        ],
    )
    priority = SelectField(
        "Приоритет",
        choices=[
            ("Низкий", "Низкий"),
            ("Средний", "Средний"),
            ("Высокий", "Высокий"),
        ],
    )
    deadline = DateField("Дедлайн", validators=[Optional()])
    submit = SubmitField("Сохранить")
