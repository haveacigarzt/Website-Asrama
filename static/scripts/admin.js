window.addEventListener("load", () => {
   const spinner_container = document.getElementById("spinner_container")
   spinner_container.classList.add("spinner--hidden")
   spinner_container.addEventListener("transitionend", () => {
      if (document.body.hasChildNodes(spinner_container)) {
         try {
            document.body.removeChild(spinner_container)
         }
         catch (e) {
         }
      }
   })
})

const url = document.URL.split("/")
let page = url[url.length - 1]

const edit_konten_navbar_links = document.querySelectorAll("#edit_konten_navbar a")
const tentang_link = document.querySelectorAll("[data-value='tentang']")

document.addEventListener("keydown", (event) => {
   const keyName = event.key;
   if (keyName === "Control") {
      // do not alert when only Control key is pressed.
      return;
   }
  
   if (event.ctrlKey) {
   // Even though event.key is not 'Control' (e.g., 'a' is pressed),
   // event.ctrlKey may be true if Ctrl key is pressed at the same time.
      if (keyName == "Enter") {
         // console.log(`Combination of ctrlKey + ${keyName}`);
         const btn_submit = document.querySelector(".btn-success")
         // console.dir(btn_submit)
         if(!btn_submit.disabled) {
            const form = document.querySelector(".content_form")
            if(form.id != "buletin_form") {
               // console.log(form)
               const form_n = document.getElementById(form.id)
               form_n.requestSubmit()
            }
         }
      }
   }
})

edit_konten_navbar_links.forEach(link => {
   if (page == '') {
      page = url[url.length - 2]
   }
   if (page == "admin") {
      tentang_link.forEach(el => el.classList.add("active"))
   } else if (link.dataset.value == page) {
      link.classList.add("active")
   } else {
      link.classList.remove("active")
   }
})

const buletin_card = document.querySelectorAll(".buletin-card ")
for (const c of buletin_card) {
   c.addEventListener("mouseenter", (e) => {
      e.target.childNodes[1].childNodes[1].classList.add("hovered")
   })
   c.addEventListener("mouseleave", (e) => {
      e.target.childNodes[1].childNodes[1].classList.remove("hovered")
   })
}

let form = document.querySelector(".content_form")
form.changed = [false];
form.changed2 = [false, false];

console.log(form.changed);
console.log(form.changed2);

let button = form.querySelector("input[type='submit']");

const button_container = button.parentElement;
// const alert = button_container.parentElement.querySelector(".alert");
const alert = button_container.parentElement.previousElementSibling;

const sumbit_subtitle = document.getElementById("sumbit_subtitle")

form.addEventListener("input", () => {
   const inputs = form.querySelectorAll(".form-control");
   for (let i = 0; i < inputs.length; i++) {
      if (inputs[i].dataset.before !== inputs[i].value) {
         form.changed[i] = true;
      } else {
         form.changed[i] = false;
      }
   }
   if (form.changed.includes(true) || form.changed2.includes(true)) {
      button.disabled = false;
      if(sumbit_subtitle) {sumbit_subtitle.classList.remove("text-muted")}
   } else {
      button.disabled = true;
      if(sumbit_subtitle) {sumbit_subtitle.classList.add("text-muted")}
   }
});
button_container.addEventListener("click", (e) => {
   if (button.disabled && alert.classList.contains("d-none")) {
      alert.classList.replace("d-none", "d-flex");
      setTimeout(() => {
         alert.classList.replace("d-flex", "d-none");
      }, "3000");
   }
})

const remove_card_btn = form.querySelectorAll(".remove-card-btn")
if (remove_card_btn.length > 0) {
   remove_card_btn.forEach(btn => {
      btn.addEventListener("click", (event) => {
         const target = event.target;
         let name = target.dataset.name;
         let col1 = '';
         if (window.confirm(`Hapus ${name}?`)) {
            if (target.tagName == "BUTTON") {
               col1 = target.parentElement;
            } else if (target.tagName == "I") {
               col1 = target.parentElement.parentElement
            }
            const col11 = col1.previousElementSibling;
            try {
               col1.remove();
               col11.remove();
               form.changed2[0] = true;
               button.disabled = false;
            } catch (error) {
               alert(error);
            }
            console.log(form.changed, form.changed2);
         }
      })
   })
}

