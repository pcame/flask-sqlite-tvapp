from flask import *
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import db

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'hseirjkgnwsllserpl'


# ------------------------------------GESTIÓN DE USUARIOS-----------------------------------
def checK_logged():
    if not 'logged' in session:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        try:
            user = db.get_user(usuario)
            if user['usuario'] == usuario and check_password_hash(user['password'], password):
                session['logged'] = True
                session['usuario'] = usuario
                if user['rol'] != 'admin':
                    session['admin'] = False
                else:
                    session['admin'] = True
            elif usuario == 'admin' and password == 'admin' and user['rol'] == 'admin':
                session['logged'] = True
                session['usuario'] = 'admin'
                session['admin'] = True
                return redirect('/changepass/admin')
        except:
            print('Usuario no registrado')
            return redirect(url_for('login'))
        return redirect(url_for('index'))


@app.route('/changepass/<usuario>', methods=['GET', 'POST'])
def change_password(usuario):
    if request.method == 'GET':
        return render_template('change_password.html')
    if request.method == 'POST':
        password = request.form['password']
        db.change_password(usuario, generate_password_hash(password))
        return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    if 'logged' in session:
        session.pop('logged')
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        edad = request.form['edad']
        email = request.form['email']
        rol = 'estandar'

        db.insert_user(usuario, generate_password_hash(password), nombre, apellido, telefono, edad, email, rol)
        return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'logged' in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['admin'] == False:
            session.pop('logged')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    usuari = db.get_user(usuario)
    return render_template('perfil.html', datos=usuari)


@app.route('/perfil/<usuario>/eliminar')
@login_required
def eliminar_perfil(usuario):
    db.eliminar_user(usuario)
    session.pop('logged')
    return redirect(url_for('login'))


# ------------------------------GESTIÓN DE USUARIOS POR EL ADMIN-----------------------

@app.route('/users/')
@admin_required
def users():
    users = db.get_users()
    return render_template('users.html', datos=users)


@app.route('/users/insert_user', methods=['GET', 'POST'])
@admin_required
def insert_user():
    if request.method == 'GET':
        return render_template('insert_user.html')

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        edad = request.form['edad']
        email = request.form['email']
        rol = request.form['rol']

        db.insert_user(usuario, generate_password_hash(password), nombre, apellido, telefono, edad, email, rol)
        return redirect(url_for('users'))


@app.route('/users/<usuario>/eliminar')
@admin_required
def eliminar_usuario(usuario):
    db.eliminar_user(usuario)
    if session['usuario'] == usuario:
        session.pop('logged')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('users'))


@app.route('/users/<usuario>/modificar', methods=['GET', 'POST'])
@admin_required
def modificar_usuario(usuario):
    if request.method == 'GET':
        usuarios = db.get_user(usuario)
        return render_template('modificar_usuario.html', user=usuarios)

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        edad = request.form['edad']
        email = request.form['email']
        rol = request.form['rol']

        db.modificar_usuario(usuario, generate_password_hash(password), nombre, apellido, telefono, edad, email, rol)
        return redirect(url_for('users'))


# -----------------------------------APLICACIÓN--------------------------------------
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/series/')
@login_required
def series():
    ser = db.get_series()
    seriesactores = db.get_seriesactores()
    return render_template('series.html', datos=ser, datos2=seriesactores)


@app.route('/series/<codser>')
@login_required
def serie(codser):
    ser = db.get_series(codser)
    seriesactores = db.get_seriesactores()
    return render_template('series.html', datos=ser, datos2=seriesactores)


@app.route('/actores/')
@login_required
def actores():
    act = db.get_actores()
    seriesactores = db.get_seriesactores()
    return render_template('actores.html', datos=act, datos2=seriesactores)


@app.route('/actores/<codac>')
@login_required
def actor(codac):
    act = db.get_actores(codac)
    seriesactores = db.get_seriesactores()
    return render_template('actores.html', datos=act, datos2=seriesactores)


