from motor.motor_asyncio import AsyncIOMotorClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()

upload_folder = "static/pictures/contents"

url_db = os.getenv('url_db_atlas')

client = AsyncIOMotorClient(url_db)

ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
   return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def resize_image(src, size):
   foo = Image.open(src)
   small = foo.resize(size, Image.Resampling.LANCZOS)
   return small

async def get_all_content():
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]
      res = content_collection.find({ "new": True })
      li = []
      for a in await res.to_list(length=100):
         li.append(a)
      return li
   except Exception:
      print("MongoDB: Fail to connect")
      return False

async def get_account(username):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      account_collection = db["accounts"]
      res = await account_collection.find_one({"username": username})
      return res
   
   except Exception:
      print("MongoDB: Fail to connect")
      return False

async def get_artikel(id):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]
      res = await content_collection.find_one({"group": "artikel"})
      res2 = list(filter(lambda el: el['id'] == str(id), res["fields"]))
      return res2[0]
   
   except Exception:
      print("MongoDB: Fail to connect")
      return False

async def update_tentang(new_data, list_tatib, list_persyaratan):
   # data = await content_collection.find_one({"group": "tentang"})
   # print(new_data)
   # print(list_tatib)
   # print(data)
   
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_deskripsi = await content_collection.update_one({"group":"tentang", "fields": {"$elemMatch": {"name": "deskripsi_asrama"}}}, {"$set": {"fields.$.value": new_data["deskripsi_asrama"]}})
      res_slot_tersedia = await content_collection.update_one({"group":"tentang", "fields": {"$elemMatch": {"name": "slot_tersedia"}}}, {"$set": {"fields.$.value": new_data["slot_tersedia"]}})
      res_visi = await content_collection.update_one({"group":"tentang", "fields": {"$elemMatch": {"name": "visi"}}}, {"$set": {"fields.$.value": new_data["visi"]}})
      res_misi = await content_collection.update_one({"group":"tentang", "fields": {"$elemMatch": {"name": "misi"}}}, {"$set": {"fields.$.value": new_data["misi"]}})
      res_tatib = await content_collection.update_one({"group":"tentang", "fields": {"$elemMatch": {"name": "tatib"}}}, {"$set": {"fields.$.value": list_tatib}})
      res_persyaratan = await content_collection.update_one({"group":"tentang", "fields": {"$elemMatch": {"name": "persyaratan"}}}, {"$set": {"fields.$.value": list_persyaratan}})

   except Exception:
      print("MongoDB: Fail to connect")
      return False
   
   return True

async def update_pembinaan(new_data, list_nama, list_gambar, list_gambar_lama,  list_keterangan):

   list_gambar_new = []

   for i in range(len(list_gambar)):
      if list_gambar[i].filename and allowed_file(list_gambar[i].filename):
         resized_image = resize_image(list_gambar[i], (400, 305))
         ext = list_gambar[i].filename.split('.')[-1]

         list_gambar[i].filename = f"pembinaan{i}.{ext}"
         filename = secure_filename(list_gambar[i].filename)

         path = os.path.join(upload_folder, filename)
         new_path = os.path.join(os.getcwd(), path)

         resized_image.save(new_path)
         
         list_gambar_new.append(f"/{path}")
      else:
         list_gambar_new.append(list_gambar_lama[i])

   butir_pembinaan = []
   for i in range(len(list_nama)):
      butir_pembinaan.append({'name': list_nama[i], 'value': list_keterangan[i], 'gambar': list_gambar_new[i]})
   
   # # print(butir_pembinaan)

   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_deskripsi = await content_collection.update_one({"group":"pembinaan_di_asrama", "fields": {"$elemMatch": {"name": "deskripsi_pembinaan"}}}, {"$set": {"fields.$.value": new_data["deskripsi_pembinaan"]}})

      res_butir_pembinaan = await content_collection.update_one({"group":"pembinaan_di_asrama", "fields": {"$elemMatch": {"name": "butir_pembinaan"}}}, {"$set": {"fields.$.value": butir_pembinaan}})


   except Exception:
      print("MongoDB: Fail to connect")
      return False
   
   return True

