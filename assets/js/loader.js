// Loads what the first paint does not need on the first interaction, like the Homepage:
// css/fonts.css (until then the system font shows). Paths are relative to this file.
(function () {
  "use strict";
  var base = document.currentScript.src;
  var loaded = false;

  function load() {
    if (loaded) return;
    loaded = true;
    var fonts = document.createElement("link");
    fonts.rel = "stylesheet";
    fonts.href = new URL("../css/fonts.css", base).href;
    document.head.appendChild(fonts);
  }

  ["pointerdown", "keydown", "touchstart", "scroll"].forEach(function (type) {
    addEventListener(type, load, { once: true, passive: true });
  });
})();
