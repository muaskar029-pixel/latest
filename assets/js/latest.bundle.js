(function () {
"use strict";
var live = document.createElement("p");
live.className = "visually-hidden";
live.setAttribute("aria-live", "polite");
document.body.appendChild(live);
function labelLoadMore() {
var next = document.querySelector('#pager a[rel="next"][hx-get]');
if (next) next.textContent = "Load more";
}
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
var first = items[countBefore].querySelector("h2 a, h3 a");
if (first) first.focus();
live.textContent = added + (added === 1 ? " more post loaded." : " more posts loaded.");
}
return;
}
if (target && target.tagName === "MAIN") {
var current = document.querySelector('.tab-grid a[aria-current="page"]');
if (current) current.focus();
labelLoadMore();
initHeroMedia();
initPostFilters();
}
});
function initHeroMedia() {
var media = document.querySelector(".hero-media");
if (!media || media.dataset.ready) return;
media.dataset.ready = "1";
var clips = Array.prototype.slice.call(media.querySelectorAll("video"));
var chip = media.querySelector(".hero-media__app");
var btn = media.querySelector(".hero-media__pause");
var track = document.querySelector(".hero-words__track");
var words = track ? track.querySelectorAll("span:not(.sep)") : [];
if (track) track.dataset.ready = "1";
var current = 0;
var paused = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
function play(v) {
if (!paused) {
var p = v.play();
if (p) p.catch(function () {});
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
clips[(current + 1) % clips.length].preload = "auto";
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
function initPostFilters() {
var form = document.querySelector(".post-search");
var list = document.getElementById("post-cards");
if (!form || !list || form.dataset.ready) return;
form.dataset.ready = "1";
var input = form.querySelector("input[type=search]");
var items = Array.prototype.slice.call(list.children);
var counts = {};
items.forEach(function (li) {
(li.dataset.tags || "").split(",").forEach(function (t) {
t = t.trim();
if (t) counts[t] = (counts[t] || 0) + 1;
});
});
var tags = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; }).slice(0, 6);
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
var text = (li.textContent + " " + (li.dataset.tags || "")).toLowerCase();
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
input.value = c.getAttribute("aria-pressed") === "true" ? "" : c.textContent;
filter();
});
});
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
(function (fn) {
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
else fn();
})(function () {
var navBtn = document.getElementById("about-menu-btn");
var dropdownContainer = document.querySelector(".dropdown");
var backBtn = document.querySelector(".d-content-back");
var isTouchDevice = ("ontouchstart" in window) || (navigator.maxTouchPoints > 0) || window.matchMedia("(pointer: coarse)").matches;
function closeDropdown() {
if (!navBtn) return;
navBtn.classList.remove("active");
navBtn.setAttribute("aria-expanded", "false");
if (document.activeElement && dropdownContainer && dropdownContainer.contains(document.activeElement)) {
document.activeElement.blur();
}
}
if (navBtn && dropdownContainer) {
if (isTouchDevice) {
navBtn.addEventListener("click", function (e) {
e.preventDefault();
var open = navBtn.classList.toggle("active");
navBtn.setAttribute("aria-expanded", String(open));
});
document.addEventListener("click", function (e) {
if (!dropdownContainer.contains(e.target)) closeDropdown();
});
} else {
dropdownContainer.addEventListener("mouseenter", function () {
navBtn.classList.add("active");
navBtn.setAttribute("aria-expanded", "true");
});
dropdownContainer.addEventListener("mouseleave", closeDropdown);
navBtn.addEventListener("click", function (e) {
e.preventDefault();
var open = navBtn.classList.toggle("active");
navBtn.setAttribute("aria-expanded", String(open));
});
}
if (backBtn) {
backBtn.addEventListener("click", function (e) {
e.preventDefault();
closeDropdown();
});
}
document.addEventListener("keydown", function (e) {
if (e.key === "Escape") closeDropdown();
});
}
var toggleBtn = document.querySelector(".nav-toggle");
var primaryNav = document.getElementById("primary-nav");
if (!toggleBtn || !primaryNav) return;
function setMenuState(open) {
toggleBtn.setAttribute("aria-expanded", String(open));
toggleBtn.setAttribute("aria-label", open ? "Tutup menu navigasi" : "Buka menu navigasi");
primaryNav.classList.toggle("is-open", open);
document.body.style.overflow = open ? "hidden" : "";
}
toggleBtn.addEventListener("click", function (e) {
e.stopPropagation();
setMenuState(toggleBtn.getAttribute("aria-expanded") !== "true");
});
primaryNav.querySelectorAll("a").forEach(function (link) {
link.addEventListener("click", function () { setMenuState(false); });
});
document.addEventListener("click", function (e) {
if (!primaryNav.contains(e.target) && !toggleBtn.contains(e.target)) {
setMenuState(false);
}
});
window.addEventListener("resize", function () {
if (window.innerWidth >= 768) setMenuState(false);
});
var langBtn = document.getElementById("lang-toggle");
if (langBtn) {
var LANG_KEY = "radova-lang";
var ID_TEXT = {
"skip": "Langsung ke konten",
"nav.packages": "Paket",
"nav.wiki": "Wiki",
"nav.learning": "Belajar",
"nav.events": "Acara",
"nav.latest": "Terbaru",
"nav.about": "Tentang",
"nav.history": "Sejarah",
"nav.contact": "Kontak",
"nav.back": "Kembali",
"latest.eyebrow": "[Pembaruan Radova]",
"latest.title": "Baca Pembaruan Terbaru Kami",
"latest.desc": "Acara, artikel, berita, dan informasi keamanan dari Radova Linux, diurutkan dari yang terbaru.",
"latest.all": "Semua Terbaru",
"latest.agenda": "Agenda",
"latest.article": "Artikel",
"latest.news": "Berita",
"latest.security": "Keamanan",
"footer.col1": "Tentang Radova",
"footer.col2": "Sumber Daya",
"footer.col3": "Pilar Utama",
"footer.col4": "Bantuan & Spesifikasi",
"footer.download": "Unduh ISO",
"footer.specs": "Kebutuhan Sistem",
"footer.security": "Info Keamanan",
"footer.copy": "© 2026 yuros.org · Dirilis di bawah Lisensi MIT",
"footer.top": "Ke atas ↑",
"agenda.desc": "Acara dan sesi komunitas Radova yang akan datang dan yang sudah lewat. Semua waktu dalam WIB (UTC+07:00).",
"article.desc": "Artikel mendalam tentang cara Radova Linux dibangun dan pemikiran di baliknya.",
"news.desc": "Pengumuman, rilis, dan kabar proyek dari tim Radova.",
"security.desc": "Informasi keamanan Radova Linux, lengkap dengan tingkat keparahan, versi terdampak, dan cara tetap aman.",
"404.title": "Halaman tidak ditemukan",
"404.desc": "Halaman ini tidak ada atau sudah dipindahkan."
};
var nodes = [];
function snapshotNodes() {
nodes = Array.prototype.slice.call(document.querySelectorAll("[data-i18n], [data-i18n-prefix]"));
nodes.forEach(function (node) {
if ("en" in node.dataset) return;
node.dataset.en = node.hasAttribute("data-i18n")
? node.textContent
: (node.firstChild ? node.firstChild.nodeValue : "");
});
}
function applyLang(lang) {
nodes.forEach(function (el) {
if (el.hasAttribute("data-i18n")) {
var key = el.getAttribute("data-i18n");
el.textContent = lang === "id" && ID_TEXT[key] != null ? ID_TEXT[key] : el.dataset.en;
} else if (el.firstChild) {
var pkey = el.getAttribute("data-i18n-prefix");
el.firstChild.nodeValue = lang === "id" && ID_TEXT[pkey] != null ? ID_TEXT[pkey] + " " : el.dataset.en;
}
});
document.documentElement.lang = lang;
langBtn.textContent = lang.toUpperCase();
langBtn.setAttribute("aria-label", lang === "id" ? "Switch language to English" : "Switch language to Indonesian");
}
snapshotNodes();
var currentLang = "en";
try {
var saved = localStorage.getItem(LANG_KEY);
if (saved === "id" || saved === "en") currentLang = saved;
} catch (_) {}
if (currentLang !== "en") applyLang(currentLang);
langBtn.addEventListener("click", function () {
currentLang = currentLang === "en" ? "id" : "en";
applyLang(currentLang);
try {
localStorage.setItem(LANG_KEY, currentLang);
} catch (_) {}
});
document.addEventListener("htmx:afterSettle", function () {
snapshotNodes();
if (currentLang !== "en") applyLang(currentLang);
});
}
});
(function () {
"use strict";
var THEME_KEY = "radova-theme";
var SUN_SVG = '<svg width="16" height="16" viewBox="0 0 256 256" fill="none" stroke="currentColor" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="128" cy="128" r="56"/><line x1="128" y1="36" x2="128" y2="16"/><line x1="128" y1="240" x2="128" y2="220"/><line x1="36" y1="128" x2="16" y2="128"/><line x1="240" y1="128" x2="220" y2="128"/><line x1="63" y1="63" x2="49" y2="49"/><line x1="207" y1="207" x2="193" y2="193"/><line x1="193" y1="63" x2="207" y2="49"/><line x1="49" y1="207" x2="63" y2="193"/></svg>';
var MOON_SVG = '<svg width="16" height="16" viewBox="0 0 256 256" fill="none" stroke="currentColor" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M216.7 152.6A91.9 91.9 0 0 1 103.4 39.3a92 92 0 1 0 113.3 113.3Z"/></svg>';
function applyTheme(theme) {
var isDark = theme === "dark";
document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
try { localStorage.setItem(THEME_KEY, isDark ? "dark" : "light"); } catch (_) {}
var btn = document.getElementById("theme-toggle");
if (!btn) return;
btn.setAttribute("aria-pressed", String(isDark));
btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
btn.setAttribute("title", isDark ? "Switch to light mode" : "Switch to dark mode");
btn.innerHTML = isDark ? SUN_SVG : MOON_SVG;
}
var saved = "light";
try { if (localStorage.getItem(THEME_KEY) === "dark") saved = "dark"; } catch (_) {}
applyTheme(saved);
document.addEventListener("click", function (e) {
if (!e.target.closest || !e.target.closest("#theme-toggle")) return;
applyTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
});
})();