async def update_fasilitas(new_data, list_nama, list_gambar, list_gambar_lama, list_keterangan):

   list_gambar_new = []

   for i in range(len(list_gambar)):
      if list_gambar[i].filename and allowed_file(list_gambar[i].filename):
         resized_image = resize_image(list_gambar[i], (400, 305))
         ext = list_gambar[i].filename.split('.')[-1]

         list_gambar[i].filename = f"fasilitas{i}.{ext}"
         filename = secure_filename(list_gambar[i].filename)

         path = os.path.join(upload_folder, filename)
         new_path = os.path.join(os.getcwd(), path)

         resized_image.save(new_path)

         list_gambar_new.append(f"/{path}")
      else:
         list_gambar_new.append(list_gambar_lama[i])

   butir_fasilitas = []
   for i in range(len(list_nama)):
      butir_fasilitas.append({'name': list_nama[i], 'value': list_keterangan[i], 'gambar': list_gambar_new[i]})
   
   # print('BUTIR FASILITAS: ',butir_fasilitas)

   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_deskripsi = await content_collection.update_one({"group":"fasilitas_asrama", "fields": {"$elemMatch": {"name": "deskripsi_fasilitas"}}}, {"$set": {"fields.$.value": new_data["deskripsi_fasilitas"]}})

      res_butir_fasilitas = await content_collection.update_one({"group":"fasilitas_asrama", "fields": {"$elemMatch": {"name": "butir_fasilitas"}}}, {"$set": {"fields.$.value": butir_fasilitas}})


   except Exception:
      print("MongoDB: Fail to connect")
      return False

   return True

async def update_buletin(deskripsi):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_deskripsi = await content_collection.update_one({"group":"buletin_asrama", "fields": {"$elemMatch": {"name": "deskripsi_buletin"}}}, {"$set": {"fields.$.value": deskripsi}})

   except Exception:
      print("MongoDB: Fail to connect")
      return False
   
   return True

async def update_artikel(data, thumbnail, list_text, is_gambar, list_gambar, list_gambar_lama, id):
   client = AsyncIOMotorClient(url_db)
   db = client["asbon"]
   content_collection = db["contents"]
   
   res = await content_collection.find_one({"group": "artikel"})
   res2 = list(filter(lambda el: el['id'] == str(id), res["fields"]))

   new_konten = []

   list_gambar_new = []

   if len(list_gambar) > 0:
      for i in range(len(list_gambar)):
         if list_gambar[i].filename and allowed_file(list_gambar[i].filename):
            resized_image = resize_image(list_gambar[i], (400, 305))
            ext = list_gambar[i].filename.split('.')[-1]

            list_gambar[i].filename = f"gambar_{i}_artikel_{id}.{ext}"
            filename = secure_filename(list_gambar[i].filename)

            path = os.path.join(upload_folder, filename)
            new_path = os.path.join(os.getcwd(), path)

            resized_image.save(new_path)

            list_gambar_new.append(f"/{path}")
         else:
            list_gambar_new.append(list_gambar_lama[i])
   else:
      list_gambar_new = list_gambar_lama

   y = 0
   x = 0
   for i in is_gambar:
      if i:
         new_konten.append({
            "text": list_text[y],
            "gambar": list_gambar_new[x]
         })
         x = x+1
      else:
         new_konten.append({
            "text": list_text[y]
         })
      y = y+1

   print(new_konten)

   if len(res2) > 0:
      old_data = res2[0]

      path_thumbnail = ''

      if thumbnail.filename and allowed_file(thumbnail.filename):
         ext = thumbnail.filename.split('.')[-1]
         thumbnail.filename = f"thumbnail_artikel_{old_data['id']}.{ext}"
         filename = secure_filename(thumbnail.filename)
         path = os.path.join(upload_folder, filename)
         thumbnail.save(path)
         path_thumbnail = f"/{path}"
      else:
         path_thumbnail = old_data["thumbnail"]

      
      new_data = {
         "tanggal": data["tanggal"],
         "lokasi": data["lokasi"],
         "thumbnail": path_thumbnail,
         "judul": data["judul"],
         "subjudul": data["subjudul"],
         "penulis": data["penulis"],
         "id": old_data["id"],
         "waktu_dibuat": old_data["waktu_dibuat"],
         "konten": new_konten
      }

      res_delete_artikel = await content_collection.update_one(
         {
            "group":"artikel",
            "fields": {"$elemMatch": {"id": id}},
         }, 
         {
            "$set": {"fields.$": new_data}
         }
         )
      
      return True
   
   return True

