// mermaid-init.js
(function () {
  var s = document.createElement("script");
  s.src = "https://cdn.jsdelivr.net/npm/mermaid@11.10.0/dist/mermaid.min.js";
  s.onload = function() {
    mermaid.initialize({
      startOnLoad: true,
      theme: "default",
      themeCSS: `
        .node text {
          text-anchor: middle;
          dominant-baseline: middle;
        }
      `
    });
  };
  document.head.appendChild(s);
})();
