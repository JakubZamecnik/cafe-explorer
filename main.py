
from flask import Flask, render_template, request, app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime




app = Flask(__name__, instance_relative_config=True)  # instance složka relativní k projektu

# cesta k databázi ve složce instance
db_path = os.path.join(app.instance_path, 'cafes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.context_processor
def inject_now():
    return {"current_year": datetime.now().year}

class Cafe(db.Model):
    __tablename__ = 'cafe'  # přesný název tabulky v DB
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
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return render_template('cafes.html', cafes=cafes)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
        if request.method == 'POST':
            new_cafe = Cafe(
                name=request.form.get("name"),
                map_url=request.form.get("map_url"),
                img_url=request.form.get("img_url"),
                location=request.form.get("loc"),
                has_sockets=bool(request.form.get("sockets")),
                has_toilet=bool(request.form.get("toilet")),
                has_wifi=bool(request.form.get("wifi")),
                can_take_calls=bool(request.form.get("calls")),
                seats=request.form.get("seats"),
                coffee_price=request.form.get("coffee_price"),
            )
            db.session.add(new_cafe)
            db.session.commit()
            return render_template('index.html')
        return render_template('add_cafe.html')

if __name__ == "__main__":
    app.run(debug=True)