async def tambah_artikel(data, thumbnail, list_text, is_gambar, list_gambar):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]
      
      res = content_collection.find({ "new": True })
      li = []
      for a in await res.to_list(length=100):
         li.append(a)

      artikel = list(filter(lambda p: p["group"] == "artikel", li))[0]
      old_data = []

      ids = []
      for el in artikel["fields"]:
         old_data.append(el)
         ids.append(el["id"])

      new_id = 0
      while True:
         if str(new_id) in ids:
            new_id += 1
         else:
            break

      new_id = str(new_id)

      path_thumbnail = ''

      if thumbnail.filename and allowed_file(thumbnail.filename):
         resized_image = resize_image(thumbnail, (400, 305))
         ext = thumbnail.filename.split('.')[-1]

         thumbnail.filename = f"thumbnail_artikel_{new_id}.{ext}"
         filename = secure_filename(thumbnail.filename)

         path = os.path.join(upload_folder, filename)
         new_path = os.path.join(os.getcwd(), path)

         resized_image.save(new_path)

         path_thumbnail = f"/{path}"
      else:
         return False
      
      dt = datetime.now()
      ts = datetime.timestamp(dt)

      new_konten = []

      list_gambar_new = []

      if len(list_gambar) > 0:
         for i in range(len(list_gambar)):
            if list_gambar[i].filename and allowed_file(list_gambar[i].filename):
               resized_image = resize_image(list_gambar[i], (400, 305))
               ext = list_gambar[i].filename.split('.')[-1]

               list_gambar[i].filename = f"gambar_{i}_artikel_{new_id}.{ext}"
               filename = secure_filename(list_gambar[i].filename)

               path = os.path.join(upload_folder, filename)
               new_path = os.path.join(os.getcwd(), path)

               resized_image.save(new_path)

               list_gambar_new.append(f"/{path}")

      y = 0
      x = 0
      for i in is_gambar:
         if i:
            new_konten.append({
               "text": list_text[y],
               "gambar": list_gambar_new[x]
            })
            x = x+1
         else:
            new_konten.append({
               "text": list_text[y]
            })
         y = y+1

      new_data = {
         "tanggal": data["tanggal"],
         "lokasi": data["lokasi"],
         "thumbnail": path_thumbnail,
         "judul": data["judul"],
         "subjudul": data["subjudul"],
         "penulis": data["penulis"],
         "id": new_id,
         "waktu_dibuat": str(ts),
         "konten": new_konten
      }

      old_data.append(new_data)
      new_artikel = old_data
      print(new_artikel)

      res_tambah_artikel = await content_collection.update_one(
         {
            "group":"artikel"
         }, 
         {
            "$set": {"fields": new_artikel}
         }
      )

   except Exception:
      print("MongoDB: Fail to connect")
      return False
   
   return True

async def delete_artikel_buletin(id):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res = await content_collection.find_one({"group":"artikel"})

      match = list(filter(lambda p: p["id"] == id, res["fields"]))

      print(f"The original list is: {len(res['fields'])}")

      if len(match) == 1:
         index = None
         for i, d in enumerate(res["fields"]):
            if d['id'] == id:
               index = i
               break
      
         if index is not None:
            res["fields"].pop(index)

      else:
         return False
      
      print(f"The original list after delete: {len(res['fields'])}")
      # print(res["fields"])

      res_delete_artikel = await content_collection.update_one(
      {
         "group":"artikel"
      }, 
      {
         "$set": {"fields": res["fields"]}
      }
      )


   except Exception:
      print("MongoDB: Fail to connect")
      return False
   
   return True

async def update_kegiatan(new_data, list_nama, list_gambar, list_gambar_lama, list_keterangan):
   
   list_gambar_new = []

   for i in range(len(list_gambar)):
      if list_gambar[i].filename and allowed_file(list_gambar[i].filename):
         resized_image = resize_image(list_gambar[i], (400, 305))
         ext = list_gambar[i].filename.split('.')[-1]

         list_gambar[i].filename = f"kegiatan{i}.{ext}"
         filename = secure_filename(list_gambar[i].filename)

         path = os.path.join(upload_folder, filename)
         new_path = os.path.join(os.getcwd(), path)

         resized_image.save(new_path)

         list_gambar_new.append(f"/{path}")
      else:
         list_gambar_new.append(list_gambar_lama[i])

   butir_kegiatan = []
   for i in range(len(list_nama)):
      butir_kegiatan.append({'name': list_nama[i], 'value': list_keterangan[i], 'gambar': list_gambar_new[i]})
   
   # print('BUTIR kegiatan: ',butir_kegiatan)

   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_deskripsi = await content_collection.update_one({"group":"kegiatan_rutin", "fields": {"$elemMatch": {"name": "deskripsi_kegiatan"}}}, {"$set": {"fields.$.value": new_data["deskripsi_kegiatan"]}})

      res_butir_kegiatan = await content_collection.update_one({"group":"kegiatan_rutin", "fields": {"$elemMatch": {"name": "butir_kegiatan"}}}, {"$set": {"fields.$.value": butir_kegiatan}})


   except Exception:
      print("MongoDB: Fail to connect")
      return False

   return True

