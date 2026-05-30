from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os

# Fungsi membuat key dari password
def generate_key(password):
    return SHA256.new(password.encode()).digest()

# Fungsi Encrypt File
def encrypt_file():
    file_name = input("\nMasukkan nama file yang akan dienkripsi: ")
    password = input("Masukkan password: ")

    if not os.path.exists(file_name):
        print("\n[!] File tidak ditemukan!")
        return

    key = generate_key(password)

    with open(file_name, "rb") as file:
        data = file.read()

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    encrypted_file = file_name + ".enc"

    with open(encrypted_file, "wb") as file:
        file.write(cipher.nonce)
        file.write(tag)
        file.write(ciphertext)

    print("\n========== ENKRIPSI BERHASIL ==========")
    print("File asli      :", file_name)
    print("File encrypted :", encrypted_file)

# Fungsi Decrypt File
def decrypt_file():
    file_name = input("\nMasukkan nama file encrypted: ")
    password = input("Masukkan password: ")

    if not os.path.exists(file_name):
        print("\n[!] File tidak ditemukan!")
        return

    key = generate_key(password)

    with open(file_name, "rb") as file:
        nonce = file.read(16)
        tag = file.read(16)
        ciphertext = file.read()

    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        output_file = "hasil_decrypt.txt"

        with open(output_file, "wb") as file:
            file.write(data)

        print("\n========== DEKRIPSI BERHASIL ==========")
        print("File encrypted :", file_name)
        print("File decrypt   :", output_file)

    except ValueError:
        print("\n[!] Password salah atau file rusak!")

# Menu Program
while True:
    print("\n===================================")
    print(" PROGRAM ENKRIPSI FILE AES ")
    print("===================================")
    print("1. Encrypt File")
    print("2. Decrypt File")
    print("3. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        encrypt_file()

    elif pilihan == "2":
        decrypt_file()

    elif pilihan == "3":
        print("\nProgram selesai.")
        break

    else:
        print("\n[!] Pilihan tidak tersedia!")