from sqlalchemy import select

from database import db
from entities.user import User

db.base.metadata.create_all(db.engine)

# Ajouter un utilisateur
u = User(userid=1, username="test", useremail="test@test.com", password="qwerty")
session = db.session()
session.add(u)
session.commit()

# Lister les utilisateurs
print(select(User))
stmt = select(User)
session = db.session()

for row in session.scalars(stmt):
    print(row.username)