async def update_makna_arti_logo(new_data, list_makna_arti_logo):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_deskripsi = await content_collection.update_one({"group":"makna_dan_arti_logo", "fields": {"$elemMatch": {"name": "deskripsi_makna_arti_logo"}}}, {"$set": {"fields.$.value": new_data["deskripsi_makna_arti_logo"]}})

      res_butir_makna_arti_logo = await content_collection.update_one({"group":"makna_dan_arti_logo", "fields": {"$elemMatch": {"name": "butir_makna_arti_logo"}}}, {"$set": {"fields.$.value": list_makna_arti_logo}})


   except Exception:
      print("MongoDB: Fail to connect")
      return False

   modified = res_deskripsi.modified_count + res_butir_makna_arti_logo.modified_count
   if not modified:
      print("MongoDB: Fail to update")
      return False
   return True

async def update_kontak(kontak):
   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_kontak = await content_collection.update_one({"group":"kontak"}, {"$set": {"fields": kontak}})

   except Exception:
      print("MongoDB: Fail to connect")
      return False

   return True

async def update_kepengurusan(new_data, anggota_1, anggota_2, anggota_3, anggota_4):
   seksi = [
      {
         "name": new_data["nama_1"],
         "value": {
            "koordinator": new_data["koordinator_1"],
            "anggota": anggota_1
         }
      },
      {
         "name": new_data["nama_2"],
         "value": {
            "koordinator": new_data["koordinator_2"],
            "anggota": anggota_2
         }
      },
      {
         "name": new_data["nama_3"],
         "value": {
            "koordinator": new_data["koordinator_3"],
            "anggota": anggota_3
         }
      },
      {
         "name": new_data["nama_4"],
         "value": {
            "koordinator": new_data["koordinator_4"],
            "anggota": anggota_4
         }
      }
   ]

   pengurus_inti = {
      "ketua_yayasan": new_data["ketua_yayasan"],
      "pembina": new_data["pembina"],
      "ketua_asrama": new_data["ketua_asrama"],
      "sekretaris": new_data["sekretaris"],
      "bendahara": new_data["bendahara"]
   }

   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_tahun_kepengurusan = await content_collection.update_one({"group":"kepengurusan_asrama", "fields": {"$elemMatch": {"name": "tahun_kepengurusan"}}}, {"$set": {"fields.$.value": new_data["tahun_kepengurusan"]}})

      res_pengurus_inti = await content_collection.update_one({"group":"kepengurusan_asrama", "fields": {"$elemMatch": {"name": "pengurus_inti"}}}, {"$set": {"fields.$.value": pengurus_inti}})

      res_seksi = await content_collection.update_one({"group":"kepengurusan_asrama", "fields": {"$elemMatch": {"name": "seksi"}}}, {"$set": {"fields.$.value": seksi}})

   except Exception:
      print("MongoDB: Fail to connect")
      return False

   return True

async def update_daftar_penghuni(nama, tahun_masuk, asal_daerah, jurusan, angkatan, kampus):

   penghuni = []

   for i in range(len(nama)):
      penghuni.append({
         "nama": nama[i],
         "tahun_masuk": tahun_masuk[i],
         "asal_daerah": asal_daerah[i],
         "jurusan": jurusan[i],
         "angkatan": angkatan[i],
         "kampus": kampus[i]
      })

   print(penghuni)

   try:
      client = AsyncIOMotorClient(url_db)
      db = client["asbon"]
      content_collection = db["contents"]

      res_penghuni = await content_collection.update_one({"group":"daftar_penghuni"}, {"$set": {"fields": penghuni}})

   except Exception:
      print("MongoDB: Fail to connect")
      return False

   # modified = res_penghuni.modified_count
   # if not modified:
   #    print("MongoDB: Fail to update")
   #    return False
   return True
