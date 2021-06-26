'use strict';


function readURL(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      $('#pro')
        .attr('src', e.target.result)
        .width(150)
        .height(150);
      $('#event')
        .attr('src', e.target.result)
        .width(200)
        .height(100);
    };
    reader.readAsDataURL(input.files[0]);
  }
}


function toggleShowHide() {
    const x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}


function toggleShowHidef() {
  const y = document.getElementById("old_pw");
  if (y.type === "password") {
      y.type = "text";
    } else {
      y.type = "password";
    }
}


function toggleRed() {
  document.getElementById("heart").style.color = "red";
}

function toggleBlue() {
  document.getElementById("thumb").style.color = "blue";
}