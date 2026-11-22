from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import os, random
from dotenv import load_dotenv

current_path = os.path.dirname(__file__)
app = Flask(__name__, instance_path=os.path.join(current_path, 'instance'))

load_dotenv()
API_KEY = os.getenv("API_KEY")
app.config['SECRET_KEY'] = API_KEY

# Creating DB
class Base(DeclarativeBase):
    pass

# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url : Mapped[str] = mapped_column(String(500), nullable=False)
    img_url : Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet : Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi : Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets : Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls : Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price : Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for col in self.__table__.columns:
            dictionary[col.name] = getattr(self, col.name)
        return dictionary
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Execute once
# with app.app_context():
#     db.create_all()

@app.route("/")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    return render_template("index.html", all_cafes=cafes)

# HTTP GET - Read Record
@app.route("/random")
def get_coffe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    random_cafe = random.choice(result)
    return jsonify(your_cafe = random_cafe.to_dict())


if __name__ == "__main__":
    app.run(debug=True, port=5003)