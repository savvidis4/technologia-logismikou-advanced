from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_email(self, email):
        self.email = email
        db.session.commit()

    @classmethod
    def create_user(cls, email, password):
        
        new_user = cls(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user