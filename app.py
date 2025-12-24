from flask import Flask, request, make_response, redirect, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, asyncio

# 15/12/2023
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from queries import get_all_content, get_artikel, update_tentang, update_pembinaan, update_fasilitas, update_buletin, update_artikel, tambah_artikel, delete_artikel_buletin, update_kegiatan, update_makna_arti_logo, update_kepengurusan, update_daftar_penghuni, update_kontak, get_account

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('flask_secret_key')

app.url_map.strict_slashes = False

def token_required(func):
   @wraps(func)
   def decorated(*args, **kwargs):
      token = request.cookies.get("token")
      if not token:
         flash(f"Harap login terlebih dahulu.", "warning")
         return redirect(url_for("login"))
      try:
         payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
      except:
         flash(f"Harap login terlebih dahulu.", "warning")
         return redirect(url_for("login"))
      return func(*args, **kwargs)
   return decorated


class NameForm(FlaskForm):
   name = StringField("What is your name?", validators=[DataRequired()])
   submit = SubmitField("Submit")

class LoginForm(FlaskForm):
   username = StringField("Username", validators=[DataRequired()])
   password = PasswordField("Password", validators=[DataRequired()])
   masuk = SubmitField("Masuk")

class ContentForm(FlaskForm):
   submit = SubmitField("Simpan")

# 15/12/2023
class FeedbackForm(FlaskForm):
   saran = TextAreaField("Feedback", validators=[DataRequired()])
   submit = SubmitField("Kirim")

