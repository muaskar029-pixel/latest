// Progressive enhancement for Radova Latest. Without JS every tab and pager link is a plain link.
// htmx does the requests and swaps; this file only handles focus, labels and announcements.
(function () {
  "use strict";

  // Screen-reader announcements for content that appears without a page load.
  var live = document.createElement("p");
  live.className = "visually-hidden";
  live.setAttribute("aria-live", "polite");
  document.body.appendChild(live);

  // With JS the enhanced Next link appends instead of navigating, so it says so.
  function labelLoadMore() {
    var next = document.querySelector('#pager a[rel="next"][hx-get]');
    if (next) next.textContent = "Load more";
  }

  // After "Load more" the swapped-in pager belongs to the page just appended:
  // drop its Previous link, and drop the whole bar once there is no next page.
  function tidyPager() {
    var pager = document.getElementById("pager");
    if (!pager) return;
    var prev = pager.querySelector('a[rel="prev"]');
    if (prev) prev.remove();
    if (!pager.querySelector('a[rel="next"]')) pager.remove();
  }

  var countBefore = 0;

  document.body.addEventListener("htmx:beforeRequest", function (e) {
    var list = document.getElementById("post-list");
    countBefore = list ? list.children.length : 0;
  });

  document.body.addEventListener("htmx:afterSettle", function (e) {
    var target = e.detail.target;

    if (target && target.id === "post-list") {
      var items = target.children;
      var added = items.length - countBefore;
      tidyPager();
      labelLoadMore();
      if (added > 0) {
        // Put keyboard focus on the first new post so reading continues where the new content starts.
        var first = items[countBefore].querySelector("h2 a, h3 a");
        if (first) first.focus();
        live.textContent = added + (added === 1 ? " more post loaded." : " more posts loaded.");
      }
      return;
    }

    // Tab switch (only the tabs target <main>): the tab that had focus was replaced, so focus the new current tab.
    if (target && target.tagName === "MAIN") {
      var current = document.querySelector('.tab-grid a[aria-current="page"]');
      if (current) current.focus();
      labelLoadMore();
      initHeroMedia(); // a fresh /latest/ <main> brings a fresh hero
      initPostFilters();
    }
  });

  // Index hero: play the app clips one after another; the chip and the h1 word follow the playing clip.
  // Without JS the first clip's poster stays. Reduced motion: stays still until the visitor presses play.
  function initHeroMedia() {
    var media = document.querySelector(".hero-media");
    if (!media || media.dataset.ready) return;
    media.dataset.ready = "1";
    var clips = Array.prototype.slice.call(media.querySelectorAll("video"));
    var chip = media.querySelector(".hero-media__app");
    var btn = media.querySelector(".hero-media__pause");
    var track = document.querySelector(".hero-words__track");
    var words = track ? track.querySelectorAll("span:not(.sep)") : []; // h1 words, one per clip, in clip order
    if (track) track.dataset.ready = "1"; // from now on, word changes animate
    var current = 0;
    var paused = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function play(v) {
      if (!paused) {
        var p = v.play();
        if (p) p.catch(function () {}); // a blocked autoplay just leaves the poster
      }
    }
    function show(n) {
      clips[current].classList.remove("is-active");
      clips[current].pause();
      current = n % clips.length;
      var v = clips[current];
      v.currentTime = 0;
      v.classList.add("is-active");
      chip.querySelector("strong").textContent = v.dataset.app;
      chip.querySelector("span").textContent = "for " + v.dataset.word;
      if (words[current]) {
        Array.prototype.forEach.call(words, function (w) { w.classList.remove("is-current", "is-previous"); });
        words[(current + words.length - 1) % words.length].classList.add("is-previous");
        words[current].classList.add("is-current");
      }
      clips[(current + 1) % clips.length].preload = "auto"; // warm up the next clip
      play(v);
    }
    function setPaused(p) {
      paused = p;
      btn.setAttribute("aria-pressed", String(p));
      btn.setAttribute("aria-label", p ? "Play video" : "Pause video");
      if (p) clips[current].pause();
      else play(clips[current]);
    }

    clips.forEach(function (v) {
      v.addEventListener("ended", function () { show(current + 1); });
    });
    btn.addEventListener("click", function () { setPaused(!paused); });
    btn.hidden = false;
    setPaused(paused);
  }

  // Header dropdowns are <details>: keep only one open, and close them on an outside click or Escape.
  function closeMenus(except) {
    document.querySelectorAll(".nav-menu[open]").forEach(function (menu) {
      if (menu !== except) menu.open = false;
    });
  }
  document.addEventListener("click", function (e) {
    closeMenus(e.target.closest ? e.target.closest(".nav-menu") : null);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var open = document.querySelector(".nav-menu[open]");
    if (!open) return;
    open.open = false;
    open.querySelector("summary").focus();
  });

  // Index search, "Popular" chips and sort: with JS they work on the cards on the page instead of leaving it.
  function initPostFilters() {
    var form = document.querySelector(".post-search");
    var list = document.getElementById("post-cards");
    if (!form || !list || form.dataset.ready) return;
    form.dataset.ready = "1";
    var input = form.querySelector("input[type=search]");
    var items = Array.prototype.slice.call(list.children);

    // The chips, the sort menu and the "no match" line only work with JS, so JS adds them:
    // Lynx and no-JS visitors never meet controls that do nothing.
    var counts = {};
    items.forEach(function (li) {
      (li.dataset.tags || "").split(",").forEach(function (t) {
        t = t.trim();
        if (t) counts[t] = (counts[t] || 0) + 1;
      });
    });
    var tags = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; }).slice(0, 6); // most used first
    var filters = el("div", "post-filters");
    var popular = el("p", "post-filters__popular");
    popular.appendChild(el("strong", "", "Popular:"));
    tags.forEach(function (t) {
      var b = el("button", "", t);
      b.type = "button";
      b.setAttribute("aria-pressed", "false");
      popular.appendChild(b);
    });
    var sortLabel = el("label", "visually-hidden", "Sort posts");
    sortLabel.htmlFor = "post-sort";
    var sort = el("select");
    sort.id = "post-sort";
    sort.setAttribute("aria-controls", "post-cards");
    sort.add(new Option("Newest first", "new"));
    sort.add(new Option("Oldest first", "old"));
    if (tags.length) filters.appendChild(popular);
    filters.appendChild(sortLabel);
    filters.appendChild(sort);
    var empty = el("p", "post-filters__empty", "No updates match your search.");
    empty.hidden = true;
    form.after(filters, empty);
    var chips = popular.querySelectorAll("button");

    function filter() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (li) {
        var text = (li.textContent + " " + (li.dataset.tags || "")).toLowerCase(); // card text plus its tags
        li.hidden = q !== "" && text.indexOf(q) === -1;
        if (!li.hidden) shown++;
      });
      Array.prototype.forEach.call(chips, function (c) {
        c.setAttribute("aria-pressed", String(c.textContent === q));
      });
      empty.hidden = shown > 0;
      live.textContent = q ? shown + (shown === 1 ? " update found." : " updates found.") : "";
    }
    form.addEventListener("submit", function (e) { e.preventDefault(); filter(); });
    input.addEventListener("input", filter);
    Array.prototype.forEach.call(chips, function (c) {
      c.addEventListener("click", function () {
        input.value = c.getAttribute("aria-pressed") === "true" ? "" : c.textContent; // a second click clears it
        filter();
      });
    });
    // Dated posts sort by date; status cards without a <time> stay at the end.
    sort.addEventListener("change", function (e) {
      var dir = e.target.value === "old" ? 1 : -1;
      function when(li) { var t = li.querySelector("time"); return t ? Date.parse(t.getAttribute("datetime")) : null; }
      items.slice().sort(function (a, b) {
        var x = when(a), y = when(b);
        if (x === null || y === null) return (x === null) - (y === null);
        return dir * (x - y);
      }).forEach(function (li) { list.appendChild(li); });
    });
  }

  function el(tag, className, text) {
    var e = document.createElement(tag);
    if (className) e.className = className;
    if (text) e.textContent = text;
    return e;
  }

  labelLoadMore();
  initHeroMedia();
  initPostFilters();
})();
