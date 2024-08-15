from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ecom_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)
CORS(app)  # Enable CORS

class SalesByCardType(db.Model):
    __tablename__ = 'charts_salesbycardtype'
    id = db.Column(db.Integer, primary_key=True)
    batch_no = db.Column(db.Integer, nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    total_sales = db.Column(db.Float, nullable=False)

class SalesByCountry(db.Model):
    __tablename__ = 'charts_salesbycountry'
    id = db.Column(db.Integer, primary_key=True)
    batch_no = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    total_sales = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/chart/filter-options/', methods=['GET'])
def get_filter_options():
    options = ['CardType', 'Country']
    return jsonify({'options': options})

@app.route('/chart/sales-by/<string:salesby>/', methods=['GET'])
def salesby_chart(salesby):
    labels = []
    sales_data = []

    try:
        if salesby == 'CardType':
            max_batch_no = db.session.query(db.func.max(SalesByCardType.batch_no)).scalar()
            queryset = SalesByCardType.query.filter_by(batch_no=max_batch_no).all()
            for sales in queryset:
                labels.append(sales.card_type)
                sales_data.append(sales.total_sales)

        elif salesby == 'Country':
            max_batch_no = db.session.query(db.func.max(SalesByCountry.batch_no)).scalar()
            queryset = SalesByCountry.query.filter_by(batch_no=max_batch_no).all()
            for sales in queryset:
                labels.append(sales.country)
                sales_data.append(sales.total_sales)

        return jsonify({
            'title': f'Sales by {salesby}',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Amount ($)',
                    'backgroundColor': generate_color_palette(len(labels)),
                    'borderColor': generate_color_palette(len(labels)),
                    'data': sales_data,
                }]
            },
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_color_palette(amount):
    colorPalette = ['#55efc4', '#81ecec', '#a29bfe', '#ffeaa7', '#fab1a0', '#ff7675', '#fd79a8']
    palette = []
    i = 0
    while len(palette) < amount:
        if i >= len(colorPalette):
            i = 0
        palette.append(colorPalette[i])
        i += 1
    return palette

@socketio.on('request_bar_chart_data')
def handle_bar_chart_data():
    try:
        max_batch_no = db.session.query(db.func.max(SalesByCardType.batch_no)).scalar()
        queryset = SalesByCardType.query.filter_by(batch_no=max_batch_no).all()

        labels = []
        sales_data = []

        for sales in queryset:
            labels.append(sales.card_type)
            sales_data.append(sales.total_sales)

        charts_data = {
            'labels': labels,
            'values': sales_data,
            'current_refresh_time': 'Current Refresh Time: {date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
        }

        socketio.emit('bar_chart_data', charts_data)
    except Exception as e:
        print(f"Error in handling bar chart data: {e}")

if __name__ == "__main__":
    socketio.run(app, debug=True)
