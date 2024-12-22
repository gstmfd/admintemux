import os

# Banner sederhana
def banner():
    print("=" * 40)
    print("    Welcome to Secure Login System    ")
    print("=" * 40)

# Fungsi utama
def main():
    banner()
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write("admin:admin123\n")  # Akun default
    
    print("\n1. Login\n2. Register\n3. Exit")
    choice = input("Pilih opsi: ")

    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Pilihan tidak valid!")

# Fungsi login
def login():
    username = input("Username: ")
    password = input("Password: ")
    with open("users.txt", "r") as f:
        users = f.readlines()
    
    for user in users:
        stored_username, stored_password = user.strip().split(":")
        if username == stored_username and password == stored_password:
            print("Login berhasil!")
            return
    print("Login gagal! Username atau password salah.")

# Fungsi register
def register():
    username = input("Buat username: ")
    password = input("Buat password: ")
    with open("users.txt", "a") as f:
        f.write(f"{username}:{password}\n")
    print("Registrasi berhasil! Silakan login.")

if __name__ == "__main__":
    main()