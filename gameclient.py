import socket


host = "localhost"
port = 7777

def play_game():
    s = socket.socket()
    s.connect((host, port))
    
    while True:
        difficulty_level = input("Please choose a difficulty level: \n "
                                 "a. Easy (1 - 50) \n "
                                 "b. Medium (1 - 100) \n "
                                 "c. Hard (1 - 500) \n"
                                 "Please enter your choice (a/b/c): ").strip().upper()
        if difficulty_level in ['a','b','c']:
            s.sendall(difficulty_level.encode())
            break
        else:
            print("Invallid Choice! Please choose a valid difficulty level (a/b/c): ")

        
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

