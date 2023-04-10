import subprocess
import shlex
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/home/tsubasa/Downloads/switch-app-8068b-firebase-adminsdk-xicam-03ce950b8a.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def on_switching(data):
    with open(data, 'r', encoding='UTF-8') as file:
        file_data = file.read()
        call_cmd = f"bto_advanced_USBIR_cmd -d {file_data}"
        args = shlex.split(call_cmd)
        ret = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(ret.returncode)
        print(ret.stdout.decode("utf-8"))
        print(ret.stderr.decode("utf-8"))

def temp_up():
    on_switching('remo_temp_up.txt')

def temp_down():
    on_switching('remo_temp_down.txt')

def mode_heating():
    on_switching('remo_mode_hot.txt')

def mode_cooling():
    on_switching('remo_mode_cool.txt')

def off_switching():
    on_switching('remo_air_off.txt')

def on_snapshot(doc_snapshot, changes, read_time):
    docs = doc_snapshot
    fetchTemp = None
    for doc in docs:
        fetchTemp = doc.to_dict()['temp']
        print(fetchTemp)

        switching = doc.to_dict().get("switching")
        temp = doc.to_dict().get("temp")
        mode = doc.to_dict().get("mode")
        print(temp)

        if switching:
            on_switching('remo_air_on.txt')
            if mode:
                mode_heating()
            else:
                mode_cooling()
        else:
            off_switching()

        if fetchTemp is not None:
            if fetchTemp < temp:
                temp_up()
                fetchTemp += 1
            elif fetchTemp > temp:
                temp_down()
                fetchTemp -= 1

doc_ref = db.collection('remoteSwitch')
doc_watch = doc_ref.on_snapshot(on_snapshot)
