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
  if (x.style.color === "#10b981") {
    x.style.color = "";
  } else {
    x.style.color = "#10b981";
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

function test1Function() {
  let x = document.getElementById('test');
  x.addEventListener('click', (e) => {
    x.style.color.toggle("#10b981");
  })

}