from flask import Flask,render_template,request,session,redirect,flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import json
from Email import send_email
from random import randint
app= Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testDB'
db = SQLAlchemy(app)
class worker(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String(50), nullable= False)
    player1 = db.Column(db.String(100), nullable= False)
    player2 = db.Column(db.String(100), nullable= False)
    player1_score = db.Column(db.String(100),)
    player2_score = db.Column(db.String(100),)
    def __repr__(self):
        return f"worker('{self.id}','{self.name}','{self.email}','{self.password}','{self.player1}','{self.player2}','{self.player1_score}','{self.player2_score}')"

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST' :
        if request.form.get('email') and request.form.get('password'):
            session['email']=request.form.get('email')
            session['password']=request.form.get('password')
            print(db.session.query(worker))
            data =worker.query.filter_by(email=session['email']).first()
            print(data)
            if  data :
                if not data.email==session['email']:
                    flash("This user doesn't have an account",'nv1')
                    return redirect(url_for('index'))
                if not data.password==session['password']:
                    flash("Incorrect password",'inv2')
                    return redirect(url_for('index'))
                session['data'] = {'score1': data.player1_score, 'score2': data.player2_score,'player1':data.player1,'player2':data.player2}
                flash('You have been logged-in secssefuly')
                return redirect(url_for('game'))
            else :
                flash("This user doesn't have an account",'inv3')
                return redirect(url_for('index'))
    return render_template("login.html")
@app.route('/singup', methods=['GET','POST'])
def singup():
    nv=False
    if request.method == 'POST':
        session['name']=request.form.get('name')
        session['email']=request.form.get('email')
        session['password']=request.form.get('password')
        session['confirm_password']=request.form.get('confirm_password')
        print(session['name'])
        if len(session['name'])<4:
            flash("username too short at least 4 letters",'inv1')
        elif checkuser(session['name']):
            flash("invalid username",'inv1')
            print('')
            nv=True
        if '@' not in session['email'] or checkemail(session['email']) or len(session['email'])<4:
            flash("invalid email",'inv2')
            nv=True
        if len(session['password'])<=8:
            flash("Password too short",'inv3')
            nv=True
        elif session['password']!=session['confirm_password']:
            flash("incorrect confimrming password",'inv3')            
        if nv:
            session.pop('name', None)
            session.pop('email', None)
            session.pop('password', None)
            session.pop('confirm_password', None)
            return redirect(url_for('singup'))
        else:
            return redirect(url_for('players'))
    if session.get('confirm_password'):
            session.pop('confirm_password')        
    return render_template("singup.html")
def checkuser(a):
    data =worker.query.filter_by(name=a).first()
    if data:
        return True
    return False
def checkemail(a):
    data =worker.query.filter_by(email=a).first()
    if data:
        return True
    return False
@app.route('/email', methods=['GET','POST'])
def email():
    if request.method == 'POST' :
        if request.form.get('email_'):
            session['email_']=request.form.get('email_')
            data =worker.query.filter_by(email=request.form.get('email_')).first()
            print(data)
            if data :
                session['validation_message']=str(randint(100000,999999))
                send_email(session['email_'],session['validation_message'])
                return redirect(url_for("verification"))
            else :
                session.pop('email_',None)
                session.pop('validation_message',None)
                return render_template('email.html',error=True)
        else:
            return redirect(url_for('index'))
    if session.get('email_'):
        session.pop('validation_message', None)
        session['validation_message']=str(randint(100000,999999))
        send_email(session['email_'],session['validation_message'])
        return redirect(url_for("verification"))
    return render_template('email.html')
@app.route('/verification/email', methods=['GET','POST'])
def verification():
    if request.method == 'POST' :
        session['valid']=request.form.get('passvalid')
        if session.get('validation_message')==request.form.get('passvalid'):
            print("what the heck")
            session.pop('validation_message', None)
            session.pop('valid', None)
            return redirect(url_for('reset'))
        else:
            session.pop('valid', None)
            flash("Incorrect Try Again")
            return redirect(url_for('verification'))
    return render_template('verifyemail.html')
@app.route('/reset', methods=['GET','POST'])
def reset():
    if request.method == 'POST' :
        if request.form.get('new_password'):
            session['new_password']=request.form.get('new_password')
            if len(session.get('new_password'))<8:
                flash("Password must be at least 8 caracters long")
                session.pop('new_password',None)
                return redirect(url_for('reset'))
            data =worker.query.filter_by(email=session['email_']).first()
            if data:
                if session.get('new_password')==data.email:
                    flash("Your new password can not be your old password")
                    session.pop('new_password',None)
                    return redirect(url_for('reset'))
                if data.email:
                    data.password=session['new_password']
                    session.pop('new_password', None)
                    session.pop('email_',None)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('reset_new.html')
@app.route('/logout')
def logout():
    for key in list(session.keys()):
     session.pop(key)
     print(worker)
    return redirect(url_for('index'))

@app.route('/<user_score>',methods=['POST'])
def indexout(user_score):
    if request.method == 'POST' :
            user_scores = json.loads(user_score)
            if 'data' in session:
                data =worker.query.filter_by(email=session['email'])
                if data:
                    data.player1_score=user_scores['player2']
                    data.player2_score=user_scores['player1']
                else:
                    return redirect(url_for('index'))
            elif 'name' in session:
                user1=worker(name=session['name'],email=session['email'],password=session['password'],\
                        player1=session['player1'],player2=session['player2'],\
                        player1_score=user_scores['player1'],player2_score=user_scores['player2'])
                db.session.add(user1)
            db.session.commit()
    return 'hello'
@app.route('/players', methods=['GET','POST'])
def players():
    if session.get('confirm_password'):
        session.pop('confirm_password',None)
    if 'name' in session and 'email' in session and 'password' in session:
        if request.method == 'POST':
            session['player1']=request.form.get('player1')
            session['player2']=request.form.get('player2')
            return redirect(url_for('game')) 
        else:
            return render_template('players.html')     
    else:
        return redirect(url_for('singup'))
    

@app.route('/Game')
def game():
    if 'player1' in session and 'player2' in session:
        user1= {'score1': 0, 'score2': 0,'player1':session['player1'],'player2':session['player2']}
        return render_template('retro.html',user=user1)
    elif 'email' in session and 'password' in session:
        user1= session['data']
        return render_template('retro.html',user=user1)
    else:
        return redirect(url_for('index'))
if (__name__=="__main__"):
    app.run(debug=True,port=5100)
    

    
    