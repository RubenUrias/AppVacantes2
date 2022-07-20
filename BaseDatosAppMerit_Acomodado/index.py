from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flaskcontacts'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


app.secret_key = "mysecretkey"

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			return render_template('msjpostulantes.html', msg = msg)
		else:
			msg = 'Correo electronico o contraseña incorrecta'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Esta cuenta ya existe'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Correo electronico invalido'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'El nombre de usuarios solo debe contener letras y numeros'
		elif not username or not password or not email:
			msg = 'Porfavor llena el formulario'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'has sido registrado exitosamente'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/In')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('adminvacantes.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        vacante = request.form['vacante']
        descripcion = request.form['descripcion']
        originario = request.form['originario']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (vacante, descripcion,originario) VALUES (%s,%s,%s)',
        (vacante,descripcion,originario))
        mysql.connection.commit()
        flash('Contacto Añadido Correctamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        vacante = request.form['vacante'] 
        descripcion = request.form['descripcion']
        originario = request.form['originario']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET vacante = %s,
                descripcion = %s,
                originario = %s
            WHERE id = %s
        """, (vacante,descripcion,originario, id)) 
        mysql.connection.commit()
        flash('Contacto Actualizado Correctamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Removido Correctamente')
    return redirect(url_for('Index'))

@app.route('/añadir/<id>', methods = ['POST', 'GET'])
def añadir_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    
    return render_template('añadir.html')


#centro mensajes

@app.route('/centromensajes')
def Index_2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM adminmensajes')
    data = cur.fetchall()
    cur.close()
    return render_template('centromensajes.html', adminmensajes = data)

@app.route('/add_centromensajes', methods=['POST'])
def add_adminmensajes():
    if request.method == 'POST':
        id = request.form['id']
        text = request.form['text']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO adminmensajes (id, text, phone, email) VALUES (%s,%s,%s,%s)', (id, text, phone, email, ))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index_2'))

@app.route('/editar/<id>', methods = ['POST', 'GET'])
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM adminmensajes WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact2.html', contact = data[0])

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        text = request.form['text']
        phone = request.form['phone']
        email = request.form['email']
        id = request.form['id']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE adminmensajes
            SET text = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (text,phone,email, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index_2'))

@app.route('/eliminar/<string:id>', methods = ['POST','GET'])
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM adminmensajes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index_2'))



    
#msj post




@app.route('/Index_4')
def Index_4():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM msjpost')
    data = cur.fetchall()
    cur.close()
    return render_template('msjpostulantes.html', msjpost = data)

@app.route('/add_msjpost', methods=['POST'])
def add_msjpost():
    if request.method == 'POST':
        vacante = request.form['vacante']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        originador = request.form['originador']
        mensaje = request.form['mensaje']
        postulantes = request.form['postulantes']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO msjpost (vacante, fecha, descripcion, originador, mensaje, postulantes) VALUES (%s,%s,%s,%s,%s,%s)', (vacante, fecha, descripcion, originador, mensaje, postulantes,))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index_4'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def edi(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM msjpost WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-3.html', msjpost = data[0])

@app.route('/act/<id>', methods=['POST'])
def act(id):
    if request.method == 'POST':
        vacante = request.form['vacante']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        originador = request.form['originador']
        mensaje = request.form['mensaje']
        postulantes = request.form['postulantes']
        id = request.form['id']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE msjpost
            SET vacante = %s,
                fecha = %s,
                descripcion = %s,
                originador = %s,
                mensaje = %s,
                postulante = %s
            WHERE id = %s
        """, (postulantes, fecha, descripcion, originador, mensaje, vacante, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index_4'))

@app.route('/eli/<string:id>', methods = ['POST','GET'])
def eli(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM msjpost WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index_4'))

@app.route('/aña/<id>', methods = ['POST', 'GET'])
def aña_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM msjpost WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    
    return render_template('aña.html')

    #actividades
@app.route('/Index_Actividad')
def Index_Actvidad_1():
    return render_template('index.html')
 
@app.route("/rubenlivesearch",methods=["POST","GET"])
def rubenlivesearch():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * from employee ORDER BY id"
            cur.execute(query)
            employee = cur.fetchall()
        else:    
            query = "SELECT * from employee WHERE empleado LIKE '%{}%' OR nombre LIKE '%{}%' OR id LIKE '%{}%' OR area LIKE '%{}%' OR vacante LIKE '%{}%' OR fecha LIKE '%{}%' ORDER BY id DESC LIMIT 20".format(search_word,search_word,search_word,search_word,search_word,search_word)
            cur.execute(query)
            numrows = int(cur.rowcount)
            employee = cur.fetchall()
            print(numrows)
    return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})

@app.route('/in')
def Index_Actvidad():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employee')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employee = data)

@app.route('/add_actividad', methods=['POST'])
def add_actividad():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        area = request.form['area']
        vacante = request.form['vacante']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO employee (nombre, area,vacante) VALUES (%s,%s,%s)',
        (nombre,area,vacante))
        mysql.connection.commit()
        return redirect(url_for('Index_Actvidad'))
    
@app.route('/añadir_actividad/<id>', methods = ['POST', 'GET'])
def añadir_actividad(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employee WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    
    return render_template('agregar_actividad.html')


























def login():
    return render_template('login.html')

@app.route('/msjpostulantes')
def msjpostulantes():
    return render_template('msjpostulantes.html')

@app.route('/adminvacantes')
def adminvacantes():
    return render_template('adminvacantes.html')

@app.route('/admincandidatos')
def admincandidatos():
    return render_template('admincandidatos.html')

@app.route('/centromensajes')
def centro():
    return render_template('centromensajes.html')



@app.route('/actividad')
def actividad():
    return render_template('actividad-nuevas.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True) 