const add_card_btn = form.querySelectorAll(".add-card-btn")
if (add_card_btn.length > 0) {
   add_card_btn.forEach(btn => {
      btn.addEventListener("click", (event) => {
         const target = event.target;
         let name = target.dataset.name;
         let col1 = '';
         if (target.tagName == "BUTTON") {
            col1 = target.parentElement;
         } else if (target.tagName == "I") {
            col1 = target.parentElement.parentElement;
         }
         try {
            if (name == "daftar_penghuni") {
               col1.insertAdjacentHTML("afterend", `
               <div class="col-12 col-md-11">
                  <div class="row border-black border px-2 py-3 rounded">
                     <div class="col-6 d-flex flex-column justify-content-between">
                        <div class="mb-3">
                           <label class="form-label" for=""><h6>Nama</h6></label>
                           <input required class="form-control" type="text" name="nama[]" id="" data-before="">
                        </div>
                        <div class="mb-3">
                           <label class="form-label" for=""><h6>Tahun Masuk</h6></label>
                           <input required class="form-control" type="text" name="tahun_masuk[]" id="" data-before="">
                        </div>
                        <div>
                           <label class="form-label" for=""><h6>Asal Daerah</h6></label>
                           <input required class="form-control" type="text" name="asal_daerah[]" id="" data-before="">
                        </div>
                     </div>
                     <div class="col-6">
                        <div class="mb-3">
                           <label class="form-label" for=""><h6>Jurusan</h6></label>
                           <input required class="form-control" type="text" name="jurusan[]" id="" data-before="">
                        </div>
                        <div class="mb-3">
                           <label class="form-label" for=""><h6>Angkatan</h6></label>
                           <input required class="form-control" type="text" name="angkatan[]" id="" data-before="">
                        </div>
                        <div>
                           <label class="form-label" for=""><h6>Kampus</h6></label>
                           <input required class="form-control" type="text" name="kampus[]" id="" data-before="">
                        </div>
                     </div>
                  </div>
               </div>
               <div class="mb-3 mb-md-0 col-12 col-md-1 d-flex flex-md-column align-items-center justify-content-evenly">
                  <button type="button" class="btn btn-outline-dark remove-card-btn" data-name="data penghuni baru" onclick="remove_card(event)">
                     <i class="fa-solid fa-trash" data-name="data penghuni baru"></i>
                  </button>
                  <button type="button" class="btn btn-outline-dark add-card-btn" data-name="daftar_penghuni" onclick="add_card(event)">
                     <i class="fa-solid fa-plus" data-name="daftar_penghuni"></i>
                  </button>
               </div>
               `);
            } else {
               col1.insertAdjacentHTML("afterend", `
               <div class="col-11 col-lg-10">
                  <div class="row border-black border px-2 py-3 rounded">
                     <div class="col-6 d-flex flex-column justify-content-between">
                        <div>
                           <label class="form-label" for="nama_butir_${name}_{{loop.index}}"><h6>Nama butir ${name}</h6></label>
                           <input required class="form-control" type="text" name="nama[]" id="nama_butir_${name}_{{loop.index}}" value="" data-before="">
                        </div>
                        <div>
                           <label class="form-label" for="keterangan_butir_${name}_{{loop.index}}"><h6>Keterangan</h6></label>
                           <textarea required class="form-control" name="keterangan[]" id="keterangan_butir_${name}_{{loop.index}}" cols="10" rows="5" data-before=""></textarea>
                        </div>
                     </div>
                     <div class="col-6 d-flex flex-column justify-content-between">
                        <div class="col-6 mb-3 w-100 d-flex justify-content-center">
                           <img src="{{el['gambar']}}" alt="gambar butir ${name}" srcset="" class="w-50 output-image d-none">
                        </div>
                        <div>
                           <label class="form-label" for="gambar_butir_${name}_{{loop.index}}"><h6>Pilih gambar</h6></label>
                           <input required class="form-control" type="file" accept="image/png, image/jpeg" name="gambar[]" id="gambar_butir_${name}_{{loop.index}}" value="" data-before="" onchange="loadFile(event)">
                           <input type="hidden"  name="gambar_lama[]" value="">
                        </div>
                     </div>
                  </div>
               </div>
               <div class="col-1 col-lg-2 col-button-edit-admin">
                  <button type="button" class="btn btn-outline-dark remove-card-btn" data-name="${name} baru" onclick="remove_card(event)"><i class="fa-solid fa-trash" data-name="${name} baru"></i></button>
                  <button type="button" class="btn btn-outline-dark add-card-btn" data-name="${name}" onclick="add_card(event)"><i class="fa-solid fa-plus" data-name="${name}"></i></button>
               </div>
               `);
            }
            form.changed2[1] = true;
            button.disabled = false;
         } catch (error) {
            alert(error);
         }
      })
   })
}

