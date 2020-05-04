from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms_components import DateRange
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Category
from app.resources import Category_resources
from datetime import datetime, date
from wtforms.fields.html5 import DateField


class New_category(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField()

class New_habit(FlaskForm):

    category_list = Category_resources.list_of_category()
    choice = [(Category.query.filter_by(
        category=category_name).first().id, category_name) for category_name in category_list]

    name = TextAreaField('Name', validators=[DataRequired()])
    category_type = SelectField('Type',coerce=int, validators=[DataRequired()], choices=choice)
    start_date = DateField('start_date', format='%Y-%m-%d', validators=[DateRange(min=date.today())])
    end_date = DateField('end_date', format='%Y-%m-%d', validators=[DateRange(min=date.today())])
    submit = SubmitField()


def get_category():
    return New_category.query