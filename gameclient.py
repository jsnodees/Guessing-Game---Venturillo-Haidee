import socket


host = "localhost"
port = 7777

def play_game():
    s = socket.socket()
    s.connect((host, port))
    
    while True:
        data = s.recv(1024)
        print(data.decode().strip())

        while True:
            #let get our input from the user
            user_input = input("").strip()
            s.sendall(user_input.encode())

            reply = s.recv(1024).decode().strip()
            print(reply)


            if "Correct" in reply:
                s.close()
                return
while True:
    play_game()
    play_again = input("Do you want to play again? (Y/N): ").upper()
    if play_again != "Y":
        break

