from flask_socketio import SocketIO, emit
from flask import Flask
from flask_cors import CORS,cross_origin
from random import random
from threading import Thread, Event
from time import sleep
from modbus_gateway import MODBUS_gateway
from models import DadosCLP
from db import Session,Base,engine

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")
CORS(app)
app.config['CORS_HEADERS'] = 'Content_type'
# Server functionality for receiving and storing data from elsewhere, not related to the websocket
#Data Generator Thread
thread = Thread()
thread_stop_event = Event()

tags = {'freq_des':{'addr':799 , 'type':'Holding','value':None},
                'freq_mot':{'addr':800 , 'type':'Holding','value':None},
                'tensao':{'addr':801 , 'type':'Holding','value':None},
                'estado_atuador':{'addr':801 , 'type':'Coil','value':None},#tag11
                'bt_OnOff':{'addr':802 , 'type':'Coil','value':None},#tag12
                'rotacao':{'addr':803 , 'type':'Holding','value':None},
                'pot_entrada':{'addr':804 , 'type':'Holding','value':None},
                'corrente':{'addr':805 , 'type':'Holding','value':None},
                'temp_estator':{'addr':806 , 'type':'Holding','value':None},
                'vel_esteira':{'addr':807 , 'type':'Holding','value':None},
                'carga':{'addr':808 , 'type':'Holding','value':None},
                'peso_obj':{'addr':809 , 'type':'Holding','value':None},
                't_part':{'addr':798 , 'type':'Holding','value':None}#tag13
        }

mg = MODBUS_gateway('localhost',502,1,tags)
#db_session=Session()
#Base.metadata.create_all(engine)


def Leitura_escrita_modbus():
    while not thread_stop_event.is_set():
        #executa a leitura dos dados modbus
        mg.data_read()
        #registradores lidos 
        number=mg._tags['freq_des']['value']
        number1=mg._tags['freq_mot']['value']
        number2=mg._tags['tensao']['value']
        number3=mg._tags['rotacao']['value']
        number4=mg._tags['pot_entrada']['value']
        number5=mg._tags['corrente']['value']
        number6=mg._tags['temp_estator']['value']
        number7=mg._tags['vel_esteira']['value']
        number8=mg._tags['carga']['value']
        number9=mg._tags['peso_obj']['value']
         #escrita no banco de dados
        #dado = DadosCLP(timestamp=mg.timestamp, Freq_desejada=number,Freq_medida=(number1/10),Tensao=number2,
                        # Rotacao=number3,Pot_entrada=(number4/10),Corrente=(number5/100),Temp_Estator=(number6/10),Vel_Esteira=(number7/100),Carga=(number8/100)) #tabela de escrita conforme models
       # db_session.add(dado)
        #db_session.commit()


        socketio.emit('newnumber',{'number':number,'number1':number1,'number2':number2,'number3':number3,'number4':number4,'number5':number5,'number6':number6,'number7':number7,'number8':number8,'number9':number9},namespace='/test')
        socketio.sleep(1)

class DataThread(Thread):
    def __init__(self):
        self.delay = 0.5
        super(DataThread, self).__init__()
    def dataGenerator(self):
        print("Initialising")
        try:
            while not thread_stop_event.isSet():
                mg.data_read()
        #registradores lidos 
                number=mg._tags['freq_des']['value']
                number1=mg._tags['freq_mot']['value']
                number2=mg._tags['tensao']['value']
                number3=mg._tags['rotacao']['value']
                number4=mg._tags['pot_entrada']['value']
                number5=mg._tags['corrente']['value']
                number6=mg._tags['temp_estator']['value']
                number7=mg._tags['vel_esteira']['value']
                number8=mg._tags['carga']['value']
                number9=mg._tags['peso_obj']['value']

                socketio.emit('responseMessage', {'freq_des': number,'freq_mot':number1,'tensao':number2,'rotacao':number3,'pot_entrada':number4,'corrente':number5,'temp_estator':number6,'vel_esteira':number7,'carga':number8,'peso_obj':number9})
                sleep(self.delay)
        except KeyboardInterrupt:
            # kill()
            print("Keyboard  Interrupt")
    def run(self):
        self.dataGenerator()
# Handle the webapp connecting to the 

@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit('responseMessage', {'data': 'Connected! ayy'})
    # need visibility of the global thread object
    global thread
    print("Starting Thread")
    thread = DataThread()
    thread.start()

# Handle the webapp connecting to the websocket, including namespace for testing
@socketio.on('connect', namespace='/devices')
def test_connect2():
    print('someone connected to websocket!')
    emit('responseMessage', {'data': 'Connected devices! ayy'})

# Handle the webapp sending a message to the websocket
@socketio.on('message')
def handle_message(message):
    # print('someone sent to the websocket', message)
    print('Data', message["data1"],message["data1"])
    print('Status', message["status"])
    global thread
    global thread_stop_event
    if (message["status"]=="Off"):
            thread_stop_event.set()
    elif (message["status"]=="On"):
            thread_stop_event.clear()
            print("Starting Thread")
            thread = DataThread()
            thread.start()
    else:
        print("Unknown command")


# Handle the webapp sending a message to the websocket, including namespace for testing
@socketio.on('message', namespace='/devices')
def handle_message2():
    print('someone sent to the websocket!')


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
    # socketio.run(app, debug=False, host='0.0.0.0')
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()