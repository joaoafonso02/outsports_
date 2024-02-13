from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UserData(db.EmbeddedDocument):
    sports = db.ListField(db.DictField())
    gallery = db.ListField(db.DictField())
    calendar = db.ListField(db.DictField())
    
class Note(db.Document):
    data = db.StringField()
    date = db.DateTimeField(default=datetime.utcnow)
    user = db.ReferenceField('User')

class User(db.Document, UserMixin):
    email = db.EmailField(unique=True)
    password = db.StringField()
    contact = db.StringField(max_length=150)
    country = db.StringField(max_length=150)
    name = db.StringField(max_length=150)
    notes = db.ListField(db.ReferenceField(Note))
    data = db.EmbeddedDocumentField(UserData, default=UserData)
    
    
    def set_password(self, password):
        # Set the hashed password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check if the provided password matches the hashed password
        return check_password_hash(self.password, password)

    meta = {
        'collection': 'Users'
    }
