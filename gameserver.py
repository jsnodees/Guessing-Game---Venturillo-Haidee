import socket
import random 

host = "0.0.0.0"
port = 7777
banner = """

== Guessing Game v1.0 ==
Choose difficulty level:
a. Easy (1-50)
b. Medium (1-100)
c. Hard (1-500)

Enter your choice (a/b/c): """

def generate_random_int(difficulty):
    if difficulty == "a":
        return random.randint(1, 50)
    elif difficulty == "b":
        return random.randint(1, 100)
    elif difficulty == "c":
        return random.randint(1, 500)
    else:
        return None

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")
conn = None
while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
        # cheat_str = f"==== number to guess is {guessme} \n" + banner 
        # conn.sendall(cheat_str.encode())
        conn.sendall(banner.encode())
    else:
        client_input = conn.recv(1024).decode().strip().upper()
        guess = generate_random_int(client_input)
        if guess is None:
            conn.sendall(b"Invalid Choice! Please choose a valid difficulty level (a/b/c) ")
            continue
        print(f"Selected difficulty: {client_input}, Number to guess: {guess}")
        conn.sendall(b"Game is now started! \n Enter your guess ")

        conn.sendall(b"Guess Lower!\nenter guess: ")
        continue