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

document.getElementById("navbar").onclick = function() {navcollaps()};
function navcollaps() {
  // Get the checkbox
  let checkBox = document.getElementById("navbar");
  // Get the output text

  // If the checkbox is checked, display the output text
  if (checkBox = document.getElementById("navbar").checked == true){
    document.getElementById("sidebar-nav").style.maxHeight = "100%";
    document.getElementById("sidebar-nav").style.display = visible;
    
  } else {
    document.getElementById("sidebar-nav").style.maxHeight = 0;
    document.getElementById("sidebar-nav").style.display = hidden;
  }
}

