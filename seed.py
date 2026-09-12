from config import app, db
from models import User, Task
from faker import Faker
import random

fake = Faker()

with app.app_context():
    print("Dropping existing tables...")
    db.drop_all()
    db.create_all()

    print("Generating mock users and paginated tasks...")
    users = []
    for _ in range(5):
        user = User(username=fake.user_name())
        user.password_hash = "password123"
        db.session.add(user)
        users.append(user)
    db.session.commit()

    for user in users:
        for _ in range(15):  # High count guarantees multi-page testing data
            task = Task(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=120),
                is_completed=random.choice([True, False]),
                user_id=user.id
            )
            db.session.add(task)
            
    db.session.commit()
    print("Database environment seeding complete!")
