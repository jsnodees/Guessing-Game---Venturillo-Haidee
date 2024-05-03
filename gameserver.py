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

leaderboard_file = "leaderboard.txt"

leaderboard = {}
try:
    with open(leaderboard_file, "r") as file:
        for line in file:
            try:
                username, score, difficulty = line.strip().split(',')
                leaderboard[username] = {'score': int(score), 'difficulty': difficulty}
            except ValueError:
                continue
except FileNotFoundError:
    pass

def generate_random_int(low, high):
    return random.randint(low, high)

def generate_random_number(difficulty):
    if difficulty == "a":
        return generate_random_int(1, 50)
    elif difficulty == "b":
        return generate_random_int(1, 100)
    elif difficulty == "c":
        return generate_random_int(1, 500)
    else:
        return generate_random_int(1, 100)
    
def display_leaderboard():
    print("\n== Leaderboard ==")
    for username, info in sorted(leaderboard.items(), key=lambda x: x[1]['score']):
        print(f"{username}: {info['score']} tries (Difficulty: {info['difficulty']})")

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
    else:
        conn.sendall(banner.encode())
        client_input = conn.recv(1024).decode().strip().lower()
        difficulty = None
        if client_input in ['a', 'b', 'c']:
            difficulty = client_input
            guessme = generate_random_number(difficulty)
            print(f"Difficulty level chosen: {guessme}")
            print(f"Number to guess: {guessme}")
            conn.sendall(b"Enter your guess: ")
            attempts = 0
        else:
            username = client_input
            conn.sendall(b"Invalid choice! Please choose again.")
            break

        if guessme is None:
            conn.sendall(b"Invalid Choice! Please choose a valid difficulty level (a/b/c) ")
            continue
        
        print(f"Selected difficulty: {client_input}, Number to guess: {guessme}")
        conn.sendall(b"Game is now started! \n Enter your guess ")

        while True:
            client_input = conn.recv(1024).decode().strip().lower()
            guess = str(client_input)
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Your Answer is Correct! ")
                conn.close()
                conn = None
                break
            elif guess > guessme:
                conn.sendall(b"Please Guess Lower! \n Enter your guess: ")
                continue
            elif guess < guessme:
                conn.sendall(b"Please Guess Higher! \n Enter your guess: ")
                continue
