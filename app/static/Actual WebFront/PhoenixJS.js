var main = function() {
  function res(note) {
    $("#" + note).removeClass('show');
    $("#" + note).animate({left: '0%'}, 0);
    dance(note);
  };

  function dance(note) {
    var pitch = Math.floor(9 * Math.random())
    var line = pitch * 10;
    $("#" + note).animate({top: "-" + line + "px"}, 0);
    $("#" + note).addClass('show');
    $("#" + note).animate({left: '100%'}, 3500, "linear");
    setTimeout(function() {
      var notefile = new Audio("static/Actual WebFront/note" + pitch + ".mp3");
      notefile.play();
    }, 1750);
    setTimeout(function() {res(note);}, 3500);
  };
  dance("n0");
  setTimeout(function() {dance("n1")}, 500);
  setTimeout(function() {dance("n2")}, 1000);
  setTimeout(function() {dance("n3")}, 1500);
  setTimeout(function() {dance("n4")}, 2000);
  setTimeout(function() {dance("n5")}, 2500);
  setTimeout(function() {dance("n6")}, 3000);
};

$(document).ready(main);

function upload() {
	var file = document.getElementById("FileUpload").value;
	alert("File: " + file);
};

function ply(n) {
  var id = "n" + n;
  var spot = document.getElementById(id).style.marginTop;
	var notefile = new Audio("static/Actual WebFront/note" + n + ".mp3");
	notefile.play();
};