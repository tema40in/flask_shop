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
price = "211212121")
item2 = Item(image = "https://aif-s3.aif.ru/images/011/924/89c157b7714dc366ad1bcaf0925ffdd6.jpg",
             name = "ivan",
             price = "23000000")

items.append(item1)
items.append(item2)

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
        chosen_price = request.form.get('chosen_price')
        chosen_image = request.form.get('chosen_image')
        chosen.append([chosen_name, chosen_price, chosen_image])
    items = Item.query.all()
    return render_template("index.html", items = items)

@app.route("/cart", methods=["GET","POST"])
def cart():
    cart_list = chosen
    prices = []
    if request.method == 'POST':
        cart_list.clear()
    for i in cart_list:
        prices.append(int(i[1]))
    total = sum(prices)
    return render_template("/cart.html", cart_list = cart_list, total = total)

app.run()