const add_list_btn = form.querySelectorAll(".add-list-btn")
if (add_list_btn.length > 0) {
   add_list_btn.forEach(btn => {
      btn.addEventListener("click", (event) => {
         const target = event.target;
         let name = target.dataset.name;
         let col1 = '';
         if (target.tagName == "BUTTON") {
            col1 = target.parentElement.parentElement;
         } else if (target.tagName == "I") {
            col1 = target.parentElement.parentElement.parentElement;
         }
         try {
            if (name.split(' ')[0].split('_').includes("anggota")) {
               col1.insertAdjacentHTML("afterend", `
               <div class="col-9 col-md-10 py-2 px-3">
                  <input type="text" class="form-control" name="${name}[]" data-before="" required>    
               </div>
               <div class="col-3 col-md-2 col-button-edit-admin-kepengurusan">
                  <button type="button" class="btn btn-outline-dark remove-card-btn" onclick="remove_card(event)" data-name="${name} baru" data-type="penghuni">
                     <i class="fa-solid fa-trash" data-name="${name} baru" data-type="penghuni"></i>
                  </button>
                  <button type="button" class="btn btn-outline-dark add-list-btn" onclick="add_list(event)" data-name="${name}" data-type="penghuni">
                     <i class="fa-solid fa-plus" data-name="${name}" data-type="penghuni"></i>
                  </button>
               </div>
               `);
            } else {
               col1.insertAdjacentHTML("afterend", `
               <div class="row mx-0 my-3 p-3 rounded shadow bg-artikel">
                  <div class="col-11 col-lg-10 my-2 pe-3 ps-0">
                     <div class="row mx-0 p-0">
                        <div class="col-12 p-0">
                           <label class="form-label" for=""><h6>Butir ${name}</h6></label>
                           <input type="text" class="form-control" name="${name}[]" id="" data-before=""  required>
                        </div>
                     </div>
                  </div>
                  <div class="col-1 col-lg-2 col-button-edit-admin p-0 m-0">
                     <button type="button" class="btn btn-secondary shadow-sm" onclick="add_list(event)" data-name="${name}">
                        <i class="fa-solid fa-plus" data-name="${name}"></i>
                     </button>
                     <button type="button" class="btn btn-danger shadow-sm" onclick="remove_card(event)" data-name="${name} baru">
                        <i class="fa-solid fa-trash" data-name="${name} baru"></i>
                     </button>
                  </div>
               </div>
               `);
            }
            form.changed2[1] = true;
            button.disabled = false;
         } catch (error) {
            alert(error);
         }
      })
   })
}

function remove_card(event) {
   const target = event.target
   let button = ''
   let name = target.dataset.name;
   let col1 = ''
   let row = ''
   if (window.confirm(`Hapus ${name}?`)) {
      if (target.tagName == "BUTTON") {
         col1 = target.parentElement;
         button = target.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
      } else if (target.tagName == "I") {
         col1 = target.parentElement.parentElement
         button = target.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
      }
      row = col1.parentElement;
      const col11 = col1.previousElementSibling;
      if (name.split(' ')[0].split('_').includes("anggota")) {
         col1.remove();
         col11.remove();
         button = form.querySelector("input[type='submit']");
      } else {
         row.remove();
      }
      try {
         const data_name = row.querySelectorAll(`[data-name='${name}']`)
         console.log(name);
         if (data_name.length == 0) {
            form.changed2[1] = false;
         } else {
            form.changed2[1] = true;
         }
         let there_is_new_form = data_name.length > 0
         let change_onform = form.changed.includes(true) || form.changed2.includes(true)
         if (there_is_new_form || change_onform) {
            button.disabled = false;
         } else {
            button.disabled = true;
         }
         // console.log('new form?', there_is_new_form);
         // console.log('form.changed', form.changed);
         // console.log('form.changed2', form.changed2);
         // console.log('change on form', change_onform);
      } catch (error) {
         console.error(error);
      }
   }
}

