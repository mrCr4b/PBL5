from flask import Flask, redirect, url_for, render_template, request, session
from sqlalchemy import Boolean, DateTime, Integer, LargeBinary, Date
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://db_pbl5_user:jwAJugGFHIgdEaoXXPKKEHcKOMl2qdSG@dpg-cooevlqcn0vc738nm790-a.singapore-postgres.render.com/db_pbl5'

db = SQLAlchemy(app)

class tai_khoan(db.Model):
    id_tai_khoan = db.Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_dang_nhap = db.Column(db.String(50), nullable=False)
    mat_khau = db.Column(db.String(50), nullable=False)
    phan_quyen = db.Column(Integer, nullable=False)
    khoa = db.Column(Integer, nullable=False)
    
class chi_tiet_tai_khoan(db.Model):
    id_tai_khoan = db.Column(Integer, primary_key=True, nullable=False)
    ho_ten = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    sdt = db.Column(db.String(50), nullable=False)
    gioi_tinh = db.Column(db.String(50), nullable=False)
    ngay_sinh = db.Column(Date, nullable=False)
    cccd = db.Column(db.String(50), nullable=False)
    thoi_gian_bat_dau = db.Column(Date, nullable=False)
    thoi_gian_ket_thuc = db.Column(Date, nullable=False)
    
class do_xe(db.Model):
    id_do_xe = db.Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_tai_khoan = db.Column(Integer, nullable=False)
    bien_so = db.Column(db.String(50), nullable=False)
    thoi_gian_vao = db.Column(DateTime, nullable=True)
    thoi_gian_ra = db.Column(DateTime, nullable=True)
    
class bien_so(db.Model):
    id_bien_so = db.Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_tai_khoan = db.Column(Integer, nullable=False)
    bien_so = db.Column(db.String(50), nullable=False)
    

@app.route("/", methods = ['POST', 'GET'])
@app.route("/login", methods = ['POST', 'GET'])
def home():
    if request.method == "POST":
        username = request.form['user']
        password = request.form['pass']
        
        # Query the database to check if the username and password match
        check_admin = tai_khoan.query.filter_by(ten_dang_nhap=username, mat_khau=password, phan_quyen=1).first()
        check_user = tai_khoan.query.filter_by(ten_dang_nhap=username, mat_khau=password, phan_quyen=0, khoa=0).first()
        if check_admin:
            session['user'] = username
            session['id'] = check_admin.id_tai_khoan
            return redirect(url_for('admin'))
        if check_user:
            session['user'] = username
            session['id'] = check_user.id_tai_khoan
            return redirect(url_for('user'))
    return render_template("login.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('id', None)
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    app.run(debug=True)