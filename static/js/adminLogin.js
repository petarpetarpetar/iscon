function onClickLoginHandler() {
  var id = document.getElementById("typeEmailX-2").value;
  var password = document.getElementById("typePasswordX-2").value;

  const xhr = new XMLHttpRequest();
  xhr.withCredentials = true;
  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      console.log(this.responseText);
      if (this.status === 200) {
        location.replace(`/adminLogin`);
      } else if (this.status === 401) {
        alert(JSON.parse(this.response)["message"]);
      }
    }
  });

  xhr.open("POST", `/adminLogin`);
  xhr.setRequestHeader("Content-Type", "application/json");
  data = JSON.stringify({
    id: id,
    password: password,
  });

  xhr.send(data);
  // location.href = 'http://192.168.137.80:5000/login'
}

function logout() {
  const xhr = new XMLHttpRequest();
  xhr.withCredentials = true;
  xhr.addEventListener("readystatechange", function () {
    if (this.readyState === this.DONE) {
      console.log(this.responseText);
      if (this.status === 200) {
        location.replace(`/adminProfile`);
      } else if (this.status === 401) {
        alert(JSON.parse(this.response)["message"]);
      }
    }
  });

  xhr.open("DELETE", `/adminLogin`);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.send();
  // location.href = 'http://192.168.137.80:5000/login'
}
