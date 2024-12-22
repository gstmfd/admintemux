#!/usr/bin/python3
#coding=utf-8

import os
import sys
import time
import json
import random
import smtplib
import shutil
import socket
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup as parser
import requests
import concurrent.futures

# Data pengguna
USERS = {
    "user1": {"password": "password123", "email": "user1@example.com"},
    "user2": {"password": "mypassword", "email": "user2@example.com"}
}

# SMTP untuk pengiriman email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "youremail@gmail.com"
EMAIL_PASSWORD = "yourpassword"

# Warna terminal
r, g, y, c, p, w, a = "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[94m", "\033[97m", "\033[0m"

MENU_LOGO = f"""
{r}███████╗██╗   ██╗███████╗██████╗ ██╗   ██╗
██╔════╝██║   ██║██╔════╝██╔══██╗██║   ██║
███████╗██║   ██║█████╗  ██████╔╝██║   ██║
╚════██║██║   ██║██╔══╝  ██╔═══╝ ██║   ██║
███████║╚██████╔╝███████╗██║     ╚██████╔╝
╚══════╝ ╚═════╝ ╚══════╝╚═╝      ╚═════╝
"""

UPDATE = "22-12-2024 10:00"

def send_reset_email(email, recovery_code):
    try:
        # Membuat email
        message = MIMEMultipart()
        message['From'] = EMAIL_SENDER
        message['To'] = email
        message['Subject'] = "Kode Pemulihan Kata Sandi"
        body = f"Kode pemulihan Anda adalah: {recovery_code}"
        message.attach(MIMEText(body, 'plain'))

        # Kirim email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email, message.as_string())

        print(f"{g}[✓] Kode pemulihan berhasil dikirim ke {email}{a}")
    except Exception as e:
        print(f"{r}[x] Gagal mengirim email: {e}{a}")

def login():
    os.system("clear")
    print(MENU_LOGO)
    print(f"{g}[LOGIN] Masukkan username dan password Anda\n")
    username = input(f"{c}Username: {a}")
    password = input(f"{c}Password: {a}")

    if username in USERS and USERS[username]["password"] == password:
        print(f"{g}[✓] Login berhasil! Selamat datang, {username}{a}")
        time.sleep(2)
        menu()
    else:
        print(f"{r}[x] Username atau password salah!{a}")
        time.sleep(2)
        login()

def reset_password():
    os.system("clear")
    print(MENU_LOGO)
    print(f"{g}[RESET PASSWORD] Masukkan username untuk memulihkan akun Anda\n")
    username = input(f"{c}Username: {a}")

    if username in USERS:
        email = USERS[username]["email"]
        recovery_code = str(random.randint(100000, 999999))
        send_reset_email(email, recovery_code)

        entered_code = input(f"{c}Masukkan kode pemulihan yang dikirim ke email: {a}")
        if entered_code == recovery_code:
            new_password = input(f"{c}Masukkan password baru: {a}")
            USERS[username]["password"] = new_password
            print(f"{g}[✓] Password berhasil diubah!{a}")
        else:
            print(f"{r}[x] Kode pemulihan salah!{a}")
    else:
        print(f"{r}[x] Username tidak ditemukan!{a}")
    time.sleep(2)
    menu()

def download_virtex():
    try:
        print(f"{p}[{y}!{p}] {r}Menghubungkan ke server...{a}")
        data = requests.get(
            "https://www.mediafire.com/api/1.4/folder/get_content.php?content_type=files&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key=ueti9cij4zf3i&response_format=json"
        ).json()
        files = data['response']['folder_content']['files']
    except requests.exceptions.RequestException:
        exit(f"{p}[{y}!{p}] {r}Tidak ada koneksi!{a}")

    os.system("clear")
    print(MENU_LOGO)
    print(f"{g}Pilih file yang ingin diunduh:\n")
    for i, file in enumerate(files, start=1):
        print(f"{p}[{r}{i}{p}] {y}{file['filename']}{a}")
    print(f"{p}[{r}0{p}] {c}Kembali ke menu utama\n")
    choice = input(f"{g}>>> {a}")

    if choice.isdigit() and 1 <= int(choice) <= len(files):
        file = files[int(choice) - 1]
        print(f"{p}[{y}!{p}] {y}Mengunduh {file['filename']}{a}")
        url = file['links']['normal_download']
        response = requests.get(url)
        with open(file['filename'], 'wb') as f:
            f.write(response.content)
        print(f"{g}[✓] File berhasil diunduh: {file['filename']}{a}")
    elif choice == "0":
        menu()
    else:
        print(f"{r}[x] Pilihan tidak valid!{a}")
        time.sleep(2)
        download_virtex()

def menu():
    os.system("clear")
    print(MENU_LOGO)
    print(f"{g}[1] {y}Login")
    print(f"{g}[2] {y}Reset Password")
    print(f"{g}[3] {y}Unduh File Virtex")
    print(f"{g}[0] {r}Keluar\n")
    choice = input(f"{w}Pilih Menu {c}> {a}")

    if choice == "1":
        login()
    elif choice == "2":
        reset_password()
    elif choice == "3":
        download_virtex()
    elif choice == "0":
        sys.exit()
    else:
        print(f"{r}[x] Pilihan tidak valid!{a}")
        time.sleep(1)
        menu()

if __name__ == "__main__":
    menu()
