## HOW TO USE

--------------------------------------------------
### 1. PERSYARATAN
- Python 3.14 atau lebih baru
- Akun email & sandi aplikasi untuk SMTP
- Cara membuat sandi aplikasi untuk SMTP: https://www.rumahweb.com/journal/cara-mengaktifkan-application-password-gmail/

--------------------------------------------------
### 2. STRUKTUR PROJECT
Website-Asrama/ <br>
├── static/ <br>
├── templates/ <br>
├── app.py <br>
├── queries.py <br>
├── .env (buat sendiri) <br>
└── README.md <br>

--------------------------------------------------
### 3. BUAT VIRTUAL ENVIRONMENT (OPSIONAL)
Jalankan pada terminal/command promt di direktori Website-Asrama/:

- python -m venv namavirtualenvironment
- Lalu aktifkan dengan: source namavirtualenvironment/Scripts/activate

--------------------------------------------------
### 4. INSTALL DEPENDENCY
Jalankan pada terminal/command promt:

pip install -r requirements.txt

--------------------------------------------------
### 5. BUAT FILE .env
File ini berfungsi sebagai konfigurasi program. Buat dan simpan di Website-Asrama/

Isi file .env:

- email=#email pengirim
- email_pass=#sandi aplikasi email pengirim
- receiver_email=#email penerima

Atau pakai punya saya:

- email=pramanaafriandy@gmail.com
- email_pass=uizeurequennqfcw
- receiver_email=afriandy193@gmail.com

--------------------------------------------------
### 6. LAUNCH PROGRAM
Jalankan pada terminal/command promt di direktori Website-Asrama/:

- python app.py
- Lalu buka localhost:4000 pada browser
- Ctrl+C pada terminal/command promt untuk menghentikan program
- Username/Password = admin/adminbona
