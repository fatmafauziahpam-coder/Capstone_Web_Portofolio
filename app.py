from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Profile, Project, Contact

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ======================
# HOME
# ======================
@app.route("/")
def home():

    profile = Profile.query.first()
    projects = Project.query.all()

    return render_template(
        "index.html",
        profile=profile,
        projects=projects
    )


# ======================
# LOGIN
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(url_for("dashboard"))

        flash("Username atau Password salah!")

    return render_template("login.html")


# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
@login_required
def dashboard():

    projects = Project.query.all()

    return render_template(
        "dashboard.html",
        projects=projects
    )
@app.route("/project/add", methods=["GET", "POST"])
@login_required
def add_project():

    if request.method == "POST":

        project = Project(
            title=request.form["title"],
            description=request.form["description"],
            github=request.form["github"],
            demo=request.form["demo"],
            image=request.form["image"]
        )

        db.session.add(project)
        db.session.commit()

        flash("Project berhasil ditambahkan!")

        return redirect(url_for("dashboard"))

    return render_template("project_form.html")
# ======================
# EDIT PROJECT
# ======================
@app.route("/project/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):

    project = Project.query.get_or_404(id)

    if request.method == "POST":

        project.title = request.form["title"]
        project.description = request.form["description"]
        project.github = request.form["github"]
        project.demo = request.form["demo"]
        project.image = request.form["image"]

        db.session.commit()

        flash("Project berhasil diupdate!")

        return redirect(url_for("dashboard"))

    return render_template("project_form.html", project=project)


# ======================
# DELETE PROJECT
# ======================
@app.route("/project/delete/<int:id>")
@login_required
def delete_project(id):

    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    flash("Project berhasil dihapus!")

    return redirect(url_for("dashboard"))

# ======================
# EDIT PROFILE
# ======================
@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    profile = Profile.query.first()

    if profile is None:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    if request.method == "POST":

        profile.fullname = request.form["fullname"]
        profile.profession = request.form["profession"]
        profile.about = request.form["about"]
        profile.email = request.form["email"]
        profile.phone = request.form["phone"]
        profile.photo = request.form["photo"]

        db.session.commit()

        flash("Profile berhasil diperbarui!")

        return redirect(url_for("dashboard"))

    return render_template("profile_form.html", profile=profile)
# ======================
# MESSAGES
# ======================
@app.route("/messages")
@login_required
def messages():

    contacts = Contact.query.order_by(Contact.created_at.desc()).all()

    return render_template(
        "messages.html",
        contacts=contacts
    )

# ======================
# LOGOUT
# ======================
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))
# ======================
# CONTACT
# ======================
@app.route("/contact", methods=["POST"])
def contact():

    data = Contact(
        name=request.form["name"],
        email=request.form["email"],
        subject=request.form["subject"],
        message=request.form["message"]
    )

    db.session.add(data)
    db.session.commit()

    flash("Pesan berhasil dikirim!")

    return redirect(url_for("home"))

try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print("DATABASE ERROR:", e)
    raise

if __name__ == "__main__":
    app.run(debug=True)