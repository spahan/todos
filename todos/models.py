from todos import db, app, mail

from flask import flash, Markup, url_for

from flask_login import UserMixin
from flask_mail import Message

from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

import json


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

    def create_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'id': self.id})

        if app.config['DEBUG']:
            flash(
                Markup('<b>DEBUG:</b> <a href={url}>{url}</a>'.format(
                    url=url_for('login_with_token', token=token, _external=True))),
                'warning')
            return

        # send login email
        msg = Message('Ohai!', recipients=[self.login])
        msg.body = 'Here is your login link: {}'.format(url_for('login_with_token', token=token, _external=True))

        mail.send(msg)

    @staticmethod
    def verify_login_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=10*60)
        except SignatureExpired:
            # valid token, but expired
            return None
        except BadSignature:
            # invalid token
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User {}>'.format(self.login)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    state = db.Column(db.Text)
    priority = db.Column(db.Integer)
    updates = db.relationship('Update', backref='todo', lazy='dynamic')

    ''' Zukunftsmusik
    not_before = db.Column(db.Date)
    parent = db.Column(db.Integer, db.ForeignKey('todo.id'))
    depends_on = db.Column(db.Text)
    '''


class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    __changes = db.Column('changes', db.Text)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def changes(self):
        return json.loads(self.__changes)

    @changes.setter
    def changes(self, changes):
        self.__changes = json.dumps(changes, default=str)
