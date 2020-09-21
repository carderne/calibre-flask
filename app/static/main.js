/* global books */

const get = document.getElementById.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const create = function (
  element,
  parent,
  properties = [],
  text = "",
  classes = []
) {
  let el = document.createElement(element);
  el.textContent = text;
  parent.appendChild(el);
  classes.forEach((c) => {
    el.classList.add(c);
  });
  for (let prop in properties) {
    el[prop] = properties[prop];
  }
  return el;
};

let divBooks = get("books");
let elView = get("view");
let elSort = get("sort");

function loadBooks() {
  books.forEach((b) => {
    let single = create("div", divBooks, [], "", ["single"]);

    let cover = create("div", single);
    let src = b.hasCover ? b.coverSmall : "static/cover.jpg";
    create("img", cover, { src: src, alt: "cover", loading: "lazy" });

    let details = create("div", single);
    create("div", details, [], b.title, ["title"]);
    create("div", details, [], b.author, ["author"]);
    create("div", details, [], b.sort, ["hidden"]);
    create("div", details, [], b.authorSort, ["hidden"]);
    create("div", details, [], b.added, ["hidden"]);

    let dl = create("div", details);
    create("a", dl, { href: b.file }, "download");

    create("div", details, [], b.description, ["description"]);
  });
}

elView.onchange = updateView;
function updateView() {
  if (elView.checked) {
    get("books").classList.add("list");
    queryAll(".single").forEach((single) => {
      single.classList.add("wide");
    });
  } else {
    get("books").classList.remove("list");
    queryAll(".single").forEach((single) => {
      single.classList.remove("wide");
    });
  }
}

elSort.oninput = updateSort;
function updateSort() {
  let by = elSort.value;
  let indices = {
    author: 3,
    title: 2,
    added: 4,
  };
  let index = indices[by];
  let order = by == "added" ? -1 : 1;
  console.log(index);
  [...divBooks.children]
    .sort((a, b) =>
      a.children[1].children[index].innerText >
      b.children[1].children[index].innerText
        ? order
        : -order
    )
    .forEach((node) => divBooks.appendChild(node));
}

document.addEventListener("DOMContentLoaded", function () {
  loadBooks();
  updateView();
  updateSort();
});
