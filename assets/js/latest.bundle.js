(function () {
"use strict";
var live = Object.assign(document.createElement("p"), { className: "visually-hidden" });
live.setAttribute("aria-live", "polite");
document.body.appendChild(live);
var THEME_KEY = "radova-theme";
var LANG_KEY = "radova-lang";
var SUN_SVG = '<svg width="16" height="16" viewBox="0 0 256 256" fill="none" stroke="currentColor" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="128" cy="128" r="56"/><line x1="128" y1="36" x2="128" y2="16"/><line x1="128" y1="240" x2="128" y2="220"/><line x1="36" y1="128" x2="16" y2="128"/><line x1="240" y1="128" x2="220" y2="128"/><line x1="63" y1="63" x2="49" y2="49"/><line x1="207" y1="207" x2="193" y2="193"/><line x1="193" y1="63" x2="207" y2="49"/><line x1="49" y1="207" x2="63" y2="193"/></svg>';
var MOON_SVG = '<svg width="16" height="16" viewBox="0 0 256 256" fill="none" stroke="currentColor" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M216.7 152.6A91.9 91.9 0 0 1 103.4 39.3a92 92 0 1 0 113.3 113.3Z"/></svg>';
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
"404.desc": "Halaman ini tidak ada atau sudah dipindahkan.",
"404.cta": "Lihat pembaruan terbaru",
"latest.notice": "Menemukan celah keamanan? Laporkan secara privat.",
"latest.noticeCta": "Baca kebijakan",
"latest.heroChip": "Radova Terbaru",
"latest.heroTitle": "Satu sistem untuk setiap",
"latest.c1": "Acara dan sesi komunitas",
"latest.c2": "Artikel dan berita dari tim",
"latest.c3": "Semua info keamanan, di satu tempat",
"latest.browse": "Lihat semua pembaruan",
"latest.searchPh": "Cari pembaruan",
"latest.emptyAgenda": "Belum ada acara.",
"latest.goAgenda": "Buka Agenda",
"latest.emptySecurity": "Belum ada info keamanan.",
"latest.goSecurity": "Buka Keamanan"
};
function syncPager(tidy) {
var pager = document.getElementById("pager");
if (!pager) return;
if (tidy) {
var prev = pager.querySelector('a[rel="prev"]');
if (prev) prev.remove();
if (!pager.querySelector('a[rel="next"]')) return pager.remove();
}
var next = pager.querySelector('a[rel="next"][hx-get]');
if (next) next.textContent = "Load more";
}
function initHeroMedia() {
var media = document.querySelector(".hero-media");
if (!media || media.dataset.ready) return;
media.dataset.ready = "1";
var clips = [].slice.call(media.querySelectorAll("video"));
var chip = media.querySelector(".hero-media__app");
var btn = media.querySelector(".hero-media__pause");
var track = document.querySelector(".hero-words__track");
var words = track ? track.querySelectorAll("span:not(.sep)") : [];
if (track) track.dataset.ready = "1";
var cur = 0;
var paused = matchMedia("(prefers-reduced-motion: reduce)").matches;
function play(v) {
if (paused) return;
var p = v.play();
if (p) p.catch(function () {});
}
function show(n) {
clips[cur].classList.remove("is-active");
clips[cur].pause();
cur = n % clips.length;
var v = clips[cur];
v.currentTime = 0;
v.classList.add("is-active");
chip.querySelector("strong").textContent = v.dataset.app;
chip.querySelector("span").textContent = "for " + v.dataset.word;
if (words[cur]) {
[].forEach.call(words, function (w) { w.classList.remove("is-current", "is-previous"); });
words[(cur + words.length - 1) % words.length].classList.add("is-previous");
words[cur].classList.add("is-current");
}
clips[(cur + 1) % clips.length].preload = "auto";
play(v);
}
function setPaused(p) {
paused = p;
btn.setAttribute("aria-pressed", String(p));
btn.setAttribute("aria-label", p ? "Play video" : "Pause video");
if (p) clips[cur].pause(); else play(clips[cur]);
}
clips.forEach(function (v) {
if (v.dataset.poster) v.poster = v.dataset.poster;
v.addEventListener("ended", function () { show(cur + 1); });
});
btn.addEventListener("click", function () { setPaused(!paused); });
btn.hidden = false;
setPaused(paused);
}
function initPostFilters() {
var form = document.querySelector(".post-search");
var list = document.getElementById("post-cards");
if (!form || !list || form.dataset.ready) return;
form.dataset.ready = "1";
var input = form.querySelector("input[type=search]");
var items = [].slice.call(list.children);
var counts = {};
items.forEach(function (li) {
(li.dataset.tags || "").split(",").forEach(function (t) {
t = t.trim();
if (t) counts[t] = (counts[t] || 0) + 1;
});
});
var tags = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; }).slice(0, 6);
var filters = Object.assign(document.createElement("div"), { className: "post-filters" });
var popular = Object.assign(document.createElement("p"), { className: "post-filters__popular" });
if (tags.length) {
popular.appendChild(Object.assign(document.createElement("strong"), { textContent: "Popular:" }));
tags.forEach(function (t) {
var b = Object.assign(document.createElement("button"), { type: "button", textContent: t });
b.setAttribute("aria-pressed", "false");
popular.appendChild(b);
});
filters.appendChild(popular);
}
var sort = Object.assign(document.createElement("select"), { id: "post-sort" });
sort.setAttribute("aria-controls", "post-cards");
sort.add(new Option("Newest first", "new"));
sort.add(new Option("Oldest first", "old"));
filters.append(
Object.assign(document.createElement("label"), { className: "visually-hidden", htmlFor: "post-sort", textContent: "Sort posts" }),
sort
);
var empty = Object.assign(document.createElement("p"), { className: "post-filters__empty", textContent: "No updates match your search.", hidden: true });
form.after(filters, empty);
var chips = popular.querySelectorAll("button");
function filter() {
var q = input.value.trim().toLowerCase();
var shown = 0;
items.forEach(function (li) {
var hit = !q || (li.textContent + " " + (li.dataset.tags || "")).toLowerCase().indexOf(q) !== -1;
li.hidden = !hit;
if (hit) shown++;
});
[].forEach.call(chips, function (c) { c.setAttribute("aria-pressed", String(c.textContent === q)); });
empty.hidden = shown > 0;
live.textContent = q ? shown + (shown === 1 ? " update found." : " updates found.") : "";
}
form.addEventListener("submit", function (e) { e.preventDefault(); filter(); });
input.addEventListener("input", filter);
popular.addEventListener("click", function (e) {
var c = e.target.closest("button");
if (!c) return;
input.value = c.getAttribute("aria-pressed") === "true" ? "" : c.textContent;
filter();
});
sort.addEventListener("change", function (e) {
var dir = e.target.value === "old" ? 1 : -1;
items.slice().sort(function (a, b) {
var ta = a.querySelector("time"), tb = b.querySelector("time");
var x = ta ? Date.parse(ta.getAttribute("datetime")) : null;
var y = tb ? Date.parse(tb.getAttribute("datetime")) : null;
return (x === null || y === null) ? (x === null) - (y === null) : dir * (x - y);
}).forEach(function (li) { list.appendChild(li); });
});
}
function applyTheme(theme) {
var dark = theme === "dark";
document.documentElement.setAttribute("data-theme", dark ? "dark" : "light");
try { localStorage.setItem(THEME_KEY, dark ? "dark" : "light"); } catch (_) {}
var btn = document.getElementById("theme-toggle");
if (!btn) return;
var label = dark ? "Switch to light mode" : "Switch to dark mode";
btn.setAttribute("aria-pressed", String(dark));
btn.setAttribute("aria-label", label);
btn.setAttribute("title", label);
btn.innerHTML = dark ? SUN_SVG : MOON_SVG;
}
var i18nNodes = [];
var currentLang = "en";
try {
var savedLang = localStorage.getItem(LANG_KEY);
if (savedLang === "id") currentLang = "id";
} catch (_) {}
function snapshotI18n() {
i18nNodes = [].slice.call(document.querySelectorAll("[data-i18n], [data-i18n-prefix], [data-i18n-placeholder]"));
i18nNodes.forEach(function (el) {
if ("en" in el.dataset) return;
if (el.hasAttribute("data-i18n-placeholder")) el.dataset.en = el.getAttribute("placeholder") || "";
else if (el.hasAttribute("data-i18n")) el.dataset.en = el.textContent;
else el.dataset.en = el.firstChild ? el.firstChild.nodeValue : "";
});
}
function applyLang(lang) {
i18nNodes.forEach(function (el) {
var idVal = function (attr) { var k = el.getAttribute(attr); return lang === "id" && ID_TEXT[k] != null ? ID_TEXT[k] : null; };
if (el.hasAttribute("data-i18n-placeholder")) el.setAttribute("placeholder", idVal("data-i18n-placeholder") || el.dataset.en);
else if (el.hasAttribute("data-i18n")) el.textContent = idVal("data-i18n") || el.dataset.en;
else if (el.firstChild) el.firstChild.nodeValue = (idVal("data-i18n-prefix") ? idVal("data-i18n-prefix") + " " : el.dataset.en);
});
document.documentElement.lang = lang;
var langBtn = document.getElementById("lang-toggle");
if (langBtn) {
langBtn.textContent = lang.toUpperCase();
langBtn.setAttribute("aria-label", lang === "id" ? "ID: switch language to English" : "EN: switch language to Indonesian");
}
}
function initNav() {
var navBtn = document.getElementById("about-menu-btn");
var dropdown = document.querySelector(".dropdown");
var backBtn = document.querySelector(".d-content-back");
var toggleBtn = document.querySelector(".nav-toggle");
var primaryNav = document.getElementById("primary-nav");
function closeDropdown() {
if (!navBtn) return;
navBtn.classList.remove("active");
navBtn.setAttribute("aria-expanded", "false");
if (dropdown && dropdown.contains(document.activeElement)) document.activeElement.blur();
}
if (navBtn && dropdown) {
navBtn.addEventListener("click", function (e) {
e.preventDefault();
navBtn.setAttribute("aria-expanded", String(navBtn.classList.toggle("active")));
});
if (!matchMedia("(pointer: coarse)").matches) {
dropdown.addEventListener("mouseenter", function () { navBtn.classList.add("active"); navBtn.setAttribute("aria-expanded", "true"); });
dropdown.addEventListener("mouseleave", closeDropdown);
}
if (backBtn) backBtn.addEventListener("click", function (e) { e.preventDefault(); closeDropdown(); });
document.addEventListener("click", function (e) { if (!dropdown.contains(e.target)) closeDropdown(); });
document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDropdown(); });
}
if (!toggleBtn || !primaryNav) return;
function setMenu(open) {
toggleBtn.setAttribute("aria-expanded", String(open));
toggleBtn.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
primaryNav.classList.toggle("is-open", open);
document.body.style.overflow = open ? "hidden" : "";
}
toggleBtn.addEventListener("click", function (e) { e.stopPropagation(); setMenu(toggleBtn.getAttribute("aria-expanded") !== "true"); });
primaryNav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
document.addEventListener("click", function (e) { if (!primaryNav.contains(e.target) && !toggleBtn.contains(e.target)) setMenu(false); });
addEventListener("resize", function () { if (innerWidth >= 768) setMenu(false); });
}
var countBefore = 0;
document.body.addEventListener("htmx:beforeRequest", function () {
var list = document.getElementById("post-list");
countBefore = list ? list.children.length : 0;
});
document.body.addEventListener("htmx:afterSettle", function (e) {
var target = e.detail.target;
if (target && target.id === "post-list") {
var added = target.children.length - countBefore;
syncPager(true);
if (added > 0) {
var first = target.children[countBefore].querySelector("h2 a, h3 a");
if (first) first.focus();
live.textContent = added + (added === 1 ? " more post loaded." : " more posts loaded.");
}
return;
}
if (target && target.tagName === "MAIN") {
var current = document.querySelector('.tab-grid a[aria-current="page"]');
if (current) current.focus();
syncPager(false);
initHeroMedia();
initPostFilters();
snapshotI18n();
if (currentLang !== "en") applyLang(currentLang);
}
});
var savedTheme = "light";
try { if (localStorage.getItem(THEME_KEY) === "dark") savedTheme = "dark"; } catch (_) {}
applyTheme(savedTheme);
syncPager(false);
initHeroMedia();
initPostFilters();
initNav();
snapshotI18n();
if (currentLang !== "en") applyLang(currentLang);
document.addEventListener("click", function (e) {
if (e.target.closest("#theme-toggle")) {
applyTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
} else if (e.target.closest("#lang-toggle")) {
currentLang = currentLang === "en" ? "id" : "en";
applyLang(currentLang);
try { localStorage.setItem(LANG_KEY, currentLang); } catch (_) {}
}
});
})();