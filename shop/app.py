from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("Магазин сюрпризов",
            template_folder="",
            static_folder="")

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///items.db"
database = SQLAlchemy(app)

class Item(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image = database.Column(database.String, nullable=False)
    name = database.Column(database.String, nullable=False)
    price = database.Column(database.String, nullable=False)

items = []
item1 = Item(image = 'https://steamuserimages-a.akamaihd.net/ugc/1843658378002555999/D2CB1C4A0B5A01521A8B19C8939A2694D7E3F105/?imw=512&amp;imh=341&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true',
name = "Icubovich",
price = "Сектор призп")

items.append(item1)

chosen = []

with app.app_context():
    database.create_all()
    existing_items = Item.query.all()
    if not(existing_items):
        for item in items:
            database.session.add(item)
            database.session.commit()



@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        chosen_name = request.form.get('chosen_name')
        chosen.append(chosen_name)
    items = Item.query.all()
    return render_template("index.html", items = items)

@app.route("/cart")
def cart():
    cart_list = chosen
    return render_template("/cart.html", cart_list = cart_list)

app.run()
