
      function saveDialog(){
        document.getElementById("popup_box").classList.add("show");
        document.getElementById("popup_input").focus();
        document.getElementById("popup_input").select();
        document.getElementById("blur-underlay").classList.add("active");
      }

      const boxes = document.querySelectorAll(".popup_btn");

      boxes.forEach((box) => {
        box.addEventListener("click", () => {
          document.getElementById("popup_box").classList.remove("show");
          document.getElementById("blur-underlay").classList.remove("active");

        });
      });