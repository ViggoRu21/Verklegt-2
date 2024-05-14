document.getElementById("Page_Container").onscroll = function() {scrollFunction()};
document.onload = function () {listingSearchBar()};

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

function testFunction() {
  let x = document.getElementById("test");
  if (x.style.color === "#10b981") {
    x.style.color = "";
  } else {
    x.style.color = "#10b981";
  }
}

function listingSearchBar() {
  let elems = ["search-right-1", "search-right-2", "search-right-3",
                        "search-right-4", "search-right-5", "search-right-6",
                        "search-right-7", "search-right-8"];
  let x = document.getElementById("bigSelect").value
  console.log(x);
  x.selectedIndex
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