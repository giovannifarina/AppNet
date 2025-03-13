import subprocess
import re
import socket
import threading

# Recupero indirizzo IP configurato sull'interfaccia di rete

def get_ip_address(interface):
    """Get IP address for a given network interface"""
    command = f"ip addr show {interface}"
    output = subprocess.check_output(command, shell=True).decode()
    ip_pattern = r'inet\s+(\d+\.\d+\.\d+\.\d+)'
    match = re.search(ip_pattern, output)
    if match:
        ip_address = match.group(1)
        return ip_address
    else:
        return None

interface_name = "eth0"
ip_address = get_ip_address(interface_name)

# Codice per aprire una socket UDP ed aspettare messaggi
def server_udp() :
    # Codice ascolto su porta UDP

    UDP_IP = "0.0.0.0" # Qualsiasi IP configurato sulla macchina
    UDP_PORT = 5000

    sock = socket.socket(socket.AF_INET,    # Crea una socket UDP
                        socket.SOCK_DGRAM) 

    sock.bind((UDP_IP, UDP_PORT)) # Associa la socket all'indirizzo e alla porta specificati

    print(f"In attesa di messaggi UDP su {UDP_IP}:{UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)  # Rimani in attesa di dati sulla socket
        message = data.decode()
        client_ip = addr[0]  # Estrai l'IP del client
        client_port = addr[1]  # Estrai la porta del client
        print(f"Ricevuto il messaggio: {message} da {client_ip}:{client_port}")

# Codice per contattare una socket UDP
def client_udp() :
    # Codice invio messaggi UDP
    print("Quale pc vuoi contattare?")
    print("1. PC1")
    print("2. PC2")
    print("3. PC3")
    #print("3. Option C: Learn a new skill")
    pc = 0
    while True:
        try:
            pc = int(input("Digita un numero per selezionare l'opzione richiesta (1-3): "))
            if 1 <= pc <= 3:
                break
            else:
                print("Valore non valido")
        except ValueError:
            print("Valore non valido")

    match pc:
        case 1:
            dest_IP = "192.168.1.1"
        case 2:
            dest_IP = "192.168.1.2"
        case 3:
            dest_IP = "192.168.1.3"

    #dest_IP = "0.0.0.0"  # Indirizzo IP del destinatario
    dest_port = 5000        # Porta del destinatario

    sock = socket.socket(socket.AF_INET,  # Internet
                        socket.SOCK_DGRAM)  # UDP

    while True:
        message = input("Inserisci il messaggio da inviare (o 'exit' per uscire): ")

        if message.lower() == "exit":
            break

        sock.sendto(message.encode(), (dest_IP, dest_port)) # Invia il messaggio codificato

        print(f"Messaggio '{message}' inviato a {dest_IP}:{dest_port}")

    print("Programma terminato.")

# Codice per contattare una socket TCP
def client_tcp():
    print("Quale pc vuoi contattare?")
    print("1. PC1")
    print("2. PC2")
    print("3. PC3")
    #print("3. Option C: Learn a new skill")
    pc = 0
    while True:
        try:
            pc = int(input("Digita un numero per selezionare l'opzione richiesta (1-3): "))
            if 1 <= pc <= 3:
                break
            else:
                print("Valore non valido")
        except ValueError:
            print("Valore non valido")

    match pc:
        case 1:
            dest_IP = "192.168.1.1"
        case 2:
            dest_IP = "192.168.1.2"
        case 3:
            dest_IP = "192.168.1.3"

    """Crea un client TCP che si connette a un server e scambia messaggi."""
    SERVER_PORT = 12345  # Porta del server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((dest_IP, SERVER_PORT))
        print(f"Connesso a {dest_IP}:{SERVER_PORT}")

        while True:
            message = input("Inserisci il messaggio da inviare: ")
            client_socket.sendall(message.encode())

            data = client_socket.recv(1024)
            print(f"Ricevuto: {data.decode()}")
    except ConnectionRefusedError:
        print("Connessione rifiutata. Assicurati che il server sia in esecuzione.")
    finally:
        client_socket.close()

# Funzione per gestire la comunicazione con un singolo client
def handle_client(connection_socket, client_address):
    """Handles communication with a single client."""
    try:
        print(f"Connessione da {client_address}")

        while True:
            data = connection_socket.recv(1024)  # Ricevi fino a 1024 byte sulla socket
            if data:
                message = data.decode()
                print(f"Ricevuto da {client_address}: {message}")

                response = input(f"Inserisci la risposta per {client_address}: ")
                connection_socket.sendall(response.encode())
            else:
                print(f"Client {client_address} disconnesso")
                break

    finally:
        connection_socket.close()

# Codice per aprire una socket TCP ed aspettare connessioni
def server_tcp():

    """Crea un server TCP che ascolta per connessioni multiple e gestisce ogni client in un thread."""
    SERVER_ADDRESS = "0.0.0.0"  
    SERVER_PORT = 12345  # Porta su cui ascoltare

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Chiedo al sistema operati di creare una socket TCP
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT)) # Associa la socket all'indirizzo e alla porta specificati
    server_socket.listen(5)  # Numero massimo di connessioni in coda

    print(f"Server in ascolto su {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        connection_socket, client_address = server_socket.accept() # Accetta la connessione
        # Avvia un nuovo thread per gestire il client
        client_thread = threading.Thread(target=handle_client, args=(connection_socket, client_address)) # Quando un client si connette, avvia un nuovo thread che gestisce la connessione su una socket dedicata
        client_thread.daemon = True  # Termina il thread quando il main thread termina
        client_thread.start()


# Richiesta tipo di comportamento all'utente

print("1. Apri Socket UDP sulla porta 5000 ed aspetta messaggi")
print("2. Apri una UDP socket per inviare messaggi ad altri processi")
print("3. Apri socket TCP per aspettare connessioni sulla porta 12345")
print("4. Apri socket TCP per comunicare con un server sulla porta 12345")
choice = 0
while True:
    try:
        choice = int(input("Digita un numero per selezionare l'opzione richiesta (1-4): "))
        if 1 <= choice <= 4:
            break
        else:
            print("Valore non valido")
    except ValueError:
        print("Valore non valido")

match choice:
    case 1:
        server_udp()
    case 2:
        client_udp()
    case 3:
        server_tcp()
    case 4:
        client_tcp()
