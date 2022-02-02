# PROIECT: Aplicatie de monitorizare a exploziilor
# REALIZAT DE: Alexandru-Marius GHEORGHE


import socket
import time

# Creare obiect socket ipv4 utilizand protocolul TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectare client
client.connect(('127.0.0.1', 1233))
response = client.recv(2048)

# Introducere USERNAME
name = input(response.decode())
client.send(str.encode(name))
response = client.recv(2048)

# Introducere PASSWORD
password = input(response.decode())
client.send(str.encode(password))

# Primire raspuns la logare
response = client.recv(2048)
response = response.decode()
print(str(response))

# Selectare mod de operare al clientului
if (response == 'Conexiune reusita!'):

    while True:

        print('')
        print('Meniu mod de masurare: ')
        print('1 - Cere date de lumina ambientala')
        print('2 - Masurare vibratii')
        print('3 - Masurare nivel gaz')
        print('0 - Incheiere conexiune')
        print('')


        print("Comanda: ")
        serverCommand = input()
        client.send(str.encode(serverCommand))


        # Masurare temperatura
        if (serverCommand == '1'):
            print('11. Masuratoare instantanee')
            print('12. Masuratoara pentru un interval x de timp')

            print("Subcomanda: ")
            serverCommand = input()
            client.send(str.encode(serverCommand))

            if (int(serverCommand) == 11):
                response = client.recv(2048)
                print(str(response)) 
                response = client.recv(2048)
                print(float(response))

            if (int(serverCommand) == 12):
                print('Cat timp: ')
                serverCommand = input()
                client.send(str.encode(serverCommand))
                for _ in range(int(serverCommand)):
                    response = client.recv(2048)
                    print("Nivel lumina: ")
                    print(float(response))
                    time.sleep(1)
                print('Sarcina incheiata cu succes!')


        # Masurare vibratie
        if (serverCommand == '2'):
            print('Cat timp: ')
            serverCommand = input()
            client.send(str.encode(serverCommand))
            for _ in range(int(serverCommand)):
                response = client.recv(2048)
                print("Vibratie: ")
                print(float(response))
                time.sleep(1)
            print('Sarcina incheiata cu succes!')

        # Masurare gaz
        if (serverCommand == '3'):
            print('Cat timp: ')
            serverCommand = input()
            client.send(str.encode(serverCommand))
            for _ in range(int(serverCommand)):
                response = client.recv(2048)
                print("Gaz: ")
                print(float(response))
                time.sleep(1)
            print('Sarcina incheiata cu succes!')


        ### MOD DE ALERTA ###
        if (serverCommand == '4'):
            print('Mod de alerta.')
            print('Cat timp sa fie activ modul de alerta (minute): ')
            serverCommand = input()
            client.send(str.encode(serverCommand))
            for _ in range(int(serverCommand)):
                response = client.recv(2048)
                response = response.decode()
                print(str(response))
            print('Sarcina incheiata cu succes!')

        if (serverCommand == '0'):
            break
else:
    client.close()

client.close()