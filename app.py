from turtle import title
from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///credo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Credo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(800), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        title=request.form['title']
        credo=Credo(title=title, desc=desc)
        db.session.add(credo)
        db.session.commit()
        
    allcredo=Credo.query.all()
    return render_template('index.html', allcredo=allcredo)
#render_template display the template you want to show
#app route for navigation and slug for https://name

@app.route("/utsav")
def utsav():
    allcredo=Credo.query.all()
    print(allcredo)
    return "<p>Good Morning Utsav Bhai!</p>"

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        title=request.form['title']
        credo=Credo.query.filter_by(sno=sno).first()
        credo.title=title
        credo.desc=desc
        db.session.add(credo)
        db.session.commit()
        return redirect("/")
        
    credo=Credo.query.filter_by(sno=sno).first()
   
    return render_template('update.html', credo=credo)

@app.route("/delete/<int:sno>")
def delete(sno):
    credo=Credo.query.filter_by(sno=sno).first()
    db.session.delete(credo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)