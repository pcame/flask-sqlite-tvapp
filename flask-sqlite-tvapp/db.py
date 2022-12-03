import sqlite3


def get_series(codser=None):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'SELECT DISTINCT codser, nombre, genero, canal_emision, ' \
          'emision, inicio, fin, puntuacion FROM series'
    if codser is not None:
        sql += ' WHERE codser=' + codser

    cursor = conn.execute(sql)
    series = []
    for row in cursor:
        serie = {}
        serie['codser'] = row[0]
        serie['nombre'] = row[1]
        serie['genero'] = row[2]
        serie['canal_emision'] = row[3]
        serie['emision'] = row[4]
        serie['inicio'] = row[5]
        serie['fin'] = row[6]
        serie['puntuacion'] = row[7]
        series.append(serie)
    conn.close()
    return series


def get_actores(codac=None):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'SELECT DISTINCT codac, nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo, ' \
          'img_tamaño FROM actores'
    if codac is not None:
        sql += ' WHERE codac=' + codac
    cursor = conn.execute(sql)
    actores = []
    for row in cursor:
        actor = {}
        actor['codac'] = row[0]
        actor['nombre'] = row[1]
        actor['apellido'] = row[2]
        actor['edad'] = row[3]
        actor['ciudad_nacimiento'] = row[4]
        actor['pais_nacimiento'] = row[5]
        actor['img_url'] = row[6]
        actor['img_tipo'] = row[7]
        actor['img_tamaño'] = row[8]
        actores.append(actor)
    conn.close()
    return actores


def get_seriesactores(codser=None, codac=None):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'SELECT s.codser, s.nombre, a.codac, a.nombre, a.apellido FROM series s JOIN seriesactores sa ON ' \
          '(s.codser=sa.codser) JOIN actores a ON (sa.codac=a.codac)'
    cursor = conn.execute(sql)
    seriesactores = []
    for row in cursor:
        serieactor = {}
        serieactor['codser'] = row[0]
        serieactor['s_nombre'] = row[1]
        serieactor['codac'] = row[2]
        serieactor['a_nombre'] = row[3]
        serieactor['a_apellido'] = row[4]
        seriesactores.append(serieactor)
    conn.close()
    return seriesactores


def insert_serie(nombre, genero, canal_emision, emision, inicio, fin, puntuacion):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'INSERT INTO series(nombre, genero, canal_emision, emision, inicio, fin, puntuacion) VALUES ' \
          '(?,?,?,?,?,?,?)'
    values = [nombre, genero, canal_emision, emision, inicio, fin, puntuacion]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def insert_actor(nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo, img_tamaño):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'INSERT INTO actores (nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo,' \
          'img_tamaño) VALUES (?,?,?,?,?,?,?,?)'
    values = [nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo, img_tamaño]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def insert_serieactor(codser, codac):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'INSERT INTO seriesactores(codser, codac) VALUES(?, ?)'
    values = [codser, codac]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def eliminar_serie(codser):
    conn = sqlite3.connect('seriesactores.db')
    sql = ' DELETE FROM series WHERE codser =? '
    values = [codser]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def eliminar_actor(codac):
    conn = sqlite3.connect('seriesactores.db')
    sql = ' DELETE FROM actores WHERE codac =? '
    values = [codac]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def eliminar_serieactor(codser, codac):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'DELETE FROM seriesactores WHERE codser =? AND codac = ?'
    values = [codser, codac]
    conn.execute(sql, values)
    conn.commit()


def modificar_serie(codser, nombre, genero, canal_emision, emision, inicio, fin, puntuacion):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'UPDATE series SET nombre = ?, genero = ?, canal_emision = ?, emision = ?, ' \
          'inicio = ?, fin = ?, puntuacion = ? WHERE codser = ? '
    values = [nombre, genero, canal_emision, emision, inicio, fin, puntuacion, codser]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def modificar_actor(codac, nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo, img_tamaño):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'UPDATE actores SET nombre = ?, apellido = ?, edad = ?, ciudad_nacimiento = ?, pais_nacimiento = ?,' \
          'img_url = ?, img_tipo = ?, img_tamaño = ? WHERE codac = ?'
    values = [nombre, apellido, edad, ciudad_nacimiento, pais_nacimiento, img_url, img_tipo, img_tamaño, codac]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


# ------------------------GESTIÓN DE USUARIOS----------------------------
def get_user(usuario):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'SELECT DISTINCT usuario, password, nombre, apellido, telefono, edad, email, rol  ' \
          ' FROM users WHERE usuario = ?'
    values = [usuario]
    cursor = conn.execute(sql, values)
    for row in cursor:
        usuari = {}
        usuari['usuario'] = row[0]
        usuari['password'] = row[1]
        usuari['nombre'] = row[2]
        usuari['apellido'] = row[3]
        usuari['telefono'] = row[4]
        usuari['edad'] = row[5]
        usuari['email'] = row[6]
        usuari['rol'] = row[7]
    conn.close()
    return usuari


def insert_user(usuario, password, nombre, apellido, telefono, edad, email, rol):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'INSERT INTO users (usuario, password, nombre, apellido, telefono, edad, email, rol) VALUES (?,?,?,?,?,?,?,?)'
    values = [usuario, password, nombre, apellido, telefono, edad, email, rol]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def eliminar_user(usuario):
    conn = sqlite3.connect('seriesactores.db')
    sql = ' DELETE FROM users WHERE usuario =? '
    values = [usuario]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def change_password(usuario, password):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'UPDATE users SET password = ? WHERE usuario = ?'
    values = [password, usuario]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def get_users(usuario=None):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'SELECT DISTINCT usuario, password, nombre, apellido, telefono, edad, email, rol  ' \
          ' FROM users'
    if usuario is not None:
        sql += ' WHERE usuario=' + usuario

    cursor = conn.execute(sql)
    usuarios = []
    for row in cursor:
        usuario = {}
        usuario['usuario'] = row[0]
        usuario['password'] = row[1]
        usuario['nombre'] = row[2]
        usuario['apellido'] = row[3]
        usuario['telefono'] = row[4]
        usuario['edad'] = row[5]
        usuario['email'] = row[6]
        usuario['rol'] = row[7]
        usuarios.append(usuario)
    conn.close()
    return usuarios


def modificar_usuario(usuario, password, nombre, apellido, telefono, edad, email, rol):
    conn = sqlite3.connect('seriesactores.db')
    sql = 'UPDATE users SET usuario = ?, password = ?, nombre = ?, apellido = ?, telefono = ?,' \
          'edad = ?, email = ?, rol = ? WHERE usuario = ?'
    values = [usuario, password, nombre, apellido, telefono, edad, email, rol, usuario]
    conn.execute(sql, values)
    conn.commit()
    conn.close()
