from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)


app.secret_key = "mysecretkey"

@app.route('/')
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
def update_contact(id):
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


#inicia parte Gabriel
#te odio gabriel por tu culpa me desvele >:(

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

#actividades

@app.route('/actividades')
def Index_A():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM actividad')
    data = cur.fetchall()
    cur.close()
    return render_template('actividades.html', actividad = data)

@app.route('/add_actividad', methods=['POST'])
def add_actividad():
    if request.method == 'POST':
        nombre = request.form['nombre']
        area = request.form['area']
        vacante = request.form['vacante']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO actividad (nombre, area,vacante) VALUES (%s,%s,%s)',
        (nombre,area,vacante))
        mysql.connection.commit()
        return redirect(url_for('Index_A'))

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

@app.route('/actividades')
def actividades():
    return render_template('actividades.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True) 



