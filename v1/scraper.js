// goto https://catalog.caltech.edu/current/cs

JSON.stringify(
  (() => {
    return Array.from(
      document.querySelectorAll("div.rich-text")[1].getElementsByTagName("p")
    ).map((e) => {
      console.log(e);
      return {
        title: e.getElementsByTagName("strong")[0].textContent,
        em0: e.getElementsByTagName("em")[0].textContent,
        em1: (e.getElementsByTagName("em")[1] || { textContent: null })
          .textContent,
        desc: e.lastChild.textContent,
      };
    });
  })()
);
