window.addEventListener("load", () => {
   const spinner_container = document.getElementById("spinner_container")
   spinner_container.classList.add("spinner--hidden")
   spinner_container.addEventListener("transitionend", () => {
      try {
         document.body.removeChild(spinner_container)
      } catch (error) {

      }
   })
})

const reveal_pass_btn = (target) => {
   let button;
   let input;
   let i_tag = document.getElementById("pass_reveal_btn")
   if (target.localName == "button") {
      button = target;
      input = target.previousElementSibling;
   } else if (target.localName == "i") {
      button = target.parentElement;
      input = target.parentElement.previousElementSibling;
   }
   if (i_tag.classList.contains("fa-eye-slash")) {
      input.removeAttribute("type", "password")
      input.setAttribute("type", "text")
   } else {
      input.removeAttribute("type", "text")
      input.setAttribute("type", "password")
   }
   i_tag.classList.toggle("fa-eye-slash")
   i_tag.classList.toggle("fa-eye")
}