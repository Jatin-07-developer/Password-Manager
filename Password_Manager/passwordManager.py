from cryptography.fernet import Fernet

def load_key():
    with open("key.key", "rb") as file:
        return file.read()

key = Fernet.generate_key()
fer = Fernet(key)

print(key)

def view():
    try:
        with open("password.txt", "r") as file:
            for line in file:
                name, encrypted_password = line.rstrip().split("|")

                password = fer.decrypt(
                    encrypted_password.encode()
                ).decode()

                print("Account:", name, "| Password:", password)

    except FileNotFoundError:
        print("No passwords saved yet.")

def add():
    name = input("Enter Account Name: ")
    password = input("Enter Password: ")

    encrypted_password = fer.encrypt(password.encode()).decode()

    with open("password.txt", "a") as file:
        file.write(name + "|" + encrypted_password + "\n")

    print("Password saved successfully!")

while True:
    mode = input(
        "\nWould you like to add a new password or view existing ones? "
        "(add/view/q): "
    ).lower()

    if mode == "q":
        print("Goodbye!")
        break

    elif mode == "add":
        add()

    elif mode == "view":
        view()

    else:
        print("Invalid option. Please choose add, view, or q.")