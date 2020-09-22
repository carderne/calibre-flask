/* global books debug */

const get = document.getElementById.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const create = function (
  element,
  parent,
  properties = {},
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
let elSize = get("size");
let elFilter = get("filter");
let elClear = get("clear");

function loadBooks() {
  let booksUse = debug ? books.slice(0, 50) : books;
  booksUse.forEach((b) => {
    let single = create("div", divBooks, [], "", ["single"]);

    let cover = create("div", single);
    let a = create("a", cover, { href: b.file });
    let pic = create("picture", a);
    create("source", pic, {
      srcset: b.hasCover ? b.coverSmall : "static/cover.jpg",
      media: "(max-width: 100px)",
    });
    create("img", pic, {
      src: b.hasCover ? b.cover : "static/cover.jpg",
      alt: "cover",
      loading: "lazy",
    });

    let details = create("div", single);
    create("div", details, [], b.title, ["title"]);
    create("div", details, [], b.author, ["author"]);
    create("div", details, [], b.sort, ["hidden"]);
    create("div", details, [], b.authorSort, ["hidden"]);
    create("div", details, [], b.added, ["hidden"]);

    let desc = b.description;
    desc = desc.length > 400 ? desc.substring(0, 400) + "..." : desc;
    create("div", details, [], desc, ["description"]);
  });
}

elView.onchange = updateView;
function updateView() {
  if (elView.value == "list") {
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
  [...divBooks.children]
    .sort((a, b) =>
      a.children[1].children[index].innerText >
      b.children[1].children[index].innerText
        ? order
        : -order
    )
    .forEach((node) => divBooks.appendChild(node));
}

elSize.oninput = updateSize;
function updateSize() {
  let size = elSize.value;
  queryAll(".single").forEach((single) => {
    single.style.width = size + "px";
    single.children[0].style.width = size + "px";
  });
}

elFilter.oninput = updateFilter;
function updateFilter() {
  let text = elFilter.value.toLowerCase();
  if (text.length > 3) {
    [...divBooks.children].forEach((single) => {
      let nodes = [
        single.children[1].children[0],
        single.children[1].children[1],
        single.children[1].children[5],
      ];
      if (nodes.some((node) => node.innerText.toLowerCase().includes(text))) {
        single.removeAttribute("style");
        let re = new RegExp(text, "ig");
        nodes.forEach((node) => {
          node.innerHTML = node.innerText.replace(
            re,
            "<span class='hl'>$&</span>"
          );
        });
      } else {
        single.style.display = "none";
      }
    });
  } else {
    [...divBooks.children].forEach((single) => {
      single.removeAttribute("style");
    });
    queryAll(".hl").forEach((node) => {
      node.parentElement.replaceChild(
        document.createTextNode(node.innerText),
        node
      );
    });
  }
}

elClear.onclick = clearFilter;
function clearFilter() {
  elFilter.value = "";
  updateFilter();
}

document.addEventListener("DOMContentLoaded", function () {
  loadBooks();
  updateView();
  updateSort();
  updateSize();
  updateFilter();
});
