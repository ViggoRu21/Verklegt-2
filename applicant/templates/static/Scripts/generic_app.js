document.getElementById("Page_Container").onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.getElementById("Page_Container").scrollTop > 120 || document.documentElement.scrollTop > 120) {
    document.getElementById("search_container").style.width = "100%";
    document.getElementById("searchbar").style.height = "2.2em";
  } else {
    document.getElementById("search_container").style.width = "160px";
    document.getElementById("searchbar").style.height = "";
  }
}

document.getElementById("navbar_container").addEventListener("click", navCollapse);
function navCollapse() {
  if (document.getElementById("nav_transparent").style.visibility !== "hidden" ){
    document.getElementById("nav_transparent").style.visibility = "hidden";
  } else {
    document.getElementById("nav_transparent").style.visibility = "visible";
  }
}

document.getElementById("test").addEventListener("click", testFunction);
function testFunction() {
  if (document.getElementById("test").style.color === "green") {
    document.getElementById("test").style.color = "#f8fafc";
  } else {
    document.getElementById("test").style.color = "green";
  }
}
