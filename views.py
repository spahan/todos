from models import *
from forms import *
from todos import app, db, login_manager

from flask import render_template, redirect, escape, jsonify

from flask_login import login_user, logout_user, login_required, current_user

from flask_sqlalchemy import inspect

from email_validator import validate_email

from jinja2 import evalcontextfilter

import json

import re

import babel


@app.route('/')
@login_required
def index():
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
# @limiter.limit('10/hour')
def login():
    loginform = LoginForm()

    if loginform.validate_on_submit():
        email = loginform.login.data.lower()

        try:
            v = validate_email(email)
            email = v['email'] # replace with normalized form

        except Exception as e:
            loginform.login.errors.append(str(e))

            return render_template('login.html', loginform=loginform)

        user = User.query.filter(User.login == email).first()

        if user is None:
            # create user
            user = User(login=email)
            db.session.add(user)
            db.session.commit()

        # create token
        user.create_token()

        flash('Check your inbox!')

    return render_template('login.html', loginform=loginform)


@app.route('/login/token/<token>')
def login_with_token(token):
    user = User.verify_login_token(token)

    if user:
        login_user(user)

        return redirect(url_for('index'))
    else:
        flash('Invalid or expired token!')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash('You have been logged out.')

    return redirect(url_for('login'))


@app.route('/todos/list')
def list_todos():
    todos = Todo.query.all()

    pending = []
    open = []
    for todo in todos:
        if todo.state == 'done':
            pass
        elif todo.due_date is not None and todo.due_date <= datetime.date.today():
            pending.append(todo)
        else:
            open.append(todo)

    help_needed = Todo.query.filter(Todo.state == 'help_needed')

    return render_template('todo_list.html', pending=pending, open=open, help_needed=help_needed)

@app.route('/todos/add', defaults={'id': None}, methods=['GET', 'POST'])
@app.route('/todos/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id=None):
    with db.session.no_autoflush:
        if id is not None:
            todo = db.session.query(Todo).get(id)

            if not (current_user.id == todo.user_id or current_user.role in ['helpdesk', 'admin']):
                todo = None

        else:
            todo = Todo()

        if todo is not None:
            todoform = TodoForm(obj=todo)

            # Default for select field, because it gets overwritten by the above statement.
            todoform.priority.data = (todoform.priority.data if todoform.priority.data else todoform.priority.default)

            if todoform.validate_on_submit():
                todoform.populate_obj(todo)

                if id is None:
                    todo.user_id = current_user.id
                    todo.created = datetime.datetime.now()
                    todo.state = 'open'

                    db.session.add(todo)
                else:
                    db.session.merge(todo)

                    changes = []

                    for t in db.session.dirty:
                        attrs = inspect(t).attrs
                        for attr in attrs:
                            if attr.history.has_changes():
                                changes.append({
                                    'field': attr.key,
                                    'old': attr.history.deleted[0],
                                    'new': attr.history.added[0]  # or attr.value
                                })

                        if len(changes) > 0 or todoform.comment.data is not '':
                            u = Update(
                                todo_id=todo.id,
                                user_id=current_user.id,
                                comment=todoform.comment.data,
                                changes=changes
                            )
                            db.session.add(u)

                db.session.commit()
                flash('Saved')

                if id is None:
                    return redirect(url_for('edit_todo', id=todo.id))
        else:
            todoform = TodoForm
            flash('Not authorized')

    return render_template('todo_edit.html', todoform=todoform, todo=todo)


@app.route('/todos/view/<int:id>')
def view_todo(id):
    todo = Todo.query.get(id)
    updates = Update.query.filter(Update.todo_id == id).all()

    for u in updates:
        print(type(u.changes))

    return render_template('todo_details.html', todo=todo, updates=updates)


def format_datetime(value):
    format = "EE, dd.MM.y"
    return babel.dates.format_datetime(value, format) if value is not None else "not set"


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){1,}')


@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'<br />\n'.join(_paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['nl2br'] = nl2br


@app.context_processor
def inject_global_template_vars():
    return dict(app_name=app.config['APP_NAME'])


@app.context_processor
def inject_today():
    return dict(today=datetime.date.today())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

