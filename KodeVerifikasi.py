import random
import string
import time
import subprocess
import os
import sys

def generate_random_password(length=6):
    password_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(password_characters) for i in range(length))
    return password

class kodeVerifikasi:
    def __init__(self):
        self.percobaan = 0
        self.keadaan = 'LOGOUT'
        self.passwordValid = generate_random_password()
        print("(Contoh Terkirim di SMS) Random password:", self.passwordValid)

    def event(self, event, user_input):
        if self.keadaan == 'LOGOUT':
            if event == 'Masuk':
                if user_input == self.passwordValid:
                    self.keadaan = 'LOGIN'
                    self.percobaan = 0
                    print("Verifikasi Berhasil!")
                    return True
                else:
                    self.percobaan += 1
                    if self.percobaan == 1:
                        print("Kode Salah, Silahkan Coba Lagi!")
                    elif self.percobaan == 2:
                        print("Kode Salah, Silahkan Coba Lagi! Sisa 1 kali Kesempatan!")
                    elif self.percobaan == 3:
                        self.keadaan = 'LOCK'
                        print("Kode Salah, Akun Anda telah terkunci.")
                        print("Coba lagi setelah 15 Detik!")
                        time.sleep(15) 
                        subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
                        print("Waktu Time Out Telah Selesai")
                        print("Apakah Anda ingin kirim ulang kode? Pilih Ya atau Tidak!")
                        self.pilihan = input()
                        if self.pilihan == 'Ya':
                            self.keadaan = 'LOGOUT'
                            self.percobaan = 0
                            self.passwordValid = generate_random_password()
                            print("(Contoh Terkirim di SMS) Random password:", self.passwordValid)
                            print("Kode Telah Dikirim Ulang. Silahkan Dicoba Kembali.")
                        elif self.pilihan == 'Tidak':
                            print("Terima Kasih!")
                            sys.exit()
    def get_keadaan(self):
        return self.keadaan

auth_system = kodeVerifikasi()

def userLogin():
    while auth_system.get_keadaan() != 'LOGIN':
        user_input = input('Masukkan Kode Verifikasi: ')
        if auth_system.event('Masuk', user_input):
            break
        if auth_system.get_keadaan() == 'LOCK':
            return
        if auth_system.get_keadaan() == 'LOGIN':
            print("Verifikasi Berhasil!")
userLogin()
