document.addEventListener("DOMContentLoaded", () => {
    (document.querySelectorAll(".notification .delete") || []).forEach(
      ($delete) => {
        const $notification = $delete.parentNode;
  
        $delete.addEventListener("click", () => {
          $notification.parentNode.removeChild($notification);
        });
      }
    );
  
    (document.querySelectorAll("input[type='password']") || []).forEach(($input) => {
      const passwordRegExp = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,50}$/;
      $input.addEventListener("input", () => {
        $passwordHelpText = $input.nextElementSibling
        if (!passwordRegExp.test($input.value)) {
          $passwordHelpText.classList.remove("is-hidden");
        }
        else {
          $passwordHelpText.classList.add("is-hidden");
        }
      })
    });
  
    (document.querySelectorAll(".navbar-burger") || []).forEach(($burger) => {
      $burger.addEventListener("click", () => {
        const target = $burger.dataset.target;
        const $target = document.getElementById(target);
  
        $burger.classList.toggle("is-active");
        $target.classList.toggle("is-active");
      })
    });
  });