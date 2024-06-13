import random
import string
import streamlit as st

class KodeVerifikasi:
    def __init__(self):
        if 'code_valid' not in st.session_state:
            st.session_state.code_valid = self.generate_random_code()
        if 'keadaan' not in st.session_state:
            st.session_state.keadaan = 'LOGOUT'
        if 'percobaan' not in st.session_state:
            st.session_state.percobaan = 0
        self.max_percobaan = 3
        st.info(f"(Contoh Terkirim di SMS) Random Kode: {st.session_state.code_valid}")

    def event(self, event, user_input):
        if st.session_state.keadaan == 'LOGOUT':
            if event == 'Masuk':
                if user_input == st.session_state.code_valid:
                    st.session_state.keadaan = 'LOGIN'
                    st.success("Verifikasi Berhasil!")
                else:
                    st.session_state.percobaan += 1
                    if st.session_state.percobaan >= self.max_percobaan:
                        st.session_state.keadaan = 'LOCKED'
                        st.error("Kode Salah, Akun terkunci karena terlalu banyak percobaan gagal.")
                    else:
                        st.session_state.keadaan = 'FAILED'
                        st.error("Kode Salah, Silahkan Coba Lagi!")
        elif st.session_state.keadaan == 'FAILED':
            if event == 'Masuk' and user_input == st.session_state.code_valid:
                st.session_state.keadaan = 'LOGIN'
                st.success("Verifikasi Berhasil!")
            elif event == 'Masuk':
                st.session_state.percobaan += 1
                if st.session_state.percobaan >= self.max_percobaan:
                    st.session_state.keadaan = 'LOCKED'
                    st.error("Kode Salah, Akun terkunci karena terlalu banyak percobaan gagal.")
                else:
                    st.error("Kode Salah, Silahkan Coba Lagi!")

    def get_keadaan(self):
        return st.session_state.keadaan

    def generate_random_code(self, length=6):
        code_characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(code_characters) for _ in range(length))
        return code

auth_system = KodeVerifikasi()

def user_login():
    st.title('Sistem Verifikasi Kode')
    user_input = st.text_input('Masukkan Kode Verifikasi')
    if st.button('Masuk'):
        auth_system.event('Masuk', user_input)
        if auth_system.get_keadaan() == 'LOCKED':
            st.error("Kode Salah, Akun terkunci karena terlalu banyak percobaan gagal.")

user_login()