# Unprotected
@app.route('/', methods=['GET', 'POST'])
def index():

   # 15/12/2023
   form_feedback = FeedbackForm()
   if request.method == "POST" and form_feedback.validate_on_submit():
      text = request.form['saran']
      subject = "Feedback pengguna website Asrama Mhs Santo Bonaventura"
      
      sender_email = os.getenv('email')
      sender_password = os.getenv('email_pass')
      receiver_email = os.getenv('receiver_email')

      message = MIMEMultipart()
      message['From'] = sender_email
      message['To'] = receiver_email
      message['Subject'] = subject
      message.attach(MIMEText(text, 'plain'))

      try:
         server = smtplib.SMTP('smtp.gmail.com', 587)
         server.starttls()
         server.login(sender_email, sender_password)
         server.sendmail(sender_email, receiver_email, message.as_string())
         server.quit()

         flash(f"Terima kasih saran anda sudah kami terima.", "success")

      except Exception as e:
         flash(f"Gagal mengirim saran: {str(e)}", "danger")
      

   
   token = request.cookies.get("token")
   is_admin = True
   if token:
      try:
         payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
      except:
         is_admin = False
   else:
      is_admin = False
      
   data2 = asyncio.run(get_all_content())
   tentang = list(filter(lambda p: p["group"] == "tentang", data2))[0]
   pembinaan = list(filter(lambda p: p["group"] == "pembinaan_di_asrama", data2))[0]
   fasilitas = list(filter(lambda p: p["group"] == "fasilitas_asrama", data2))[0]
   buletin = list(filter(lambda p: p["group"] == "buletin_asrama", data2))[0]
   artikel = list(filter(lambda p: p["group"] == "artikel", data2))[0]
   kegiatan = list(filter(lambda p: p["group"] == "kegiatan_rutin", data2))[0]
   makna_arti_logo = list(filter(lambda p: p["group"] == "makna_dan_arti_logo", data2))[0]
   kepengurusan = list(filter(lambda p: p["group"] == "kepengurusan_asrama", data2))[0]
   daftar_penghuni = list(filter(lambda p: p["group"] == "daftar_penghuni", data2))[0]
   kontak = list(filter(lambda p: p["group"] == "kontak", data2))[0]
   tentang = {
      "deskripsi_asrama": list(filter(lambda p: p["name"] == "deskripsi_asrama", tentang["fields"]))[0]["value"],
      "slot_tersedia": list(filter(lambda p: p["name"] == "slot_tersedia", tentang["fields"]))[0]["value"],
      "misi": list(filter(lambda p: p["name"] == "misi", tentang["fields"]))[0]["value"],
      "visi": list(filter(lambda p: p["name"] == "visi", tentang["fields"]))[0]["value"],
      "tatib": list(filter(lambda p: p["name"] == "tatib", tentang["fields"]))[0]["value"],
      "persyaratan": list(filter(lambda p: p["name"] == "persyaratan", tentang["fields"]))[0]["value"],
   }
   pembinaan = {
      "deskripsi_pembinaan": list(filter(lambda p: p["name"] == "deskripsi_pembinaan", pembinaan["fields"]))[0]["value"],
      "butir_pembinaan": list(filter(lambda p: p["name"] == "butir_pembinaan", pembinaan["fields"]))[0]["value"]
   }
   fasilitas = {
      "deskripsi_fasilitas": list(filter(lambda p: p["name"] == "deskripsi_fasilitas", fasilitas["fields"]))[0]["value"],
      "butir_fasilitas": list(filter(lambda p: p["name"] == "butir_fasilitas", fasilitas["fields"]))[0]["value"]
   }
   buletin = {
      "deskripsi_buletin": list(filter(lambda p: p["name"] == "deskripsi_buletin", buletin["fields"]))[0]["value"],
      "butir_buletin": artikel["fields"]
   }
   kegiatan = {
      "deskripsi_kegiatan": list(filter(lambda p: p["name"] == "deskripsi_kegiatan", kegiatan["fields"]))[0]["value"],
      "butir_kegiatan": list(filter(lambda p: p["name"] == "butir_kegiatan", kegiatan["fields"]))[0]["value"]
   }
   makna_arti_logo = {
      "deskripsi_makna_arti_logo": list(filter(lambda p: p["name"] == "deskripsi_makna_arti_logo", makna_arti_logo["fields"]))[0]["value"],
      "butir_makna_arti_logo": list(filter(lambda p: p["name"] == "butir_makna_arti_logo", makna_arti_logo["fields"]))[0]["value"]
   }
   kepengurusan = {
      "tahun_kepengurusan": list(filter(lambda p: p["name"] == "tahun_kepengurusan", kepengurusan["fields"]))[0]["value"],
      "pengurus_inti": list(filter(lambda p: p["name"] == "pengurus_inti", kepengurusan["fields"]))[0]["value"],
      "seksi": list(filter(lambda p: p["name"] == "seksi", kepengurusan["fields"]))[0]["value"]
   }
   daftar_penghuni = daftar_penghuni["fields"]
   kontak = kontak["fields"]
   
   for el in buletin["butir_buletin"]:
      try:
         el["waktu_dibuat"] = float(el["waktu_dibuat"])
      except Exception as e:
         el["waktu_dibuat"] = 0

   buletin["butir_buletin"] = sorted(buletin["butir_buletin"], key=lambda d: d["waktu_dibuat"], reverse=True)
   
   for el in buletin["butir_buletin"]:
      waktu = datetime.fromtimestamp(el["waktu_dibuat"])
      el["waktu_dibuat"] = f"{waktu.day}/{waktu.month}/{waktu.year}"


   return render_template('beranda.html', tentang=tentang, pembinaan=pembinaan, fasilitas=fasilitas, buletin=buletin, kegiatan=kegiatan, makna_arti_logo=makna_arti_logo, kepengurusan=kepengurusan, daftar_penghuni=daftar_penghuni, kontak=kontak, form_feedback=form_feedback, is_admin=is_admin)


@app.route('/buletin/')
@app.route('/buletin/<id>')
def buletin(id=0):
   token = request.cookies.get("token")
   is_admin = True
   if token:
      try:
         payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
      except:
         is_admin = False
   else:
      is_admin = False
   
   data = asyncio.run(get_artikel(id))
   waktu = datetime.fromtimestamp(float(data["waktu_dibuat"]))
   data["waktu_dibuat"] = f"{waktu.day}/{waktu.month}/{waktu.year} {waktu.hour}:{waktu.minute}"
   return render_template('buletin.html', buletin='true', is_admin=is_admin, data=data)


# Protected
@app.route('/admin', methods=["GET", "POST"])
@app.route('/admin/tentang', methods=["GET", "POST"])
@token_required
def admin_tentang():
   form_tentang = ContentForm()

   if request.method == "POST" and form_tentang.validate_on_submit():
      data = asyncio.run(update_tentang(request.form, request.form.getlist("tatib[]"), request.form.getlist("persyaratan[]")))
      if data:
         flash(f"Berhasil mengubah konten Tentang", "success")
      else:
         flash(f"Gagal mengubah konten Tentang", "danger")
      return redirect(url_for("admin_tentang"))

   data = asyncio.run(get_all_content())
   tentang = list(filter(lambda p: p["group"] == "tentang", data))[0]

   return render_template('admin_partials/tentang.html',is_admin=True, form_tentang=form_tentang, tentang=tentang)

