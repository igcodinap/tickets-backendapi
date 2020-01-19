from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite = db.Table(
    "favorite",
    db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.category_id")),
)


attendance = db.Table(
    "attendance",
    db.Column("calendar_id", db.Integer, db.ForeignKey("calendar.calendar_id")),
    db.Column("event_id", db.Integer, db.ForeignKey("event.event_id")),
)

fbattendance = db.Table(
    "fbattendance",
    db.Column("calendar_id", db.Integer, db.ForeignKey("fbcalendar.calendar_id")),
    db.Column("event_id", db.Integer, db.ForeignKey("event.event_id")),
)


fbfavorite = db.Table(
    "fbfavorite",
    db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("fbuser.user_id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.category_id")),
)


class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=False))
    is_valid = db.Column(db.Boolean)
    login_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __repr__(self):
        return "<Auth %r>" % self.token

    def serialize(self):
        return {
            "token": self.token
        }


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    birthday_date = db.Column(db.String(8))
    auths = db.relationship("Auth", backref="user")
    calendars = db.relationship("Calendar", backref="user")
    favs = db.relationship(
        "Category", secondary=favorite, back_populates="users", lazy=True
    )

    def __repr__(self):
        return "<User %r>" % self.name

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "birthday_date": self.birthday_date,
            "favs": list(map(lambda x: x.serialize(), self.favs)),
            "calendars": list(map(lambda x: x.serializeforuser(), self.calendars)),
        }



class Calendar(db.Model):
    __tablename__ = "calendar"
    calendar_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    calendar_id_owner = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    events_assistance = db.relationship(
        "Event", secondary=attendance, back_populates="in_calendar", lazy=True
    )

    def __repr__(self):
        return "<Calendar %r>" % self.name

    def serialize(self):
        return {
            "calendar_id": self.calendar_id,
            "name_calendar": self.name,
            "description": self.description,
            "calendar_id_owner": self.calendar_id_owner,
            "events_assistance": list(
                map(lambda x: x.serialize(), self.events_assistance)
            ),
        }

    def serializeforuser(self):
        return {"calendar_id": self.calendar_id, "name_calendar": self.name}


class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    events = db.relationship("Event", backref="category")
    users = db.relationship(
        "User", secondary=favorite, back_populates="favs", lazy=True
    )
    fbusers = db.relationship(
        "fbUser", secondary=fbfavorite, back_populates="favs", lazy=True
    )

    def __repr__(self):
        return "<Category %r>" % self.category_name

    def serialize(self):
        return {
            "categoryid": self.category_id,
            "categoryname": self.category_name,
        }


class Event(db.Model):
    __tablename__ = "event"
    event_id = db.Column(db.Integer, primary_key=True, unique=True)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000))
    start_time = db.Column(db.String(50))
    end_time = db.Column(db.String(50))
    city = db.Column(db.String(100))
    street = db.Column(db.String(100))
    lat = db.Column(db.Float)
    longi = db.Column(db.Float)
    is_canceled = db.Column(db.String(100))
    event_category = db.Column(db.String, db.ForeignKey("category.category_name"))
    event_photo_url = db.Column(db.String(200))
    in_calendar = db.relationship(
        "Calendar", secondary=attendance, back_populates="events_assistance", lazy=True
    )
    in_fbcalendar = db.relationship(
        "fbCalendar", secondary=fbattendance, back_populates="events_assistance", lazy=True
    )

    def __repr__(self):
        return "<Event %r>" % self.event_id

    def serialize(self):
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "event_category": self.event_category,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "lat": str(self.lat)[:10],
            "longi": str(self.longi)[:10],
            "city": self.city,
            "street": self.street,
            "is_canceled": self.is_canceled,
            "event_photo_url": self.event_photo_url
        }


class fbUser(db.Model):
    __tablename__ = "fbuser"
    table_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(80))
    calendars = db.relationship("fbCalendar", backref="fbuser")
    favs = db.relationship(
        "Category", secondary=fbfavorite, back_populates="fbusers", lazy=True
    )

    def __repr__(self):
        return "<fbUser %r>" % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
        }


class fbCalendar(db.Model):
    __tablename__ = "fbcalendar"
    calendar_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    calendar_id_owner = db.Column(db.Integer, db.ForeignKey("fbuser.user_id"))
    events_assistance = db.relationship(
        "Event", secondary=fbattendance, back_populates="in_fbcalendar", lazy=True
    )

    def __repr__(self):
        return "<fbCalendar %r>" % self.name

    def serialize(self):
        return {
            "calendar_id": self.calendar_id,
            "name_calendar": self.name,
            "description": self.description,
            "calendar_id_owner": self.calendar_id_owner,
            "events_assistance": list(
                map(lambda x: x.serialize(), self.events_assistance)
            ),
        }

    def serializeforuser(self):
        return {"calendar_id": self.calendar_id, "name_calendar": self.name}