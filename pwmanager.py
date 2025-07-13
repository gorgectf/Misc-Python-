from  cryptography.fernet import Fernet

def write_key():
    key = Fernet.generate_key()

    with open("key.key", "wb") as key_file: # write bytes mode
        key_file.write(key)

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

master_pwd: any = input("Input the master password: ")
key = load_key() + master_pwd.encode()
fer = Fernet(key)

def view():
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip() # strips the carrager turn (\n) from the line

            user, pwd = data.split("|") # Reads a string and splits every part of it per every occurence of the split() argument, this case the pipe symbol
            print("User: ", user, " Password: ", (fer.decrypt(pwd.encode()).decode()))

def add():
    name = input("Account name: ")
    pwd = input("Password: ")

    if len(name) > 0 and len(pwd) > 0:
        with open("passwords.txt", "a") as f: # Using statement like in VB, a is APPEND (adds to), w is WRITE (clears and writes), r is READ
            f.write(name + " | " + fer.encrypt(pwd.encode()).decode() + "\n") #\n adds a new line, its called a carrager turn
    else:
        pass

while True:
    mode = input("Add new password or view existing? (add, view): ").lower()
    if mode == 'q':
        quit()

    if mode == "add":
        add()
    elif mode == "view":
        view()
    else:
        print("Invalid.")
        continue