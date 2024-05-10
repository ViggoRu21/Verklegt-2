document.getElementById("Page_Container").onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.getElementById("Page_Container").scrollTop > 80 || document.documentElement.scrollTop > 80) {
    document.getElementById("searchbar").style.width = "100%";
    document.getElementById("searchbar").style.height = "1em";
  } else {
    document.getElementById("searchbar").style.width = "10em";
    document.getElementById("searchbar").style.height = "";
  }
}

document.getElementById("test").addEventListener("click", testFunction);
function testFunction() {
  if (document.getElementById("test").style.color === "green") {
    document.getElementById("test").style.color = "#f8fafc"
  } else {
    document.getElementById("test").style.color = "green"
  }
}


