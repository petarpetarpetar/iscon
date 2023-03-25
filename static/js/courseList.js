$(document).ready(function () {
  $("#btn_save_page1").on("click", function () {
    window.localStorage.setItem("submit_status_1", "filled");
    window.localStorage.setItem("submit_ects", $("#ects-ukupno").text());
    location.replace(`/applyMenu`);
  });
});
