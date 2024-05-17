addEventListener("scroll", (event) => {
    if (document.documentElement.scrollTop > 170) {
        document.getElementById("search_container").style.position = "fixed";
        document.getElementById("search_container").style.width = "90%";
        document.getElementById("search_container").style.top = "0";

    } else {
        document.getElementById("search_container").style.top = '';
        document.getElementById("search_container").style.width = "100%";
        document.getElementById("search_container").style.position = "relative";
    }});



function navCollapse() {

  if (document.getElementById("nav_transparent").className === "nav_transparent" ){
    document.getElementById("navbar_container").style.marginTop = "0.7rem";
    document.getElementById("nav_transparent").className = "nav";
    document.getElementById("nav_img").src = nav2;
  } else {
    document.getElementById("nav_transparent").className = "nav_transparent";
    document.getElementById("navbar_container").style.marginTop = "0.5rem";
    document.getElementById("nav_img").src = nav1;
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
  if (x.className === "sub_title") {
    x.className = "sub_title_green";
  } else {
    x.className = "sub_title";
  }
}


document.getElementById("bigSearch").onchange = function () {
    let elems = ["search-right-1", "search-right-2", "search-right-5",
                      "search-right-6", "search-right-7"];
    for (i in elems) {
      document.getElementById(elems[i]).className = 'search_hide';
    }
    document.getElementById(this[this.selectedIndex].value).className = 'search_show';
};


document.getElementById("bigSelect").onchange = function () {
    let x = document.getElementById("search-right-3");
    let y = document.getElementById("search-right-4");
    if (x.className === "search_show") {
        x.className = 'search_hide';
        y.className = 'search_show';
    } else {
        y.className = 'search_hide';
        x.className = 'search_show';
    }
};