function add_card(event) {
   const target = event.target
   let button = ''
   let name = target.dataset.name;
   let col1 = ''
   if (target.tagName == "BUTTON") {
      col1 = target.parentElement.parentElement;
      button = target.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
   } else if (target.tagName == "I") {
      col1 = target.parentElement.parentElement.parentElement;
      button = target.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
   }
   try {
      if (name == "daftar_penghuni") {
         col1.insertAdjacentHTML("afterend", `
         <div class="row mx-0 my-4 p-3 rounded shadow bg-card">
            <div class="col-12 col-md-11">
               <div class="row px-2 py-3 rounded">
                  <div class="col-6 d-flex flex-column justify-content-between">
                     <div class="mb-3">
                        <label class="form-label" for=""><h6>Nama</h6></label>
                        <input required class="form-control" type="text" name="nama[]" id="" data-before="">
                     </div>
                     <div class="mb-1 mb-sm-2 mb-md-3 d-flex">
                        <div>
                           <label class="form-label" for=""><h6>Tahun Masuk</h6></label>
                           <input required class="form-control" type="text" name="tahun_masuk[]" id="">
                        </div>
                        <div class="ms-4">
                           <label class="form-label" for=""><h6>Status</h6></label>
                           <input required class="form-control" type="text" name="status[]" id="">
                        </div>
                     </div>
                     <div>
                        <label class="form-label" for=""><h6>Asal Daerah</h6></label>
                        <input required class="form-control" type="text" name="asal_daerah[]" id="" data-before="">
                     </div>
                  </div>
                  <div class="col-6">
                     <div class="mb-3">
                        <label class="form-label" for=""><h6>Jurusan</h6></label>
                        <input required class="form-control" type="text" name="jurusan[]" id="" data-before="">
                     </div>
                     <div class="mb-3">
                        <label class="form-label" for=""><h6>Angkatan</h6></label>
                        <input required class="form-control" type="text" name="angkatan[]" id="" data-before="">
                     </div>
                     <div>
                        <label class="form-label" for=""><h6>Kampus</h6></label>
                        <input required class="form-control" type="text" name="kampus[]" id="" data-before="">
                     </div>
                  </div>
               </div>
            </div>
            <div class="mb-3 mb-md-0 col-12 col-md-1 d-flex flex-md-column align-items-center justify-content-evenly">
               <button type="button" class="btn btn-secondary shadow-sm" data-name="daftar_penghuni" onclick="add_card(event)">
                  <i class="fa-solid fa-plus" data-name="daftar_penghuni"></i>
               </button>
               <button type="button" class="btn btn-danger shadow-sm" data-name="data penghuni baru" onclick="remove_card(event)">
                  <i class="fa-solid fa-trash" data-name="data penghuni baru"></i>
               </button>
            </div>
         </div>
         `);
      } else {
         col1.insertAdjacentHTML("afterend", `
         <div class="row mx-0 my-4 p-3 rounded shadow bg-card flex-column flex-md-row">
            <div class="col-12 col-md-11 col-lg-10">
               <div class="row px-2 py-3 gap-3 gap-md-0">
                  <div class="col-12 col-md-6 d-flex flex-column justify-content-between gap-2 gap-md-0">
                     <div>
                        <label class="form-label" for="nama_butir_${name}_{{loop.index}}"><h6>Nama butir ${name}</h6></label>
                        <input required class="form-control" type="text" name="nama[]" id="nama_butir_${name}_{{loop.index}}" value="" data-before="">
                     </div>
                     <div>
                        <label class="form-label" for="keterangan_butir_${name}_{{loop.index}}"><h6>Keterangan</h6></label>
                        <textarea required class="form-control" name="keterangan[]" id="keterangan_butir_${name}_{{loop.index}}" cols="10" rows="5" data-before=""></textarea>
                     </div>
                  </div>
                  <div class="col-12 col-md-6 d-flex flex-column justify-content-between">
                     <div class="col-6 mb-3 w-100 d-flex justify-content-center">
                        <img src="{{el['gambar']}}" alt="gambar butir ${name}" srcset="" class="w-50 output-image d-none">
                     </div>
                     <div>
                        <label class="form-label" for="gambar_butir_${name}_{{loop.index}}"><h6>Pilih gambar</h6></label>
                        <input required class="form-control" type="file" accept="image/png, image/jpeg" name="gambar[]" id="gambar_butir_${name}_{{loop.index}}" value="" data-before="" onchange="loadFile(event)">
                        <input type="hidden"  name="gambar_lama[]" value="">
                     </div>
                  </div>
               </div>
            </div>
            <div class="col-md-1 col-lg-2 col-button-edit-admin flex-row flex-md-column gap-5 gap-md-0 p-4 p-md-0">
               <button type="button" class="btn btn-secondary shadow-sm" onclick="add_card(event)" data-name="${name}"><i class="fa-solid fa-plus" data-name="${name}"></i></button>
               <button type="button" class="btn btn-danger shadow-sm" onclick="remove_card(event)" data-name="${name} baru"><i class="fa-solid fa-trash" data-name="${name} baru"></i></button>
            </div>
         </div>
         `);
      }
      button.disabled = false;
   } catch (error) {
      alert(error);
   }
}

