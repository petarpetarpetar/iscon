$(document).ready(function () {
  submit_status_1 = window.localStorage.getItem("submit_status_1");
  submit_status_2 = window.localStorage.getItem("submit_status_2");
  submit_status_3 = window.localStorage.getItem("submit_status_3");

  ects_score = window.localStorage.getItem("ects-ukupno");

  console.log(submit_status_1);
  console.log(submit_status_2);
  console.log(submit_status_3);

  if (submit_status_1 === "filled") {
    $("#list1").attr("class", "btn btn-success stretched-link");
    $("#list1").text("Попуњено");
  }
  if (submit_status_2 === "filled") {
    $("#list2").attr("class", "btn btn-success stretched-link");
    $("#list2").text("Попуњено");
  }
  if (submit_status_3 === "filled") {
    $("#list3").attr("class", "btn btn-success stretched-link");
    $("#list3").text("Попуњено");
  }

  $("#btn_finalize").click(function () {
    if (submit_status_1 && submit_status_2 && submit_status_3) {
      window.localStorage.setItem("submit_status_1", false);
      window.localStorage.setItem("submit_status_2", false);
      window.localStorage.setItem("submit_status_3", false);

      ects_score = window.localStorage.getItem("ects_score");

      if (ects_score < 15) {
        alert("Nedovoljno Bodova!");
        return;
      }
      const xhr = new XMLHttpRequest();
      xhr.withCredentials = true;
      xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
          console.log(this.responseText);
          if (this.status === 200) {
            location.replace(`/studentProfil`);
          } else if (this.status === 401) {
            alert(JSON.parse(this.response)["Message"]);
          }
        }
      });

      xhr.open("POST", `/nextSemester`);
      xhr.setRequestHeader("Content-Type", "application/json");
      data = JSON.stringify({
        ects: ects_score,
      });

      xhr.send(data);
    } else {
      alert("Nekompletna dokumentacija.");
    }
  });
});