@app.route('/admin/pembinaan', methods=["GET", "POST"])
@token_required
def admin_pembinaan():
   form_pembinaan = ContentForm()

   data = asyncio.run(get_all_content())
   pembinaan = list(filter(lambda p: p["group"] == "pembinaan_di_asrama", data))[0]

   if request.method == "POST" and form_pembinaan.validate_on_submit():
      data = asyncio.run(update_pembinaan(request.form, request.form.getlist("nama[]"), request.files.getlist("gambar[]"), request.form.getlist("gambar_lama[]"), request.form.getlist("keterangan[]")))
      if data:
         flash(f"Berhasil mengubah konten Pembinaan", "success")
      else:
         flash(f"Gagal mengubah konten Pembinaan", "danger")
      return redirect(url_for("admin_pembinaan"))


   return render_template('admin_partials/pembinaan.html',is_admin=True,  form_pembinaan=form_pembinaan, pembinaan=pembinaan)

@app.route('/admin/fasilitas', methods=["GET", "POST"])
@token_required
def admin_fasilitas():
   form_fasilitas = ContentForm()

   data = asyncio.run(get_all_content())
   fasilitas = list(filter(lambda p: p["group"] == "fasilitas_asrama", data))[0]

   if request.method == "POST" and form_fasilitas.validate_on_submit():
      data = asyncio.run(update_fasilitas(request.form, request.form.getlist("nama[]"), request.files.getlist("gambar[]"), request.form.getlist("gambar_lama[]"), request.form.getlist("keterangan[]")))
      if data:
         flash(f"Berhasil mengubah konten Fasilitas", "success")
      else:
         flash(f"Gagal mengubah konten Fasilitas", "danger")
      return redirect(url_for("admin_fasilitas"))

   
   return render_template('admin_partials/fasilitas.html',is_admin=True,  form_fasilitas=form_fasilitas, fasilitas=fasilitas)
   
@app.route('/admin/buletin', methods=["GET", "POST"])
@token_required
def admin_buletin():
   form_buletin = ContentForm()

   data = asyncio.run(get_all_content())
   buletin = list(filter(lambda p: p["group"] == "buletin_asrama", data))[0]

   artikel = list(filter(lambda p: p["group"] == "artikel", data))[0]

   buletin = {
      "deskripsi_buletin": list(filter(lambda p: p["name"] == "deskripsi_buletin", buletin["fields"]))[0]["value"],
      "butir_buletin": artikel["fields"]
   }

   for el in buletin["butir_buletin"]:
      try:
         el["waktu_dibuat"] = float(el["waktu_dibuat"])
      except Exception as e:
         el["waktu_dibuat"] = 0

   buletin["butir_buletin"] = sorted(buletin["butir_buletin"], key=lambda d: d["waktu_dibuat"], reverse=True)

   for el in buletin["butir_buletin"]:
      waktu = datetime.fromtimestamp(el["waktu_dibuat"])
      el["waktu_dibuat"] = f"{waktu.day}/{waktu.month}/{waktu.year}"

   if request.method == "POST" and form_buletin.validate_on_submit():
      # print(request.form["deskripsi_buletin"], request.files.getlist("thumbnail[]"))
      data = asyncio.run(update_buletin(request.form["deskripsi_buletin"]))

      if data:
         flash(f"Berhasil mengubah deskripsi Buletin", "success")
      else:
         flash(f"Gagal mengubah deskripsi Buletin", "danger")
      return redirect(url_for("admin_buletin"))

   return render_template('admin_partials/buletin.html',is_admin=True,  form_buletin=form_buletin, buletin=buletin)
   

