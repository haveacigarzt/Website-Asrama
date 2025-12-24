var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
   return new bootstrap.Popover(popoverTriggerEl)
})

window.addEventListener("load", () => {
   const spinner_container = document.getElementById("spinner_container")
   spinner_container.classList.add("spinner--hidden")
   spinner_container.addEventListener("transitionend", () => {
      if (document.body.contains(spinner_container)) {
         document.body.removeChild(spinner_container)
      }
   })
})

window.onload = function () {
   if (window.innerWidth >= 768) {
      document.getElementById("button_group_daftar").classList.replace("btn-group-vertical", "btn-group")
   } else {
      document.getElementById("button_group_daftar").classList.replace("btn-group", "btn-group-vertical")
   }
}

window.onresize = function () {
   if (window.innerWidth >= 768) {
      document.getElementById("button_group_daftar").classList.replace("btn-group-vertical", "btn-group")
   } else {
      document.getElementById("button_group_daftar").classList.replace("btn-group", "btn-group-vertical")
   }
}

const sections = document.querySelectorAll(".anchor");
const navLi = document.querySelectorAll(".link");
function active_link(li) {
   navLi.forEach((item) => item.classList.remove("active"));
   li.classList.add("active");
}
navLi.forEach((item) => {
   item.addEventListener('click', function () {
      active_link(this);
   })
})
const kontak = document.querySelector(`[data-anchor='kontak_anchor']`)
window.onscroll = () => {
   sections.forEach(section => {
      let top = window.scrollY;
      let offset = section.offsetTop;
      let height = section.offsetHeight;
      let id = section.getAttribute("id");

      if (top >= offset && top < offset + height) {
         const target = document.querySelector(`[data-anchor='${id}']`)
         active_link(target);
      }
   })
   if ((window.innerHeight + Math.round(window.scrollY)) >= document.body.offsetHeight - 10) {
      navLi.forEach((item) => item.classList.remove("active"));
      kontak.classList.add("active");
   } else {
      kontak.classList.remove("active");
   }
};

const vm_tp = document.getElementById("vm_tp")
const visi_misi = vm_tp.querySelector("#visi_misi")
const tatib_persy = vm_tp.querySelector("#tatib_persyaratan")
const toggle_visi = vm_tp.querySelectorAll('input[name="options-outlined"]')
for (let t of toggle_visi) {
   t.addEventListener("click", (e) => {
      if (t.checked) {
         if (t.id == "success-outlined") {
            visi_misi.style.display = "flex"
            tatib_persy.style.display = "none"
         } else {
            visi_misi.style.display = "none"
            tatib_persy.style.display = "flex"
         }
      }
   })
}

const penghuni_sec = document.getElementById("penghuni_div")
const pengurus = penghuni_sec.querySelector("#struktur_pengurus")
const daftar_penghuni = penghuni_sec.querySelector("#daftar_penghuni")
const toggle_pengurus = penghuni_sec.querySelectorAll('input[name="options-outlined2"]')
for (let t of toggle_pengurus) {
   t.addEventListener("click", (e) => {
      if (t.checked) {
         if (t.id == "success-outlined2") {
            pengurus.classList.replace("d-none", "d-block")
            daftar_penghuni.classList.replace("d-block", "d-none")
         } else {
            pengurus.classList.replace("d-block", "d-none")
            daftar_penghuni.classList.replace("d-none", "d-block")
         }
      }
   })
}

const buletin_card = document.querySelectorAll(".buletin-card ")
for (const c of buletin_card) {
   c.addEventListener("mouseenter", (e) => {
      e.target.childNodes[1].childNodes[1].classList.add("hovered")
   })
   c.addEventListener("mouseleave", (e) => {
      e.target.childNodes[1].childNodes[1].classList.remove("hovered")
   })
}

const trHover = document.querySelectorAll(".tr-hover");
trHover.forEach(el => {
   el.addEventListener("mouseenter", (event) => {
      const tds = event.target.querySelectorAll('td')
      tds.forEach(td => td.classList.add('td-hovered'))
   })
   el.addEventListener("mouseleave", (event) => {
      const tds = event.target.querySelectorAll('td')
      tds.forEach(td => td.classList.remove('td-hovered'))
   })
});

let table1 = new DataTable('#tablePenghuni');

// const copyContent = (event) => {
//    const text = event.target.dataset["copy"];
//    try {
//       navigator.clipboard.writeText(text);
//       alert("Copied to clipboard!");
//    } catch (err) {
//       alert('Failed to copy: ', err);
//    }
// }

function copyContent(event) {
   let target = ''
   if (event.target.tagName == "BUTTON") {
      target = event.target;
   } else if (event.target.tagName == "I") {
      target = event.target.parentElement;
   } else if (event.target.tagName == "SMALL") {
      target = event.target.parentElement;
   }

   const textToCopy = target.dataset["copy"];
   try {
      navigator.clipboard.writeText(textToCopy);
      alert(`Copied to clipboard!`);
   } catch (err) {
      alert(`Failed to copy ${textToCopy}: `, err);
   }
}

// const myModal = document.getElementById('myModal')
// const myInput = document.getElementById('myInput')

// myModal.addEventListener('shown.bs.modal', () => {
//    myInput.focus()
// })

const hover_the_link = (event) => {
   const btn = event.target.querySelector(".badge");
   btn.classList.add("hovered")
}

const unhover_the_link = (event) => {
   const btn = event.target.querySelector(".badge");
   btn.classList.remove("hovered")
}

function confirmLogout(event) {
   if (!confirm("Logout sekarang?")) {
      event.preventDefault()
   }
}

const card_pembinaan = document.querySelectorAll(".card-pembinaan")
card_pembinaan.forEach(el => {
})
card_pembinaan.forEach(el => {
   let deskripsi_small = el.querySelector(".deskripsi-small")
   const el_height = el.offsetHeight
   const height_gap = deskripsi_small.scrollHeight - deskripsi_small.offsetHeight
   console.log("gap ", height_gap)
   if(height_gap) {
      el.addEventListener("mouseenter", () => {
         deskripsi_small.classList.add("line_clamp_unset")
         // console.log(el_height)
         // el.classList.remove("height-fit-content")
         el.style.height = `${el_height + height_gap}px`
      })
      el.addEventListener("mouseleave", () => {
         // console.log(el)
         // const deskripsi_small = el.querySelector(".deskripsi-small")
         deskripsi_small.classList.remove("line_clamp_unset")
         // el.classList.add("height-fit-content")
         el.style.height = `${el_height}px`
      })
   }
})