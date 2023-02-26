from blog.models.database import db
from flask import Flask, render_template
from flask import request
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models import User
from blog.views.auth import login_manager, auth_app
# для работы авторизации нам обязательно нужен SECRET_KEY в конфигурации, добавляем


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix='/articles')
app.config["SECRET_KEY"] = "abcdefg123456"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """

    admin = User(username="admin", is_staff=True)
    james = User(username="james")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", admin, james)
