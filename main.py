from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import choice
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random', methods=["GET"])
def random():
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    random_cafe = choice(cafe)
    # return jsonify(
    #     cafe={
    #         "name": random_cafe.name,
    #         "map_url": random_cafe.map_url,
    #         "img_url": random_cafe.img_url,
    #         "location": random_cafe.location,
    #
    #         "amenities": {
    #             "seats": random_cafe.seats,
    #             "has_toilet": random_cafe.has_toilet,
    #             "has_wifi": random_cafe.has_wifi,
    #             "has_sockets": random_cafe.has_sockets,
    #             "can_take_calls": random_cafe.can_take_calls,
    #             "coffee_price": random_cafe.coffee_price,
    #         }
    #     }
    # )
    return jsonify(cafe=to_dict(random_cafe))


@app.route('/all', methods=["GET"])
def all_cafe():
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return jsonify(cafes=[to_dict(i) for i in cafe])


@app.route('/search', methods=["GET"])
def find():
    location = request.args.get('loc')
    locations = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
    location_names = [i.location for i in locations]
    if location in location_names:
        return jsonify(cafe=[to_dict(cafe) for cafe in locations])
    else:
        return jsonify(
            {"error": "location not provided"}
        ), 400


# HTTP POST - Create Record
@app.route('/add', methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe"})


# HTTP PUT/PATCH - Update Record

@app.route('/update-price/<int:id>', methods=["PATCH", "GET"])
def update(id):
    new_price = request.args.get('new_price') or request.form.get('new_price')
    cafe = db.session.get(Cafe, id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Price Updated"})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 404


# HTTP DELETE - Delete Record
@app.route('/reported-closed/<int:id>', methods=["DELETE", "GET"])
def delete_cafe(id):
    api_key = request.args.get('api-key')
    cafe = db.session.get(Cafe, id)
    if not cafe:
        return jsonify(error={"Not Found": "Sorry cafe id not found"}), 404
    if api_key == "TopSecretAPIKey":
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"Success": "Record Deleted"})
    elif api_key != "TopSecretAPIKey":
        return jsonify(error={"Failed": "Unauthorized access"}), 400




if __name__ == '__main__':
    app.run(debug=True)
