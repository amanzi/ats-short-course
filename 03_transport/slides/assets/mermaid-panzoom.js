(function () {
  // load mermaid
  var s1 = document.createElement("script");
  s1.src = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";
  document.head.appendChild(s1);

  // load panzoom
  var s2 = document.createElement("script");
  s2.src = "https://cdn.jsdelivr.net/npm/@panzoom/panzoom/dist/panzoom.min.js";
  document.head.appendChild(s2);

  // once both scripts are ready
  s2.onload = function () {
    mermaid.initialize({ startOnLoad: false });

    document.addEventListener("DOMContentLoaded", function () {
      mermaid.run({
        querySelector: ".mermaid",
        postRenderCallback: (id) => {
          const container = document.getElementById("diagram-container");
          const svgElement = container.querySelector("svg");

          const panzoomInstance = Panzoom(svgElement, {
            maxScale: 5,
            minScale: 0.5,
            step: 0.1,
          });

          // wheel zoom
          container.addEventListener("wheel", (event) => {
            panzoomInstance.zoomWithWheel(event);
          });
        },
      });
    });
  };
})();
