const get = document.getElementById.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const create = function(element, parent, properties=[], text="", classes=[]) {
  let el = document.createElement(element);
  el.textContent = text;
  parent.appendChild(el);
  classes.forEach((c) => { el.classList.add(c) });
  for (let prop in properties) {
    el[prop] = properties[prop];
  }
  return el;
}

function loadBooks() {
  let divBooks = get("books");
  books.forEach((book) => {
    let single = create("div", divBooks, [], "", ["single"]);

    let cover = create("div", single);
    let src = book.hasCover ? book.cover : "static/cover.jpg";
    let img = create("img", cover, {"src": src, "alt": "cover", "loading": "lazy"});

    let details = create("div", single);
    let title = create("div", details, [], book.title, ["title"]);
    let author = create("div", details, [], book.author, ["author"]);

    let dl = create("div", details);
    let a = create("a", dl, {"href": book.file}, "download");

    let desc = create("div", details, [], book.description, ["description"]);
  });
}

get("list-view").onchange = updateView;
function updateView() {
  if (get("list-view").checked) {
    get("books").classList.add("list");
    queryAll(".single").forEach((single) => {
      single.classList.add("wide")
    });
  } else {
    get("books").classList.remove("list");
    queryAll(".single").forEach((single) => {
      single.classList.remove("wide")
    });
  }
}

document.addEventListener("DOMContentLoaded", function(){
  loadBooks();
  updateView();
});
