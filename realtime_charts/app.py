from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/ecom_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SalesByCardType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_no = db.Column(db.Integer, nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    total_sales = db.Column(db.Float, nullable=False)

class SalesByCountry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_no = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    total_sales = db.Column(db.Float, nullable=False)

if __name__ == "__main__":
    db.create_all()
