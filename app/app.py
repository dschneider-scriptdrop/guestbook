import logging
import os

from flask import Flask, render_template, request
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('DB_ENV_MYSQL_USER'),
        password=os.getenv('DB_ENV_MYSQL_PASSWORD'),
        hostname=os.getenv('DB_PORT_3306_TCP_ADDR'),
        database=os.getenv('DB_ENV_MYSQL_DATABASE'))


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome to Docker Guestbook")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.debug("index")

    if request.method == 'POST':
        name = request.form['name']
        guest = Guest(name=name)
        db.session.add(guest)
        db.session.commit()

    return render_template('index.html', guests=list_guests())


class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return self.name

@manager.command
def list_guests():
    return Guest.query.all()

@manager.command
def create_test_data():
    guest = Guest(name='Steve')
    db.session.add(guest)
    db.session.commit()

@manager.command
def create_db():
    logger.debug("create_db")
    logger.debug(SQLALCHEMY_DATABASE_URI)
    db.create_all()


if __name__ == '__main__':
    manager.run()
