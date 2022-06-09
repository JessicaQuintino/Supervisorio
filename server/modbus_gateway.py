
from datetime import datetime
from flask.json import tag
from pyModbusTCP.client import ModbusClient
from time import sleep
from threading import Thread,Lock

class MODBUS_gateway():
    """
    Classe Cliente MODBUS
    """
    def __init__(self,server_ip,porta,scan_time,tags):
        """
        Construtor
        tags = {'tag_1':{'addr':1000 , 'type':'Holding','value':None},
                'tag_2':{'addr':1001 , 'type':'Holding','value':None}
        }
        """
        self._cliente = ModbusClient(host=server_ip,port=porta)
        self._scan_time = scan_time
        self._tags=tags
        self._thread = Thread(target=self.data_read)
        self._lock = Lock()
        

    def data_read(self):
        self._cliente.open()
        self._lock.acquire()
        try:
            self.timestamp=datetime.now()
            for tagname,tag in self._tags.items():
                tag['value']= self.lerDado(tag['type'],tag['addr']) 
            sleep(self._scan_time)
        except Exception as e:
            print("Erro: ",e.args)
        self._lock.release()

    
    def data_write(self,addr,type,valor):
        self._lock.acquire()
        try:
            print(type,addr,valor)
            self.escreveDado(type,addr,valor)
        except Exception as e:
            print("Erro: ",e.args)
        self._lock.release()

             
    def run(self):
     self._thread.start()
                
        
    def lerDado(self,tipo,addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        """
        if tipo == 'Holding':
            return self._cliente.read_holding_registers(addr,1)[0]
        if tipo == 'Coil':
            return self._cliente.read_coils(addr,1)[0]
        if tipo == 'Input':
            return self._cliente.read_input_registers(addr,1)[0]
        if tipo == 'Discrete':
            return self._cliente.read_discrete_inputs(addr,1)[0] 

    def escreveDado(self,tipo,addr,valor):
        """
        Método para a escrita de dados na tabela MODBUS
        """
        if tipo == 'Holding':
            self._cliente.write_single_register(addr,valor)
        if tipo == 'Coil':
            self._cliente.write_single_coil(addr,valor)