@app.route('/series/insert_serie', methods=['GET', 'POST'])
@admin_required
def insert_serie():
    if request.method == 'GET':
        return render_template('insert_serie.html')

    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        canal_emision = request.form['canal_emision']
        emision = request.form['emision']
        inicio = request.form['inicio']
        fin = request.form['fin']
        puntuacion = request.form['puntuacion']

        db.insert_serie(nombre, genero, canal_emision, emision, inicio, fin, puntuacion)
        return redirect(url_for('series'))


@app.route('/actores/insert_actor', methods=['GET', 'POST'])
@admin_required
def insert_actor():
    if request.method == 'GET':
        return render_template('insert_actor.html')

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        ciudad_nacimiento = request.form['ciudad_nacimiento']
        pais_nacimiento = request.form['pais_nacimiento']
        img_url = request.form['img_url']
        img_tipo = request.form['img_tipo']
        img_tamaño = request.form['img_tamaño']

        db.insert_actor(nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo, img_tamaño)
        return redirect(url_for('actores'))


@app.route('/insert_serieactor', methods=['GET', 'POST'])
@admin_required
def insert_serieactor():
    if request.method == 'GET':
        series = db.get_series()
        actores = db.get_actores()
        return render_template('insert_serieactor.html', datos=series, datos2=actores)

    if request.method == 'POST':
        codser = request.form['codser']
        codac = request.form['codac']
        db.insert_serieactor(codser, codac)
        return redirect('/')


@app.route('/series/<codser>/eliminar')
@admin_required
def eliminar_serie(codser):
    db.eliminar_serie(codser)
    return redirect(url_for('series'))


@app.route('/actores/<codac>/eliminar')
@admin_required
def eliminar_actor(codac):
    db.eliminar_actor(codac)
    return redirect(url_for('actores'))


@app.route('/series/<codser>/modificar', methods=['GET', 'POST'])
@admin_required
def modificar_serie(codser):
    if request.method == 'GET':
        series = db.get_series(codser)
        return render_template('modificar_serie.html', serie=series[0])

    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        canal_emision = request.form['canal_emision']
        emision = request.form['emision']
        inicio = request.form['inicio']
        fin = request.form['fin']
        puntuacion = request.form['puntuacion']

        db.modificar_serie(codser, nombre, genero, canal_emision, emision, inicio, fin, puntuacion)
        return redirect(url_for('series'))


@app.route('/actores/<codac>/modificar', methods=['GET', 'POST'])
@admin_required
def modificar_actor(codac):
    if request.method == 'GET':
        actores = db.get_actores(codac)
        return render_template('modificar_actor.html', actor=actores[0])

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        ciudad_nacimiento = request.form['ciudad_nacimiento']
        pais_nacimiento = request.form['pais_nacimiento']
        img_url = request.form['img_url']
        img_tipo = request.form['img_tipo']
        img_tamaño = request.form['img_tamaño']

        db.modificar_actor(codac, nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo,
                           img_tamaño)
        return redirect(url_for('actores'))


@app.route('/eliminar_serieactor/<codser>/<codac>')
@admin_required
def eliminar_serieactor(codser, codac):
    db.eliminar_serieactor(codser, codac)
    return redirect('/')


# ----------------------------------API----------------------------------

@app.route('/api/series/', methods=["GET"])
@login_required
def api_get_series():
    series = db.get_series()
    data = {'data': series}
    return jsonify(data)


@app.route('/api/actores/', methods=["GET"])
@login_required
def api_get_actores():
    actores = db.get_actores()
    data = {'data': actores}
    return jsonify(data)


@app.route('/api/series/<codser>', methods=["GET"])
@login_required
def api_get_serie(codser):
    series = db.get_series(codser)
    data = {'data': series}
    return jsonify(data)


@app.route('/api/actores/<codac>', methods=["GET"])
@login_required
def api_get_actor(codac):
    actores = db.get_actores(codac)
    data = {'data': actores}
    return jsonify(data)


@app.route('/api/seriesactores/', methods=["GET"])
@login_required
def api_get_seriesactores():
    serieactor = db.get_seriesactores()
    data = {'data': serieactor}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
