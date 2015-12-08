var main = function() {
  function res(note) {
    $("#n" + note).removeClass('show');
    $("#b" + note).removeClass('show');
    $("#t" + note).removeClass('show');
    $("#n" + note).animate({left: '0%'}, 0);
    dance(note);
  };

  function dance(note) {
    var pitch = Math.floor(9 * Math.random())
    var line = pitch * 10;
    $("#n" + note).animate({top: "-" + line + "px"}, 0);
    $("#n" + note).addClass('show');
    if (pitch >= 4) {
      $("#b" + note).addClass('show');
    } else {
      $("#t" + note).addClass('show');
    }
    $("#n" + note).animate({left: '100%'}, 7000, "linear");
    /*setTimeout(function() {
      var notefile = new Audio("note" + pitch + ".mp3");
      notefile.play();
    }, 1750);*/
    setTimeout(function() {res(note);}, 7000);
  };
  dance("0");
  setTimeout(function() {dance("1")}, 1000);
  setTimeout(function() {dance("2")}, 2000);
  setTimeout(function() {dance("3")}, 3000);
  setTimeout(function() {dance("4")}, 4000);
  setTimeout(function() {dance("5")}, 5000);
  setTimeout(function() {dance("6")}, 6000);
};

$(document).ready(main);

function upload() {
	$('form').submit();
};

function ply(n) {
  var id = "n" + n;
  var spot = document.getElementById(id).style.marginTop;
	var notefile = new Audio("static/Actual Webfront/note" + n + ".mp3");
	notefile.play();
};