@app.route('/admin/tambah-buletin', methods=["GET", "POST"])
@token_required
def admin_tambah_buletin():
   form_buletin = ContentForm()
   if request.method == "POST" and form_buletin.validate_on_submit():
      data = asyncio.run(tambah_artikel(request.form, request.files["thumbnail"], request.form.getlist("par_text[]"), request.form.getlist("is_gambar[]"), request.files.getlist("par_gambar[]")))

      if data:
         flash(f"Berhasil menambakkan Artikel", "success")
      else:
         flash(f"Gagal menambakhan Artikel", "danger")
      return redirect(url_for("admin_buletin"))


   return render_template('admin_partials/tambah_buletin.html', is_admin=True,  form_buletin=form_buletin)


@app.route('/admin/buletin/<id>', methods=["GET", "POST"])
@token_required
def admin_buletin_artikel(id=0):
   form_buletin = ContentForm()
   
   if request.method == "POST" and form_buletin.validate_on_submit():
      data = asyncio.run(update_artikel(request.form, request.files["thumbnail"], request.form.getlist("par_text[]"), request.form.getlist("is_gambar[]"), request.files.getlist("par_gambar[]"), request.form.getlist("par_gambar_lama[]"), id))

      if data:
         flash(f"Berhasil mengubah Artikel Buletin", "success")
      else:
         flash(f"Gagal mengubah Artikel Buletin", "danger")
      return redirect(url_for("admin_buletin_artikel", id=id))
   

   token = request.cookies.get("token")
   is_admin = True
   if token:
      try:
         payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
      except:
         is_admin = False
   else:
      is_admin = False

   data = asyncio.run(get_artikel(id))

   return render_template('admin_partials/buletin_artikel.html', buletin='true', form_buletin=form_buletin, is_admin=is_admin, data=data)


@app.route('/admin/buletin/<id>/delete', methods=["POST"])
@token_required
def admin_delete_buletin_artikel(id=0):
   res = asyncio.run(delete_artikel_buletin(id))
   if res:
      flash("Sukses hapus artikel", "success")
      return redirect(url_for("admin_buletin"))
   else:
      flash("Gagal hapus artikel", "danger")
      return redirect(url_for("admin_buletin_artikel", id=id))


@app.route('/admin/kegiatan', methods=["GET", "POST"])
@token_required
def admin_kegiatan():
   form_kegiatan = ContentForm()

   data = asyncio.run(get_all_content())
   kegiatan = list(filter(lambda p: p["group"] == "kegiatan_rutin", data))[0]

   if request.method == "POST" and form_kegiatan.validate_on_submit():
      data = asyncio.run(update_kegiatan(request.form, request.form.getlist("nama[]"), request.files.getlist("gambar[]"), request.form.getlist("gambar_lama[]"), request.form.getlist("keterangan[]")))
      if data:
         flash(f"Berhasil mengubah konten Kegiatan", "success")
      else:
         flash(f"Gagal mengubah konten Kegiatan", "danger")
      return redirect(url_for("admin_kegiatan"))

   return render_template('admin_partials/kegiatan.html',is_admin=True,  form_kegiatan=form_kegiatan, kegiatan=kegiatan)


@app.route('/admin/makna-arti-logo', methods=["GET", "POST"])
@token_required
def admin_makna_arti_logo():
   form_makna_arti_logo = ContentForm()

   data = asyncio.run(get_all_content())
   makna_arti_logo = list(filter(lambda p: p["group"] == "makna_dan_arti_logo", data))[0]

   if request.method == "POST" and form_makna_arti_logo.validate_on_submit():
      data = asyncio.run(update_makna_arti_logo(request.form, request.form.getlist("butir_makna_arti_logo[]")))
      if data:
         flash(f"Berhasil mengubah konten Makna & Arti Logo", "success")
      else:
         flash(f"Gagal mengubah konten Makna & Arti Logo", "danger")
      return redirect(url_for("admin_makna_arti_logo"))

   return render_template('admin_partials/makna_arti_logo.html',is_admin=True,  form_makna_arti_logo=form_makna_arti_logo, makna_arti_logo=makna_arti_logo)