function add_list(event) {
   const target = event.target
   let button = ''
   let name = target.dataset.name;
   let col1 = ''
   if (target.tagName == "BUTTON") {
      col1 = target.parentElement.parentElement;
      button = target.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
   } else if (target.tagName == "I") {
      col1 = target.parentElement.parentElement.parentElement
      button = target.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
   }
   try {
      if (name.split(' ')[0].split('_').includes("anggota")) {
         if (target.tagName == "BUTTON") {
            col1 = target.parentElement;
            button = target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
         } else if (target.tagName == "I") {
            col1 = target.parentElement.parentElement;
            button = target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");
         }
         console.log(target.tagName);
         console.log(col1);
         console.log(button);
         // button = target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector("input[type='submit']");;
         col1.insertAdjacentHTML("afterend", `
         <div class="col-8 col-sm-9 col-md-10 py-2 px-2 px-sm-3">
            <input type="text" class="form-control" name="${name}[]" data-before="" required>    
         </div>
         <div class="col-4 col-sm-3 col-md-2 px-1 px-sm-2 col-button-edit-admin-kepengurusan gap-1 gap-lg-0">
            <button type="button" class="btn btn-secondary shadow-sm add-list-btn" onclick="add_list(event)" data-name="${name}" data-type="penghuni">
               <i class="fa-solid fa-plus" data-name="${name}" data-type="penghuni"></i>
            </button>
            <button type="button" class="btn btn-danger shadow-sm remove-card-btn" onclick="remove_card(event)" data-name="${name} baru" data-type="penghuni">
               <i class="fa-solid fa-trash" data-name="${name} baru" data-type="penghuni"></i>
            </button>
         </div>
         `);
      } else {
         col1.insertAdjacentHTML("afterend", `
         <div class="row mx-0 my-3 p-3 rounded shadow bg-artikel">
            <div class="col-11 col-lg-10 my-2 pe-3 ps-0">
               <div class="row mx-0 p-0">
                  <div class="col-12 p-0">
                     <label class="form-label" for=""><h6>Butir ${name.replaceAll('_', ' ').replace('butir ', '')}</h6></label>
                     <input type="text" class="form-control" name="${name}[]" id="" data-before=""  required>
                  </div>
               </div>
            </div>
            <div class="col-1 col-lg-2 col-button-edit-admin p-0 m-0">
               <button type="button" class="btn btn-secondary shadow-sm" onclick="add_list(event)" data-name="${name}">
                  <i class="fa-solid fa-plus" data-name="${name}"></i>
               </button>
               <button type="button" class="btn btn-danger shadow-sm" onclick="remove_card(event)" data-name="${name} baru">
                  <i class="fa-solid fa-trash" data-name="${name} baru"></i>
               </button>
            </div>
         </div>
         `);
      }
      button.disabled = false;
   } catch (error) {
      console.log(error);
   }
}

function confirmLogout(event) {
   if (!confirm("Logout sekarang?")) {
      event.preventDefault()
   }
}

function confirmDelete(event, subject) {
   if (!confirm(`Hapus ${subject} ini?`)) {
      event.preventDefault()
   }
}

function loadFile(event) {
   const output = event.target.parentElement.parentElement.parentElement.querySelector('img.output-image');
   output.classList.remove("d-none")
   output.src = URL.createObjectURL(event.target.files[0]);
};

function loadFileBuletin(event) {
   const output = event.target.parentElement.parentElement.querySelector('img.output-image');
   output.classList.remove("d-none")
   output.src = URL.createObjectURL(event.target.files[0]);
};

function remove_par(e) {
   if (window.confirm("Hapus paragraf?")) {
      col1 = ''
      console.log(e.target);
      if (e.target.tagName == "BUTTON") {
         col1 = e.target.parentElement.parentElement;
      } else if (e.target.tagName == "I") {
         col1 = e.target.parentElement.parentElement.parentElement;
      }
      console.log(col1);
      try {
         col1.remove();
         form.changed2[0] = true;
         button.disabled = false;
      } catch (error) {
         alert(error);
      }
   }
}

