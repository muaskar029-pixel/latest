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
    }
  });

  labelLoadMore();
})();
