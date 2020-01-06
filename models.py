from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
)


attendance = db.Table('attendance',
    db.Column('calendar_id', db.Integer, db.ForeignKey('calendar.calendar_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)

class Auth(db.Model):
    __tablename__="auth"
    id = db.Column(db.Integer, primary_key = True)
    token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone = False))
    is_valid = db.Column(db.Boolean)
    login_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
         return '<Auth %r>' % self.token

class User(db.Model):
    __tablename__="user"
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    birthday_date = db.Column(db.String(8))
    auths = db.relationship('Auth', backref ='user')
    calendars = db.relationship('Calendar', backref = 'user') 
    favs = db.relationship('Category', secondary = favorite, backref = 'user')

    def __repr__(self):
         return '<User %r>' % self.name

    def serialize(self):
         return {
             "name": self.name,
             "last_name": self.last_name,
             "email": self.email,
             "birthday_date": self.birthday_date,
             "favs": list(map(lambda x: x.serialize(), self.favs))
            }


class Calendar(db.Model):
    __tablename__="calendar"
    calendar_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable = False)
    description = db.Column(db.String(300), nullable = True)
    calendar_id_owner = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    attendances = db.relationship('Event', secondary = attendance, backref = 'calendar')

    def __repr__(self):
         return '<Calendar %r>' % self.name

    def serialize(self):
        return {
             "calendar_id": self.calendar_id,
             "name_calendar": self.name,
            "description": self.description,
             "calendar_id_owner": self.calendar_id_owner
            }

class Category(db.Model):
    __tablename__="category"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable = False)
    events = db.relationship('Event', backref = 'category')
    users = db.relationship('User', secondary = favorite, backref = 'category')
    
    def __repr__(self):
        return '<Category %r>' % self.category_name

    def serialize(self):
        return {
            "categoryid": self.category_id,
            "categoryname": self.category_name,
            "users": list(map(lambda x: x.serialize(), self.users))
        }

class Event(db.Model):
    __tablename__="event"
    event_id = db.Column(db.Integer, primary_key = True, unique = True)
    event_name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(5000))
    start_time = db.Column(db.String(30))
    end_time = db.Column(db.String(30))
    city = db.Column(db.String(100))
    street = db.Column(db.String(100))
    lat = db.Column(db.Float)
    longi = db.Column(db.Float)
    ticket_url = db.Column(db.String(100))
    is_canceled = db.Column(db.String(100))
    event_category = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    attendances = db.relationship('Calendar', secondary = attendance, backref = 'event')

    def __repr__(self):
        return '<Event %r>' % self.event_id

    def serialize(self):
        return {
             "event_id": self.event_id,
             "event_name": self.event_name,
             "event_category": self.event_category,
             "description": self.description,
             "start_time": self.start_time,
             "end_time": self.end_time,
             "lat": self.lat,
             "longi": self.longi,
             "city": self.city,
             "street": self.street,
             "ticket_url": self.ticket_url,
             "is_canceled": self.is_canceled,
            }
