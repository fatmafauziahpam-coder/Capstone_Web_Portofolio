from app import app
from models import db, User

with app.app_context():

    if User.query.filter_by(username="admin").first():

        print("Admin sudah ada")

    else:

        admin = User(
            username="admin"
        )

        admin.set_password("admin123")

        db.session.add(admin)

        db.session.commit()

        print("Admin berhasil dibuat")