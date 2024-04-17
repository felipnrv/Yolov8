import pyrebase 
import datetime as dt

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

fecha_db = dt.datetime.now().strftime('%d-%m-%Y')
hora_db = dt.datetime.now().strftime('%H:%M')

firebase = pyrebase.initialize_app(config)
db = firebase.database()

users=db.child(fecha_db).get()
print(users.val())