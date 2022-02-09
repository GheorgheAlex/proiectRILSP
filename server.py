# PROIECT: Sistem de monitorizarea a parametrilor unei hale industriale
# REALIZAT DE: Alexandru-Marius GHEORGHE


# Imports
import socket
import os
import threading
import hashlib
import time
import pyfirmata

# REALIZARE COMUNICATIE CU PLACA DE DEZVOLTARE ARDUINO
board = pyfirmata.Arduino('COM3') # Define the port of the Arduino Uno board
it = pyfirmata.util.Iterator(board)
it.start()

# CONFIGURARE PINI ARDUINO
# Format: a - port analogic; 0 - numarul portului; i - input
# CONEXIUNI:
#  -> Senzor lumina ambientala TEMT6000 - A0
#  -> Senzor piezoelectric de vibratii - A1
#  -> Senzor de gaze imflamabile - A2

temt6000_input = board.get_pin('a:0:i')
vibrationSensor_input = board.get_pin('a:1:i')
gasSensor_input = board.get_pin('a:2:i')

# FUNCTIE MASURARE LUMINA AMBIENTALA
def citireSenzorLuminaAmbientala():
    temt6000_value = temt6000_input.read()
    if (temt6000_value == None):
        return 0
    else:
        lightValue = temt6000_value * 1000
        return lightValue

# FUNCTIE MASURARE SENZOR DE VIBRATII
def citireSenzorVibratii():
    piezo_value = vibrationSensor_input.read()
    if (piezo_value == None):
        return 0
    else:
        return piezo_value

# FUNCTIE MASURARE DATE SENZOR DE GAZ MQ2
def citireSenzorGaze():
    mq2_value = gasSensor_input.read()
    if (mq2_value == None):
        return 0
    else:
        if(mq2_value < 0.18):
            return "Nu s-a detectat gaz"
        else:
            if(mq2_value >= 0.18):
                return "Gaz detectat!"

def citireSenzorGaze1():
    mq2_value = gasSensor_input.read()
    if (mq2_value == None):
        return 0
    else:
        return mq2_value

# CREARE CONEXIUNE TCP
ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Se asteapta conexiunea...')
ServerSocket.listen(5)
HashTable = {}

# FUNCTIONALITATE
def threaded_client(connection):
    connection.send(str.encode('Introduce USERNAME: '))  # Cere Username
    name = connection.recv(2048)
    connection.send(str.encode('Introduce PASSWORD: '))  # Cere Password
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    password = hashlib.sha256(str.encode(password)).hexdigest()  # Parola criptata folosind SHA256

    # FAZA DE INREGISTRARE
    # Daca USER-ul este nou, creaza cont
    if name not in HashTable:
        HashTable[name] = password
        connection.send(str.encode('Inregistrare efectuata cu succes!'))
        print('Inregistrat : ', name)
        print("{:<8} {:<20}".format('USER', 'PASSWORD'))
        for k, v in HashTable.items():
            label, num = k, v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")

    else:
        # Daca USER-ul este existent, verifica daca parola e corecta
        if (HashTable[name] == password):
            connection.send(str.encode('Conexiune reusita!'))  # Raspunsul pentru client
            print('Connected : ', name)

            # FUNCTIONALITATE
            while True:
                # Se asteapta comanda pentru a alege modul de functionare
                controlCommand = connection.recv(2048)
                print('controlCommand :', controlCommand)

                # CITIRE DATE LUMINA AMBIENTALA:
                if (int(controlCommand) == 1):
                    print('Cerere date : senzor TEMT6000')
                    print('Astept subcomanda...')
                    subCommand = connection.recv(2048)
                    print(subCommand)

                    # Functie de masurare a valorii instantanee de lumina ambientala
                    if (int(subCommand) == 11):
                        print('Cerere date instantanee: senzor TEMT6000')
                        lightData = citireSenzorLuminaAmbientala()
                        connection.send(str.encode('Valoare lumina ambientala: '))
                        connection.send(str.encode(str(lightData)))

                    # Functie de masurare a luminii ambientale pentru un anumit interval de timp stabilit de client
                    elif (int(subCommand) == 12):
                        measurementTime = connection.recv(2048)
                        print('Cerere masurare date senzor TEMT6000 timp de', int(measurementTime), 'secunde.')
                        for _ in range(int(measurementTime)):
                            lightData = citireSenzorLuminaAmbientala()
                            connection.send(str.encode(str(lightData)))
                            time.sleep(1)

                # CITIRE DATE SENZOR DE VIBRATIE:
                # Se trimit date pentru un interval de timp definit de client
                if (int(controlCommand) == 2):
                    print('Cerere date : senzor piezoelectric de vibratie')
                    measurementTime = connection.recv(2048)
                    print('Cerere masurare date senzor de vibratii timp de', int(measurementTime), 'secunde.')
                    for _ in range(int(measurementTime)):
                        vibrationData = citireSenzorVibratii()
                        connection.send(str.encode(str(vibrationData)))
                        time.sleep(1)

                # CITIRE DATE SENZOR DE GAZE:
                # Se trimit date pentru un interval de timp definit de client
                if (int(controlCommand) == 3):
                    print('Cerere date : senzor de gaz')
                    measurementTime = connection.recv(2048)
                    print('Cerere masurare date senzor de gaz timp de', int(measurementTime), 'secunde.')
                    for _ in range(int(measurementTime)):
                        gasData = citireSenzorGaze()
                        connection.send(str.encode(str(gasData)))
                        time.sleep(1)

                elif (int(controlCommand) == 0):
                    command0 = 'Conexiune incheiata'
                    print('Commanda :', command0)
                    connection.send(str.encode(command0))
                    break

        else:
            connection.send(str.encode('Login esuat'))  # Raspuns pentru login esuat
            print('Conexiune nepermisa : ', name)
    while True:
        break
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)
    )
    client_handler.start()
    ThreadCount += 1
    print('Cerere conexiune ' + str(ThreadCount))
    
ServerSocket.close()
