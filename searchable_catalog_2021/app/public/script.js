import { html, render } from "https://unpkg.com/lit-html@1.3.0?module";
import { repeat } from "https://unpkg.com/lit-html@1.3.0/directives/repeat.js?module";
import Fuse from "https://cdn.jsdelivr.net/npm/fuse.js@6.4.1/dist/fuse.esm.js";
import debounce from "https://cdn.jsdelivr.net/npm/lodash-es@4.17.15/debounce.js";

function displayError(msg) {
  let m;
  if (!msg) {
    m = "";
  } else {
    m = msg;
  }
  document.getElementById("error").textContent = m;
}

let courseTemplate = (course) => {
  // console.log(course);
  return html`<div>
    <h3>${course.label + " " + course.title}</h3>
    ${course.offered ? "" : html`<sup>Not offered this year.</sup>`}
    <div><strong>Units:</strong> ${course.units}</div>
    <div><strong>Terms:</strong> ${course.terms}</div>
    <div><strong>Instructors:</strong> ${course.instructors}</div>
    <div><strong>Prerequisites:</strong> ${course.prerequisites}</div>
    <div>
      <strong>Description:</strong>
      ${course.description}
    </div>
  </div>`;
};

let coursesTemplate = (courses) => html`<section class="course-list">
  ${repeat(
    courses,
    (course) => course.unique_id,
    (course) => courseTemplate(course.item)
  )}
</section>`;

function renderResults(element, courses) {
  render(coursesTemplate(courses), element);
}

// prevent form submission
document.getElementById("gen-form").addEventListener("submit", (e) => {
  e.preventDefault();
});

fetch("./data.json")
  .then((resp) => resp.json())
  .then((data) => {
    // add unique key items for faster lit HTML
    for (let i = 0; i < data.length; i++) {
      data[i].unique_id = i;
    }
    let fuse = new Fuse(data, {
      isCaseSensitive: false,
      includeScore: false,
      shouldSort: true,
      keys: [
        {
          name: "label",
          weight: 150,
        },
        {
          name: "title",
          weight: 90,
        },
        {
          name: "units",
          weight: 5,
        },
        {
          name: "terms",
          weight: 5,
        },
        {
          name: "instructors",
          weight: 20,
        },
        {
          name: "description",
          weight: 30,
        },
      ],
      ignoreLocation: true,
    });
    let query_input = document.getElementById("input-info");
    query_input.addEventListener(
      "input",
      debounce((evt) => {
        displayError(null);
        // grab code and render
        let pattern = query_input.value;
        if (!pattern) {
          renderResults(document.getElementById("render"), []);
          return;
        }
        let courses = fuse.search(pattern, { limit: 20 });
        if (courses.length < 1) {
          displayError("Couldn't find a matching course.");
        }
        renderResults(document.getElementById("render"), courses);
      }, 50)
    );
  });
