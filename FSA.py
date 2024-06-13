import random
import string

class KodeVerifikasi:
    def __init__(self):
        self.keadaan = 'LOGOUT'  
        self.percobaan = 0
        self.max_percobaan = 3  
        self.code_valid = self.generate_random_code()  
        print("(Contoh Terkirim di SMS) Random Kode:", self.code_valid)

    def event(self, event, user_input):
        if self.keadaan == 'LOGOUT':
            if event == 'Masuk':
                if user_input == self.code_valid:
                    self.keadaan = 'LOGIN'
                    print("Verifikasi Berhasil!")
                else:
                    self.percobaan += 1
                    if self.percobaan >= self.max_percobaan:
                        self.keadaan = 'LOCKED'
                    else:
                        self.keadaan = 'FAILED'
                        print("Kode Salah, Silahkan Coba Lagi!")
        elif self.keadaan == 'FAILED':
            if event == 'Masuk' and user_input == self.code_valid:
                self.keadaan = 'LOGIN'
                print("Verifikasi Berhasil!")
            elif event == 'Masuk':
                self.percobaan += 1
                if self.percobaan >= self.max_percobaan:
                    self.keadaan = 'LOCKED'
                else:
                    print("Kode Salah, Silahkan Coba Lagi!")

    def get_keadaan(self):
        return self.keadaan

    def generate_random_code(self, length=6):
        code_characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(code_characters) for _ in range(length))
        return code

auth_system = KodeVerifikasi()

def user_login():
    while auth_system.get_keadaan() not in ['LOGIN', 'LOCKED']:
        user_input = input('Masukkan Kode Verifikasi: ')
        auth_system.event('Masuk', user_input)
        if auth_system.get_keadaan() == 'LOCKED':
            print("Kode Salah, Akun terkunci karena terlalu banyak percobaan gagal.")
            return

user_login()