@app.route('/admin/kepengurusan', methods=["GET", "POST"])
@token_required
def admin_kepengurusan():
   form_kepengurusan = ContentForm()

   data = asyncio.run(get_all_content())
   kepengurusan = list(filter(lambda p: p["group"] == "kepengurusan_asrama", data))[0]

   if request.method == "POST" and form_kepengurusan.validate_on_submit():
      data = asyncio.run(update_kepengurusan(request.form, request.form.getlist("anggota_1[]"), request.form.getlist("anggota_2[]"), request.form.getlist("anggota_3[]"), request.form.getlist("anggota_4[]")))
      if data:
         flash(f"Berhasil mengubah konten Kepengurusan", "success")
      else:
         flash(f"Gagal mengubah konten Kepengurusan", "danger")
      return redirect(url_for("admin_kepengurusan"))
   
   return render_template('admin_partials/kepengurusan.html',is_admin=True,  form_kepengurusan=form_kepengurusan, kepengurusan=kepengurusan)


@app.route('/admin/daftar-penghuni', methods=["GET", "POST"])
@token_required
def admin_daftar_penghuni():
   form_daftar_penghuni = ContentForm()

   data = asyncio.run(get_all_content())
   daftar_penghuni = list(filter(lambda p: p["group"] == "daftar_penghuni", data))[0]

   if request.method == "POST" and form_daftar_penghuni.validate_on_submit():
      data = asyncio.run(update_daftar_penghuni(request.form.getlist("nama[]"), request.form.getlist("tahun_masuk[]"), request.form.getlist("asal_daerah[]"), request.form.getlist("jurusan[]"), request.form.getlist("angkatan[]"), request.form.getlist("kampus[]")))
      if data:
         flash(f"Berhasil mengubah konten Daftar Penghuni", "success")
      else:
         flash(f"Gagal mengubah konten Daftar Penghuni", "danger")
      return redirect(url_for("admin_daftar_penghuni"))

   return render_template('admin_partials/daftar_penghuni.html',is_admin=True, form_daftar_penghuni=form_daftar_penghuni, daftar_penghuni=daftar_penghuni)


@app.route('/admin/kontak', methods=["GET", "POST"])
@token_required
def admin_kontak():
   form_kontak = ContentForm()

   data = asyncio.run(get_all_content())
   kontak = list(filter(lambda p: p["group"] == "kontak", data))[0]

   if request.method == "POST" and form_kontak.validate_on_submit():
      kontak = {
         "whatsapp": request.form["whatsapp"],
         "email": request.form["email"],
         "instagram": request.form["instagram"],
         "youtube": request.form["youtube"],
         "alamat": request.form["alamat"],
         "maps": request.form["maps"]
      }
      data = asyncio.run(update_kontak(kontak))
      if data:
         flash(f"Berhasil mengubah konten Kontak", "success")
      else:
         flash(f"Gagal mengubah konten Kontak", "danger")
      return redirect(url_for("admin_kontak"))
   
   return render_template('admin_partials/kontak.html',is_admin=True,  form_kontak=form_kontak, kontak=kontak)


@app.route('/login', methods=["GET", "POST"])
def login():
   form = LoginForm()
   token = request.cookies.get("token")
   is_admin = True
   if token:
      try:
         payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
         flash(f"Anda sudah login!", "warning")
         return redirect(url_for("admin_tentang"))
      except:
         is_admin = False
   else:
      is_admin = False
   if form.validate_on_submit():
      account = asyncio.run(get_account(form.username.data))
      if account:
         if check_password_hash(account["password"], form.password.data):
            token = jwt.encode({"username": form.username.data, "exp": datetime.utcnow() + timedelta(days=1)}, app.config["SECRET_KEY"], algorithm="HS256")
            flash(f"Selamat datang di halaman Admin!", "success")
            resp = make_response(redirect(url_for("admin_tentang")))
            resp.set_cookie("token", token)
            return resp           
         else:
            flash(f"Username/password salah!", "danger")
      else :
         flash(f"Username/password salah!", "danger")
      return redirect(url_for("login"))
   return render_template('login.html', form=form, is_admin=is_admin, login=True)


@app.route('/logout', methods=[ "POST"])
@token_required
def logout():
   if request.method == "POST":
      flash(f"Berhasil logout!", "success")
      resp = make_response(redirect(url_for("index")))
      resp.set_cookie("token", "", expires=0)
      return resp


@app.errorhandler(404)
def page_not_found(e):
   token = request.cookies.get("token")
   is_admin = True
   if token:
      try:
         payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
      except:
         is_admin = False
   else:
      is_admin = False

   return render_template('404.html', is_admin=is_admin), 404

if __name__ == "__main__":
   app.run(debug=True, port=4000)