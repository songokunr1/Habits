from app.models import Category, Habit, Date, Database
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import New_category, New_habit, Building_habit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date


from app.resources import Category_resources

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


@app.route("/")
@app.route("/home")
def home():
    form = Building_habit()
    return render_template('home.html', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/category", methods= ['POST', 'GET'])
def category():
    form = New_category()

    print(form)
    print(request.method)
    for i in range(Category.query.count()):
        print(i)
    #print(Category.statement.execute().fetchall())
    #print(Category.query.all())
    print(Category.find_by_id(1))
    print(Category.find_by_id(2))
    #print(Category.list_of_ids)
    #print(db.session.query(Category.id).all()[1][0]) - iterowanie po row
    print(Category.find_by_id(db.session.query(Category.id).all()[1][0]))
    #print(Category.list_of_ids2)
    # print(Database.list_of_ids(Category), 'Database')
    # print(Database.find_by_id(Category, 1), 'database look by id')
    print(db.session.query(Category.id).all()[0], 'list of ids')
    # print(Database.list_of_column(Category, category, Database.list_of_ids(Category)))
    #print(Category.category_column(), 'all category')
    print(Habit.query.all(), 'lista')
    #print(Database.column_with_id(Category, Category.category, ))
    cate = Category.query.get_or_404(1)
    print(form.validate_on_submit())
    form.submit()
    print(form.validate_on_submit())
    #print(SQLAlchemy.execute("SELECT * FROM category"))
    print(Category_resources.list_of_category(), 'resources model')
    if form.validate_on_submit():
        print('under POST')
        cat = Category(category=form.category.data)
        db.session.add(cat)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('category.html', title='New Category',
                           form=form, legend='New Category')

@app.route("/showcat")
def show_cat():
    cat=Category.query.all()
    return render_template('showcat.html', cat=cat)

@app.route("/myhabit/<habits>")
def myhabit(habits):
    incategory = Category.query.filter_by(category=habits).first()
    myhabits = Habit.query.filter_by(category_id=incategory.id).all()
    print(myhabits)
    #TODO lista nawyków dla danej kategori
    return render_template('myhabit.html', myhabits=myhabits, category=habits)

@app.route("/new_habit", methods= ['POST', 'GET'])
def new_habit():
    form = New_habit()

    category_list = Category_resources.list_of_category()
    choice = [(Category.query.filter_by(category=category_name).first().id, category_name) for category_name in category_list]
    print( choice, ' Choice')
    print(form.data, 'form full')
    print(form.name.data, 'name data')
    print(form.start_date.data, 'name data')
    print(form.end_date.data, 'name data')
    print(form.category_type.data, 'type.data')
    print(category_list, 'category list')
    print(form, 'form')
    print(Category.query.first().id, 'reczna query')
    print(Category_resources.find_by_category(Category, 'angielski').first().id, 'find by category')
    print(request.method)
    print(form.validate_on_submit())
    # print(request.form.get('cat_name'), 'cat_name variable')
    form.submit()
    print(form.category_type.type, 'category type', form.name.name, 'category name')
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('under POST')
        print(form.name.data, 'name data')
        print(form.category_type.data, 'type.data')
        name = Habit(name=form.name.data, category_id=form.category_type.data, date_start=form.start_date.data, date_end=form.end_date.data)
        db.session.add(name)
        db.session.commit()
        new_habit_id = Habit.query.filter_by(name=form.name.data).first().id
        for single_date in daterange(form.start_date.data, form.end_date.data):
            dates = Date(date=single_date, habit_id = new_habit_id)
            db.session.add(dates)
            db.session.commit()

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

