addEventListener("scroll", (event) => {
    if (document.documentElement.scrollTop > 170) {
        document.getElementById("search_container").style.position = "fixed";
        document.getElementById("search_container").style.width = "90%";
        document.getElementById("search_container").style.top = "0";

    } else {
        document.getElementById("search_container").style.top = '';
        document.getElementById("search_container").style.width = "80%";
        document.getElementById("search_container").style.position = "relative";
    }});





function navCollapse() {
  if (document.getElementById("nav_transparent").className === "nav_transparent" ){
    document.getElementById("nav_transparent").className = "nav";
  } else {
    document.getElementById("nav_transparent").className = "nav_transparent";
  }
}

function profileHover() {
  document.getElementById("profile_nav").style.visibility = "visible";
}

function profileUnHover() {
  document.getElementById("profile_nav").style.visibility = "hidden";
}

function testFunction() {
  let x = document.getElementById("test");
  if (x.className === "title") {
    x.className = "title_green";
  } else {
    x.className = "title";
  }
}

document.getElementById("bigSelect").onchange = function () {
    let elems = ["search-right-1", "search-right-2", "search-right-3",
                      "search-right-4", "search-right-5", "search-right-6",
                      "search-right-7", "search-right-8"];
    for (i in elems) {
      document.getElementById(elems[i]).className = 'search_hide';
    }
    document.getElementById(this[this.selectedIndex].value).className = 'search_show';
};
