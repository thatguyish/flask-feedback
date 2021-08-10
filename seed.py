from models import db,User,Feedback
from app import app

db.drop_all()
db.create_all()

user1 = User(
    username = "thatguy",
    password = "strongpass",
    email = "i.r@gmail.com",
    first_name = "ish",
    last_name = "ram"

)
user2 = User(
    username = "thatgirl",
    password = "strongpass",
    email = "e.g@gmail.com",
    first_name = "em",
    last_name = "g"
)

feedback1 = Feedback(
    title="Great",
    content="So like it was great",
    username="thatguy"
)

feedback2 = Feedback(
    title="Bad",
    content="So like it was bad",
    username="thatguy"
)
user1.register()
user2.register()

db.session.add_all([user1,user2])
db.session.add_all([feedback1,feedback2])
db.session.commit()