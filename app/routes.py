from datetime import timedelta

from flask import render_template, url_for, flash, redirect
from flask_restful import Api

from app import app
from app import db
from app.forms import New_category, New_habit, Building_habit, Delete_habit, DateHabitReport
from app.models import Category, Habit, Date
from app.resources import CategoryResource
from sqlalchemy import update
from flask_sqlalchemy import SQLAlchemy

#todo change model to done/not done, category name in date

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
api = Api(app)

api.add_resource(CategoryResource, '/category1/<string:name>')


@app.route("/")
@app.route("/home")
def home():
    form = Building_habit()
    habits = Date.query.filter_by(date='2020-05-10').all()
    habit_list = []
    for habit in habits:
        habit_list.append(Habit.query.filter_by(id=habit.id).first().name)
    print(habit_list)
    return render_template('home.html', form=form, habits=habit_list)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/category", methods=['POST', 'GET', 'DELETE'])
def category():
    form = New_category()
    form_delete = Delete_habit()
    date = Date.find_date_by_habit_id_and_date(_id=12, date='2020-05-11')
    for i in range(Category.query.count()):
        print(i)
    form.submit()
    if form.validate_on_submit():
        print('under POST')
        new_category = Category(category=form.category.data)
        Category.save_to_db(new_category)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    if form_delete.validate_on_submit():
        print('under DELETE')
        print(form_delete.category_type.data, 'category type ')
        category_to_delete = Category.find_by_id(form_delete.category_type.data)
        print(category_to_delete, 'asdfasdf')
        db.session.delete(category_to_delete)
        db.session.commit()
        flash('Your DELETE has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('category.html', title='New Category',
                           form=form, form_delete=form_delete, legend='New Category')


@app.route("/report", methods=['POST', 'GET', 'DELETE'])
def report():
    form = DateHabitReport()
    form_delete = Delete_habit()
    dates = Date.find_habits_by_date('2020-05-11')
    form.submit()
    if form.validate_on_submit():
        number_of_dates = 1
        choosen_date = str(form.selected_date.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('report_with_date', number_of_dates=number_of_dates, choosen_date=choosen_date))
    return render_template('report.html',
                           form=form)


@app.route("/report/<number_of_dates>/<choosen_date>", methods=['POST', 'GET', 'DELETE'])
def report_with_date(number_of_dates, choosen_date):
    form = DateHabitReport()
    form_done = Building_habit()
    all_date_objects = [Date.find_habits_by_date(single_list) for single_list in choosen_date.split(',')]

    print (all_date_objects)
    form_done.submit_done_or_not()
    if form_done.validate_on_submit():
        date = Date.query.filter_by(id=form_done.date_id.data).first()
        date.done = True
        db.session.commit()
        flash('Your DELETE has been created!', 'success')
        return render_template('report.html',
                               form=form, number_of_dates=number_of_dates, choosen_date=choosen_date,
                               all_date_objects=all_date_objects, form_done=form_done)

    form.submit()
    if form.validate_on_submit():
        number_of_dates = 1 + int(number_of_dates)
        choosen_dates = choosen_date + ',' + str(form.selected_date.data)
        print(choosen_dates, 'ciekawe co to za string')
        flash('Your post has been created!', 'success')
        return redirect(url_for('report_with_date', number_of_dates=number_of_dates, choosen_date=choosen_dates))
    return render_template('report.html',
                           form=form, number_of_dates=number_of_dates, choosen_date=choosen_date, all_date_objects=all_date_objects, form_done=form_done)


@app.route("/showcat")
def show_cat():
    cat = Category.query.all()
    return render_template('showcat.html', cat=cat)


@app.route("/category/<name>")
def myhabit(name):
    allcategory = Category.find_by_category(name)
    myhabits = Habit.find_by_category_id(allcategory.id)
    return render_template('myhabit.html', myhabits=myhabits, category=name)


@app.route("/index")
def index():
    # TODO lista nawyków dla danej kategori
    a_user = Date.query.filter_by(id='1').first()
    a_user.done = True
    db.session.commit()
    # Date.query.update().\
    #         where(Date.id==1).\
    #         values(done='true')
    return render_template('index.html')


@app.route("/new_habit", methods=['POST', 'GET'])
def new_habit():
    db.session.modified = True

    form = New_habit()
    category_list = Category.list_of_category()
    form.submit()
    if form.validate_on_submit():
        new_record = Habit(name=form.name.data, category_id=form.category_type.data, date_start=form.start_date.data,
                           priority=form.priority.data, date_end=form.end_date.data)
        Habit.save_to_db(new_record)
        new_habit_id = Habit.query.filter_by(name=form.name.data).first().id
        for single_date in daterange(form.start_date.data, form.end_date.data):
            dates = Date(date=single_date, habit_id=new_habit_id, category_id=form.category_type.data)
            Date.save_to_db(dates)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('habit.html', title='New Category',
                           form=form, legend='New Category', category_list=category_list)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

        # if form.validate_on_submit():
        #        print('under POST')
        #        cat = Category(category=form.category.data)
        #        db.session.add(cat)
        #        db.session.commit()
        #        flash('Your post has been created!', 'success')
        #        return redirect(url_for('home'))
