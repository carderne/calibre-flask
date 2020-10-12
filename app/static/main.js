const get = document.getElementById.bind(document);
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);

let divBooks = query("main");
let elView = get("view");
let elSort = get("sort");
let elSize = get("size");
let elFilter = get("filter");
let elClear = get("clear");

elView.onchange = updateView;
function updateView() {
  divBooks.setAttribute("view", elView.value);
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
  query("main").setAttribute("size", size);
  let sizes = size == "small" ? "1vw" : "100vw";
  queryAll("img").forEach((img) => {
    img["sizes"] = sizes;
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
        single.style.display = "";
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
      single.style.display = "";
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
  let search = new URL(window.location.href).searchParams.get("s");
  if (search != null) {
    elFilter.value = search;
  }
  updateView();
  updateSort();
  updateSize();
  updateFilter();
});
