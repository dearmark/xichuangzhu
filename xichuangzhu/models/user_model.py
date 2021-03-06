#-*- coding: UTF-8 -*-
import datetime
from xichuangzhu import db
from xichuangzhu.utils import check_is_me

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    abbr = db.Column(db.String(50))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    signature = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=False)
    check_inform_time = db.Column(db.DateTime, default=datetime.datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<User %s>' % self.name

    @property
    def friendly_name(self):
        return '我' if check_is_me(self.id) else self.name