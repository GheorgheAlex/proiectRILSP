
print('Meniu: ')
print('1 - Cere date de lumina ambientala')
# print('2 - In dezvoltare')
print('0 - Incheiere conexiune')

commandList = [0, 1, 2]

while True:
    print("Comanda: ")
    serverCommand = input()
    print(serverCommand)

    if (serverCommand == '1'):
        print('11. Masuratoare instantanee')
        print('12. Masuratoara pentru un interval x de timp')

        print("Subcomanda: ")
        serverCommand = input()
        #client.send(str.encode(serverCommand))

        if(int(serverCommand) != [11, 12]):
            print("Comanda nu exista!")

        if (int(serverCommand) == 11):
            #response = client.recv(2048)
            print(str(1))
            #response = client.recv(2048)
            print(float(1))

        if (int(serverCommand) == 12):
            print('Cat timp: ')
            serverCommand = input()
            for _ in range(int(serverCommand)):

                print(float(1))
            print('Sarcina incheiata cu succes!')

    if (int(serverCommand) != commandList):
        print("Comanda nu este permisa!")

    if (serverCommand == '0'):
        break