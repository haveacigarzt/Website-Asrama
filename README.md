--------------------------------------------------
### 1. PERSYARATAN
--------------------------------------------------
- Python 3.14 atau lebih baru
- Akun email (Gmail / Outlook / Yahoo)

--------------------------------------------------
### 2. STRUKTUR PROJECT
--------------------------------------------------
Website-Asrama/
│
├── static/
├── templates/
├── app.py
├── queries.py
├── .env (buat sendiri)
└── README.txt

--------------------------------------------------
### 3. BUAT VIRTUAL ENVIRONMENT (OPSIONAL)
--------------------------------------------------
--------------------------------------------------
Jalankan pada terminal/command promt di direktori Website-Asrama/:

- python -m venv namavirtualenvironment
Lalu aktifkan:
- source namavirtualenvironment/Scripts/activate

--------------------------------------------------
### 4. INSTALL DEPENDENCY
--------------------------------------------------
Jalankan pada terminal/command promt:

pip install requirements.txt

--------------------------------------------------
### 5. MEMBUAT FILE .env
--------------------------------------------------
File ini berfungsi sebagai konfigurasi program. Buat dan simpan di Website-Asrama/

Isi file .env:

- email=#email pengirim
- email_pass=#sandi aplikasi email pengirim
- receiver_email=#email penerima

Atau pakai punya saya:

- email=pramanaafriandy@gmail.com
- email_pass=uizeurequennqfcw
- receiver_email=afriandy193@gmail.com