function add_par(e, new_artikel = false) {
   col1 = ''
   console.log(e.target);
   if (e.target.tagName == "BUTTON") {
      col1 = e.target.parentElement.parentElement;
   } else if (e.target.tagName == "I") {
      col1 = e.target.parentElement.parentElement.parentElement;
   }
   if (new_artikel) {
      col1 = document.getElementById("control_tambah_paragraf")
   }
   try {
      col1.insertAdjacentHTML('afterend', `
            <div class="row mx-1 my-2 m-md-3 px-1 pt-1 pb-2 px-md-3 py-md-3 flex-shrink-1 shadow rounded bg-artikel">
               <input type="hidden" name="is_gambar[]" value="">
               <div class="col-12 col-md-10">
                  <label for="" class="form-label"><h6>Teks</h6></label>
                  <textarea name="par_text[]" required class="form-control" name="" id="" rows="6"></textarea>
               </div>
               <div class="col-12 col-md-2 d-flex flex-md-column align-items-center justify-content-evenly mt-3 mt-md-0">
                  <button type="button" class="btn btn-danger shadow" title="Hapus Paragraf" onclick="remove_par(event)">
                     <i class="fa-solid fa-trash" title="Hapus Paragraf"></i>
                  </button>
                  <button type="button" class="btn btn-secondary shadow" title="Tambah Paragraf (Teks)" onclick="add_par(event)">
                     <i class="fa-solid fa-align-right" title="Tambah Paragraf (Teks)"></i>
                  </button>
                  <button type="button" class="btn btn-secondary shadow" title="Tambah Paragraf (Teks & Gambar)" onclick="add_par_gam(event)">
                     <i class="fa-solid fa-align-right mx-1" title="Tambah Paragraf (Teks & Gambar)"></i>
                     <i class="fa-solid fa-image mx-1" title="Tambah Paragraf (Teks & Gambar)"></i>
                  </button>
               </div>
            </div>
            `)
      if (!new_artikel) {
         form.changed2[1] = true;
         button.disabled = false;
      }
   } catch (error) {
      alert(error);
   }
}

function add_par_gam(e, new_artikel = false) {
   col1 = ''
   console.log(e.target);
   if (e.target.tagName == "BUTTON") {
      col1 = e.target.parentElement.parentElement;
   } else if (e.target.tagName == "I") {
      col1 = e.target.parentElement.parentElement.parentElement;
   }
   if (new_artikel) {
      col1 = document.getElementById("control_tambah_paragraf")
   }
   try {
      col1.insertAdjacentHTML('afterend', `
            <div class="row mx-1 my-2 m-md-3 px-1 pt-1 pb-2 px-md-3 py-md-3 flex-shrink-1 shadow rounded bg-artikel">
               <input type="hidden" name="is_gambar[]" value="1">
               <div class="col-12 col-md-5">
                  <label class="form-label" for=""><h6>Teks</h6></label>
                  <textarea required class="form-control" name="par_text[]" id="" rows="6"></textarea>
               </div>
               <div class="col-12 col-md-5 d-flex flex-column align-items-center mt-3 mt-md-0">
                  <img src='' width="200" height="170" alt="" class="output-image d-none">
                  <div class="mt-2 mt-md-3">
                     <label class="form-label"><h6>Pilih gambar</h6></label>
                     <input required class="form-control" type="file" accept="image/png, image/jpeg" onchange="loadFileBuletin(event)" name="par_gambar[]">
                     <input type="hidden" name="par_gambar_lama[]" value="">
                  </div>
               </div>
               <div class="col-12 col-md-2 d-flex flex-md-column align-items-center justify-content-evenly mt-3 mt-md-0">
                  <button type="button" class="btn btn-danger shadow" title="Hapus Paragraf" onclick="remove_par(event)">
                     <i class="fa-solid fa-trash" title="Hapus Paragraf"></i>
                  </button>
                  <button type="button" class="btn btn-secondary shadow" title="Tambah Paragraf (Teks)" onclick="add_par(event)">
                     <i class="fa-solid fa-align-right" title="Tambah Paragraf (Teks)"></i>
                  </button>
                  <button type="button" class="btn btn-secondary shadow" title="Tambah Paragraf (Teks & Gambar)" onclick="add_par_gam(event)">
                     <i class="fa-solid fa-align-right mx-1" title="Tambah Paragraf (Teks & Gambar)"></i>
                     <i class="fa-solid fa-image mx-1" title="Tambah Paragraf (Teks & Gambar)"></i>
                  </button>
               </div>
            </div>
            `)
      if (!new_artikel) {
         form.changed2[1] = true;
         button.disabled = false;
      }
   } catch (error) {
      alert(error);
   }
}

