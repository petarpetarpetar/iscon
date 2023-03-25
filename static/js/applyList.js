$(document).ready(function () {
  $("#btn_save_page3").on("click", function () {
    window.localStorage.setItem("submit_status_3", "filled");
    location.replace(`/applyMenu`);
  });
});
