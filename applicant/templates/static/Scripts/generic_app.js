document.getElementById("Page_Container").onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.getElementById("Page_Container").scrollTop > 120 || document.documentElement.scrollTop > 120) {
    document.getElementById("search_container").style.width = "100%";
    document.getElementById("search_bar").style.height = "2.2em";
  } else {
    document.getElementById("search_container").style.width = "160px";
    document.getElementById("search_bar").style.height = "";
  }
}

document.getElementById("navbar_container").addEventListener("click", navCollapse);
function navCollapse() {
  if (document.getElementById("nav_transparent").style.visibility === "hidden" ){
    document.getElementById("nav_transparent").style.visibility = "visible";
  } else {
    document.getElementById("nav_transparent").style.visibility = "hidden";
  }
}

function profileHover() {
  document.getElementById("profile_nav").style.visibility = "visible";
}

function profileUnHover() {
  document.getElementById("profile_nav").style.visibility = "hidden";
}

document.getElementById("test").addEventListener("click", testFunction);
function testFunction() {
  if (document.getElementById("test").style.color === "green") {
    document.getElementById("test").style.color = "#f8fafc";
  } else {
    document.getElementById("test").style.color = "green";
  }
}
