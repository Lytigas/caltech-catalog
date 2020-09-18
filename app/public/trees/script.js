function displayError(msg) {
  let m;
  if (!msg) {
    m = "";
  } else {
    m = "Error: " + msg;
  }
  document.getElementById("error").textContent = m;
}

function displayInfo(msg) {
  let m;
  if (!msg) {
    m = "";
  } else {
    m = "Info: " + msg;
  }
  document.getElementById("error").textContent = m;
}

function canonicalize(index, user_input) {
  // im lazy so delegate this to Fuse JS
  let codes = Object.keys(index);
  let fuse = new Fuse(codes, {});
  let results = fuse.search(user_input);
  if (results.length < 1) {
    displayError("No matching courses found.");
    return null;
  }
  return results[0].item;
}

function renderGraph(index, course_code) {
  let dotsafe = (identifier) =>
    identifier.replace(/ /g, "_").replace(/\//g, "_");
  let dfs = (course_code, index, dot_lines, seen_set) => {
    seen_set.add(course_code);
    dot_lines.push(dotsafe(course_code));
    index[course_code].c_prereq.forEach((pr_code) => {
      dot_lines.push(dotsafe(course_code) + " -> " + dotsafe(pr_code));
      if (!seen_set.has(pr_code)) {
        dfs(pr_code, index, dot_lines, seen_set);
      }
    });
  };
  dot_lines = [];
  dfs(course_code, index, dot_lines, new Set());
  dot_source = "strict digraph {\nrankdir=LR;\n";
  dot_lines.forEach((line) => {
    dot_source += line;
    dot_source += "\n";
  });
  dot_source += "}\n";
  console.log(dot_source);
  d3.select("#render").graphviz().renderDot(dot_source);
}

// prevent form submission
document.getElementById("gen-form").addEventListener("submit", (e) => {
  e.preventDefault();
});

fetch("./data.json")
  .then((resp) => resp.json())
  .then((data) => {
    // build index
    let index = {};
    data.forEach((course) => {
      index[course.code] = course;
    });
    document.getElementById("gen-form").addEventListener("submit", (evt) => {
      // clear last time
      document.getElementById("render").innerHTML = "";
      displayError(null);
      displayInfo(null);
      // grab code and render
      let inp_code = evt.target.elements["code"].value;
      let code = canonicalize(index, inp_code);
      if (!code) {
        displayError("Could not find a matching course.");
        return;
      }
      displayInfo("Fuzzy-matched query to course " + code + ".");
      renderGraph(index, code);
    });
  });
