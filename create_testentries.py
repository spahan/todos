#!/usr/bin/env python

'''
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    not_before = db.Column(db.Date)
    due_date = db.Column(db.Date)
    priority = db.Column(db.Integer)
    parent = db.Column(db.Integer, db.ForeignKey('todo.id'))
    depends_on = db.Column(db.Text)
    state = db.Column(db.Text)
    updates = db.relationship('Update', backref='todo', lazy='dynamic')
'''

from todos import db
from views import Todo
from datetime import datetime

t = Todo(user_id=1,
         title='Test Todo',
         description='Das ist ein Todo.\nDas ist die zweite Zeile.\n Tolles Todo. Da müsste man echt mach was machen. '
                     'Aber wer bloß? Und wie erklärt man das den Leuten jetzt am besten?',
         due_date=datetime(year=2019, month=9, day=30, hour=13, minute=37),
         priority=2,
         state='help_needed')

db.session.add(t)
db.session.commit()

