from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from models.ModelUser import ModelUser
from models.ModelAula1 import ModelAula1
from models.ModelAula2 import ModelAula2
from models.ModelAula3 import ModelAula3
from models.entities.User import User
from models.entities.Aula1 import Aula1
from models.entities.Aula2 import Aula2
from models.entities.Aula3 import Aula3
from datetime import datetime
from flask import jsonify

app = Flask(_name_)

app.config['SECRET_KEY'] = ''

db = MySQL(app)

app.config['MYSQL_HOST'] = "Angela2fp.mysql.pythonanywhere-services.com"
app.config['MYSQL_USER'] = "Angela2fp"
app.config['MYSQL_PASSWORD'] = "1234root"
app.config['MYSQL_DB'] = "Angela2fp$flask_login"


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                cursor = db.connection.cursor()
                cursor.execute('INSERT INTO user_accesos(username, fecha) VALUES (%s, %s)',
                               [request.form['username'], datetime.now()])
                db.connection.commit()
                return redirect(url_for('accesar'))
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/accesar', methods=['GET', 'POST'])
def accesar():
    if request.method == 'POST':
        aula1 = Aula1(0, 'aula1', request.form['password'])
        aula1_selected = ModelAula1.login(db, aula1)

        aula2 = Aula1(0, 'aula2', request.form['password'])
        aula2_selected = ModelAula2.login(db, aula2)

        aula3 = Aula1(0, 'aula3', request.form['password'])
        aula3_selected = ModelAula3.login(db, aula3)

        aula = request.form.get("aulas")
        if aula1_selected != None:
            if aula == "aula1":
                if aula1_selected.password:
                    flash("The door is unlocked...")
                    return jsonify(request.form['password'])
                    return redirect(url_for('accesar'))
                else:
                    flash("Invalid password...")
                    return render_template('accesar.html')
        else:
            flash("Aula not found...")
            return render_template('accesar.html')

        if aula2_selected != None:
            if aula == "aula2":
                if aula2_selected.password:
                    flash("The door is unlocked...")
                    return jsonify(request.form['password'])
                    return redirect(url_for('accesar'))
                else:
                    flash("Invalid password...")
                    return render_template('accesar.html')
        else:
            flash("Aula not found...")
            return render_template('accesar.html')

        if aula3_selected != None:
            if aula == "aula3":
                if aula3_selected.password:
                    flash("The door is unlocked...")
                    return jsonify(request.form['password'])
                    return redirect(url_for('accesar'))
                else:
                    flash("Invalid password...")
                    return render_template('accesar.html')
        else:
            flash("Aula not found...")
            return render_template('accesar.html')

    else:
        return render_template('accesar.html')


if _name_ == '_main_':
    app.run(port=8000, debug=True)