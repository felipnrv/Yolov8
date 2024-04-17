#pip install -r requerimientos.txt

import cv2
from ultralytics import YOLO
from ultralytics.solutions import object_counter 
import supervision as sv
import os
import sqlite3 as sql 
import pyrebase
from flask import Flask,render_template,Response,request,redirect,url_for,session 
import datetime as dt

key=os.urandom(12)
app = Flask(__name__,template_folder='plantilla') #se inicializa la aplicacion
app.secret_key = 'key'

config = {
        "apiKey": "AIzaSyCC1C7eIcb6Q0-WeWKuzSrZNwVoSyVf8Lw",
        "authDomain": "dbfrutas-dd3ba.firebaseapp.com",
        "projectId": "dbfrutas-dd3ba",
        "databaseURL": "https://dbfrutas-dd3ba-default-rtdb.firebaseio.com/",
        "storageBucket": "dbfrutas-dd3ba.appspot.com",
        "messagingSenderId": "404825544625",
        "appId": "1:404825544625:web:efaa68356d01d1153ccf90",
        "measurementId": "G-EMQTJ61ZL6"
    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()


LINEA_INICIO = sv.Point(320, 0)
 #punto de inicio de la linea,la coordenada x es 320 y la coordenada y es 0
LINEA_FINAL = sv.Point(320, 480) #punto final de la line, la coordenada x es 320 y la coordenada y es 480

fruta1_aguact = 0 # aguacate
fruta2_marac = 1 # maracuya
fruta3_pitah = 2 # pitahaya
fruta4_tomate = 3# tomate de arbol

fecha_db = dt.datetime.now().strftime('%d-%m-%Y')
hora_db = dt.datetime.now().strftime('%H:%M')

class linea_conteo_class():
    def __init__(self,id_clase,linea_conteo):
        self.id_clase = id_clase #es el numero de la clase que se quiere contar
        self.linea_conteo = linea_conteo #es el contador de la linea

    def detections(self,result):
        deteccion = sv.Detections.from_yolov8(result) #se obtienen las detecciones
        deteccion = deteccion[deteccion.class_id == self.id_clase] #se filtran las detecciones de la clase que se quiere contar

        if result.boxes.id is not None:#se asigna el id del tracker a las detecciones
            deteccion.tracker_id = result.boxes.id.cpu().numpy().astype(int) 
            # se usa boxes.id.cpu().numpy() para obtener el id del tracker, es cpu porque se esta trabajando con un tensor de pytorch

        self.linea_conteo.trigger(detections=deteccion)#se cuentan las detecciones que cruzan la linea
        conteo_in = self.linea_conteo.in_count#in de derecha a izquierda
        conteo_out = self.linea_conteo.out_count#out de izquierda a derecha

        return conteo_in,conteo_out


def main():

    linea = sv.LineZone(start=LINEA_INICIO, end=LINEA_FINAL) #se crea el contador de la linea
    linea_1 = sv.LineZone(start=LINEA_INICIO, end=LINEA_FINAL)
    linea_2 = sv.LineZone(start=LINEA_INICIO, end=LINEA_FINAL)
    linea_3 = sv.LineZone(start=LINEA_INICIO, end=LINEA_FINAL)
    linea_4 = sv.LineZone(start=LINEA_INICIO, end=LINEA_FINAL)

    #LinezoneAnnotator es donde se esconde el contador de la linea
    linea_anotador = sv.LineZoneAnnotator(thickness=2, text_thickness=1, text_scale=0.5) #se crea el contador de la linea
    
    caja_anotador = sv.BoxAnnotator(thickness=2,text_thickness=1,text_scale=0.5) #se crea el objeto que permite anotar las cajas

    #se crea un objeto de la clase linea_conteo_class
    aguacate = linea_conteo_class(fruta1_aguact, linea_1) #linea_1 es el contador de la linea
    maracuya = linea_conteo_class(fruta2_marac, linea_2)
    pitahaya = linea_conteo_class(fruta3_pitah, linea_3)
    tomatearbol = linea_conteo_class(fruta4_tomate, linea_4)

    model = YOLO("./modelo_frutas.pt")

    cam_sources=[0,1]
    for source in cam_sources:
        for result in model.track(source=source, show=False, stream=True, agnostic_nms=True,conf=0.3):
            
            
            frame = result.orig_img

            detections = sv.Detections.from_yolov8(result)

            #detections = detections[detections.class_id != 10]
            detections1 = detections[detections.class_id == 0]
            detections2 = detections[detections.class_id == 1]
            detections3 = detections[detections.class_id == 2]
            detections4 = detections[detections.class_id == 3]
            
        
            if result.boxes.id is not None:#es para el conteo de las detecciones
                detections1.tracker_id = result.boxes.id.cpu().numpy().astype(int)

            if result.boxes.id is not None: #se asigna el id del tracker a las detecciones
                detections2.tracker_id = result.boxes.id.cpu().numpy().astype(int)
                
            if result.boxes.id is not None: 
                detections3.tracker_id = result.boxes.id.cpu().numpy().astype(int)
            
            if result.boxes.id is not None: 
                detections4.tracker_id = result.boxes.id.cpu().numpy().astype(int)
                        
            labels = [ #se crea una lista con las etiquetas de las detecciones
            f"# {class_id}{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id,tracker_id
            in detections #deteccions sirve para obtener las detecciones diferentes a 10
            ]
            
            frame = caja_anotador.annotate(scene=frame, detections=detections, labels=labels)

            linea_1.trigger(detections=detections1)
            linea_2.trigger(detections=detections2)
            linea_3.trigger(detections=detections3)
            linea_4.trigger(detections=detections4)
            linea_anotador.annotate(frame=frame, line_counter=linea)#line_counter es el contador de la linea, 
            #se usa linea y no linea_1 porque se quiere que el contador de la linea sea el mismo para todas las frutas
    
            maracuya_in,maracuya_out = maracuya.detections(result)
            aguacate_in,aguacate_out = aguacate.detections(result)
            pitahaya_in,pitahaya_out = pitahaya.detections(result)
            tomatearbol_in,tomatearbol_out = tomatearbol.detections(result)

            y_offset = 50  # Espacio vertical entre cada línea de texto

            aguacate_text = f"Aguacate: {aguacate_out}"
            cv2.putText(frame, aguacate_text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)#color negro en rgb es (0,0,0)
            y_offset += 30  # Incrementar el desplazamiento vertical

            maracuya_text = f"Maracuya: {maracuya_out}"
            cv2.putText(frame, maracuya_text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            y_offset += 30

            pitahaya_text = f"Pitahaya: {pitahaya_out}"
            cv2.putText(frame, pitahaya_text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            y_offset += 30

            tomatearbol_text = f"Tomate de arbol: {tomatearbol_out}"
            cv2.putText(frame, tomatearbol_text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)#blanco en rgb es (255,255,255)
            y_offset += 30

            #flecha = "<--------"
            #cv2.putText(frame, flecha, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)#blanco en rgb es (255,255,255)
            #y_offset += 30

            
            if aguacate_out != 0:
                print('Aguacate', aguacate_out)
            if maracuya_out != 0:
                print('Maracuya', maracuya_out)
            if pitahaya_out != 0:
                print('Pitahaya', pitahaya_out)
            if tomatearbol_out != 0:
                print('Tomatearbol', tomatearbol_out)

            db.child(fecha_db).child(hora_db).update(
                {"Aguacate": aguacate_out,
                "Maracuya": maracuya_out,
                "Pitahaya": pitahaya_out,
                "Tomatearbol": tomatearbol_out})

            base_datos_conteo(maracuya_out, pitahaya_out,aguacate_out,tomatearbol_out)
            try:
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    raise ValueError("La codificación de la imagen falló")  # Lanza un error específico

                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')
            except Exception as e:
                print("Error al procesar la imagen:", e)
                
            
  
def base_datos_conteo(maracuya_out, pitahaya_out,aguacate_out,tomatearbol_out):
 
        # Conecta con la base de datos o crea una nueva si no existe
        connection = sql.connect('frutascont.db')

        # Crea un cursor para ejecutar consultas SQL
        cursor = connection.cursor()

        # Crea la tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS conteo_frutas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            maracuya INTEGER DEFAULT 0,
                            pitahaya INTEGER DEFAULT 0,
                            aguacate INTEGER DEFAULT 0,
                            tomate_arbol INTEGER DEFAULT 0,
                            fecha_creacion DATE NOT NULL DEFAULT 0
                            
                        )''')
        
        fecha_creacion = dt.datetime.today().strftime('%Y-%m-%d')
        
        
        cursor.execute('SELECT * FROM conteo_frutas WHERE fecha_creacion=?', (fecha_creacion,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Si hay un registro con la misma fecha, actualiza los valores
            cursor.execute('''UPDATE conteo_frutas SET maracuya=?, pitahaya=?, aguacate=?, tomate_arbol=? WHERE fecha_creacion=?''',
                        (maracuya_out, pitahaya_out, aguacate_out, tomatearbol_out, fecha_creacion))
            
            
        else:
            # Si no hay un registro con la misma fecha, inserta uno nuevo
            cursor.execute('''INSERT INTO conteo_frutas (maracuya, pitahaya, aguacate, tomate_arbol, fecha_creacion) VALUES (?, ?, ?, ?, ?)''',
                        (maracuya_out, pitahaya_out, aguacate_out, tomatearbol_out, fecha_creacion))
        
            
        connection.commit()

        connection.close()

def registro_user():
    connection = sql.connect('usuarios.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            nombre TEXT NOT NULL
                        )''')
    connection.commit()
    connection.close()

def get_data():
    # Retrieve data from the specified location
    data_ref = db.child(fecha_db).child(hora_db).get()
    data = data_ref.val()

    # Prepare data for rendering
    table_data = []
    if data:
        for key, value in data.items():
            table_data.append({
                "campo1": key,
                "campo2": value["campo2"],
                "campo3": value["campo3"]
            })

    return table_data

@app.route('/')#se crea una ruta
def main_page():
    
    
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    registro_user()
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        connection = sql.connect('usuarios.db')
        cursor = connection.cursor()

        cursor.execute('''INSERT INTO usuarios (email, password,nombre) VALUES (?, ?, ?)''', (email, password,nombre))
        connection.commit()
        connection.close()
        return redirect(url_for('main_page'))

    # Renderizar la plantilla de registro
    return render_template('registro.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        connection = sql.connect('usuarios.db')
        cursor = connection.cursor()

        if not email or not password:
            error = "Por favor, ingrese su nombre de usuario y contraseña."
        cursor.execute('''SELECT * FROM usuarios WHERE email=? AND password=?''', (email, password))
        
        usuario = cursor.fetchone()

        if usuario:
                # Guardar el nombre de usuario en la sesión
                session['email'] = email
                return redirect(url_for('video'))
        else:
                error = "Usuario o contraseña incorrectos."
        
        connection.close()
        

    return render_template('login.html',error=error)



@app.route('/video' )
def video():
    fecha_seleccion=request.args.get('fecha',dt.date.today()) 

    connection = sql.connect('frutascont.db')
    cursor = connection.cursor()

    # Obtiene los registros de la tabla conteo_frutas
    cursor.execute('''SELECT * FROM conteo_frutas WHERE fecha_creacion = ?''', (fecha_seleccion,))
    registros = cursor.fetchall()

    # Cierra la conexión con la base de datos
    connection.close()

    return render_template('video.html',registros=registros,fecha=fecha_seleccion)

@app.route('/video_feed')
def video_feed():
    return Response(main(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/informe')
def informe():

    fecha_seleccion=request.args.get('fecha',dt.date.today()) 

    connection = sql.connect('frutascont.db')
    cursor = connection.cursor()

    # Obtiene los registros de la tabla conteo_frutas
    cursor.execute('''SELECT * FROM conteo_frutas WHERE fecha_creacion = ?''', (fecha_seleccion,))
    registros = cursor.fetchall()

    # Cierra la conexión con la base de datos
    connection.close()

    return render_template('informe.html',registros=registros,fecha=fecha_seleccion)


if __name__ == "__main__":
   
    app.run(debug=True)

