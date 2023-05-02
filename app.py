# server.py
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///court-database.sqlite3'
db = SQLAlchemy(app)

with app.app_context():
    db.Model.metadata.reflect(db.engine)

class Cases_en(db.Model):
    __tablename__ = 'data_en'
    __table_args__ = {'extend_existing': True }
    court_file_number = db.Column(db.Text, primary_key=True)   

@app.route("/")
def index():
    cases_count = Cases_en.query.count()

    courts = Cases_en.query.with_entities(Cases_en.court_en).distinct().all()
    courts = [court[0] for court in courts]
    return render_template("index.html", count=cases_count, courts=courts)



@app.route('/court/cases/<slug>')
def detail(slug):
    case = Cases_en.query.filter_by(slug=slug).first()
    return render_template("detail.html", case=case)



@app.route('/court/<url-slug>')
def court(court_name):
    court_meetings = Cases_en.query.filter_by(court_en=court_name).all()
    return render_template("court.html", courts=court_name, count=len(court_meetings), location=court_name, meetings=court_meetings)


if __name__ == '__main__':
    app.run(debug=True)