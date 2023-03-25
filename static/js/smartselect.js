$(document).ready(function () {
  for (let i = 1; i < 9; i++) {
    $("#semestar-select-" + i).on("change", function (a) {
      var val = $(this).find(":selected").val();

      $("#predmet-select-" + i + " > option").each(function () {
        sem = $(this).attr("semestar");
        if (sem != val) $(this).hide();
        else $(this).show();
      });
    });

    $("#predmet-select-" + i).on("change", function (e) {
      var selected = $(this).find(":selected");
      var sem = $(selected).attr("semestar");
      var bod = $(selected).attr("ects");
      var OI = $(selected).attr("obavezan");
      $("#semestar-select-" + i).val(sem);
      $("#ects-bodovi-" + i).text(bod);
      $("#oi-select-" + i).val(OI);
      calculate_ects();
    });
  }
});

function calculate_ects() {
  var sum = 0;
  for (let i = 1; i < 9; i++) sum += parseInt($("#ects-bodovi-" + i).text());

  $("#ects-ukupno").text(sum);
}
