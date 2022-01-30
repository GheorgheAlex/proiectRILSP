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
    print('Mod de operare: ')
    print('8 - Mod de alerta ')
    print('9 - Mod de masurare ')

serverCommand = input()
client.send(str.encode(serverCommand))

# MOD DE ALERTA

if (serverCommand == '0'):
    print('Mod de alerta.')
    print('Apasa 0 si Enter pentru a opri clientul')

    while True:
        serverCommand = input()
        client.send(str.encode(serverCommand))

        response = client.recv(2048)
        response = response.decode()
        print(str(response))


        if(serverCommand == '0'):
            break




# MOD DE MASURARE
if (serverCommand == '9'):
    print('Meniu mod de masurare: ')
    print('1 - Cere date de lumina ambientala')
    print('2 - Masurare vibratii')
    print('3 - Masurare nivel gaz')
    print('0 - Incheiere conexiune')



    while True:
        commandList = [0, 1, 2, 3]

        print("Comanda: ")
        serverCommand = input()
        client.send(str.encode(serverCommand))

        if (int(serverCommand) != commandList):
            print("Comanda nu este permisa!")

        # TODO: Sa creez doua moduri de lucru: unul de monitorizare, si unul de alerta

        # Masurare temperatura
        if (serverCommand == '1'):
            print('11. Masuratoare instantanee')
            print('12. Masuratoara pentru un interval x de timp')

            print("Subcomanda: ")
            serverCommand = input()
            client.send(str.encode(serverCommand))

            # if(int(serverCommand) != [11, 12]):
            #     print("Comanda nu exista!")

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
                # TODO: de vazut cum se realizeaza masuratorile
                # TODO: Cum as putea sa imi fac un sistem de alerta la vibratie?
                print(float(response))
                time.sleep(1)
            print('Sarcina incheiata cu succes!')

        # Masurare gaz
        if (serverCommand == '2'):
            print('Cat timp: ')
            serverCommand = input()
            client.send(str.encode(serverCommand))
            for _ in range(int(serverCommand)):
                response = client.recv(2048)
                print("Gaz: ")
                # TODO: sa fac un sistem de alerta care zice daca este gaz prezent sau nu. Pentru asta ar trebui sa verific pragurile de tensiune si apoi sa fac alertele
                print(float(response))
                time.sleep(1)
            print('Sarcina incheiata cu succes!')
        if (serverCommand == '0'):
            break
else:
    client.close()

client.close()