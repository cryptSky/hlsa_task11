from . import db

class User(db.Document):
    
    name = db.StringField(nullable=False) 
    email = db.StringField(nullable=False)
    birthdate = db.DateField(nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'birthdate': self.birthdate.strftime("%Y-%m-%d")
        }