from faker import Faker
from app import app
from models import db,User

fake = Faker()
with app.app_context():

    User.query.delete()
    

    users = []
    for n in range(40):
        user = User(name = fake.name())
        users.append(user)
        db.session.add_all(users)
        db.session.commit()