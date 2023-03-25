$(document).ready(function () {
  $("#btn_save_page2").on("click", function () {
    window.localStorage.setItem("submit_status_2", "filled");
    location.replace(`/applyMenu`);
  });
});
