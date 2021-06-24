'use strict';


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