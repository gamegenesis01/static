(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var usd = function (n, digits) {
    return "$" + n.toLocaleString("en-US", { minimumFractionDigits: digits || 0, maximumFractionDigits: digits || 0 });
  };

  /* Header border on scroll */
  var header = $(".header");
  var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile nav */
  var burger = $("#burger");
  var nav = $("#nav");
  var setNav = function (open) {
    nav.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.style.overflow = open ? "hidden" : "";
  };
  burger.addEventListener("click", function () { setNav(!nav.classList.contains("is-open")); });
  $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 960) setNav(false); });

  /* Hero balance count-up (page shows the final value without JS) */
  var bal = $("#balance");
  if (bal && !reduceMotion) {
    var target = parseFloat(bal.dataset.value);
    var start = target * 0.93;
    var t0 = null;
    var dur = 1800;
    var step = function (ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 4);
      bal.textContent = usd(start + (target - start) * eased, 2);
      if (p < 1) requestAnimationFrame(step);
    };
    setTimeout(function () { requestAnimationFrame(step); }, 500);
  }

  /* Payment rail status ticker: open/closed computed from New York time */
  var rails = $("#rails");
  if (rails) {
    var nyParts = function () {
      try {
        var f = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", minute: "numeric", hour12: false });
        var parts = {};
        f.formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
        return { day: parts.weekday, mins: (parseInt(parts.hour, 10) % 24) * 60 + parseInt(parts.minute, 10) };
      } catch (e) { return { day: "Mon", mins: 600 }; }
    };
    var ny = nyParts();
    var weekday = ["Sat", "Sun"].indexOf(ny.day) === -1;
    var marketOpen = weekday && ny.mins >= 9 * 60 + 30 && ny.mins < 16 * 60;
    var items = [
      { name: "NYSE", note: "9:30–16:00 ET", on: marketOpen },
      { name: "Nasdaq", note: "9:30–16:00 ET", on: marketOpen },
      { fx: "S&P 500", rate: "6,012.40", chg: "+0.42%" },
      { fx: "Nasdaq 100", rate: "21,184.6", chg: "+0.61%" },
      { fx: "Dow", rate: "43,920.1", chg: "+0.18%" },
      { fx: "Russell 2000", rate: "2,341.7", chg: "−0.27%" },
      { fx: "10-yr Treasury", rate: "4.18%", chg: "+0.03" },
      { fx: "13-wk T-bill", rate: "4.31%", chg: "+0.01" },
      { fx: "Gold", rate: "$2,684", chg: "+0.35%" },
      { fx: "EUR/USD", rate: "1.0842", chg: "+0.12%" },
      { name: "Prices", note: "indicative, for illustration", on: true, static: true }
    ];
    var html = items.map(function (i) {
      if (i.fx) {
        var up = i.chg.charAt(0) === "+";
        return '<li><b>' + i.fx + '</b><span>' + i.rate + '</span><span class="' + (up ? "fx-up" : "") + '">' + i.chg + "</span></li>";
      }
      var pill = i.static ? "" : '<span class="pill ' + (i.on ? "pill--on" : "pill--off") + '">' + (i.on ? "open" : "closed") + "</span>";
      return "<li><b>" + i.name + "</b>" + pill + "<span>" + i.note + "</span></li>";
    }).join("");
    rails.innerHTML = html;
    var clone = rails.cloneNode(true);
    clone.removeAttribute("id");
    clone.setAttribute("aria-hidden", "true");
    rails.parentNode.appendChild(clone);
  }

  /* Fee calculator: 7% gross return, 1.00% vs 0.25% yearly fee */
  var cash = $("#cash"), years = $("#years");
  if (cash && years) {
    var GROSS = 0.07, ADVISOR = 0.01, ACCEL = 0.0025;
    var fill = function (el) {
      var pct = ((el.value - el.min) / (el.max - el.min)) * 100;
      el.style.setProperty("--p", pct + "%");
    };
    var update = function () {
      var v = parseFloat(cash.value), n = parseInt(years.value, 10);
      var adv = v * Math.pow(1 + GROSS - ADVISOR, n);
      var acc = v * Math.pow(1 + GROSS - ACCEL, n);
      $("#cashOut").textContent = usd(v);
      $("#yearsOut").textContent = n;
      $("#bankOut").textContent = usd(Math.round(adv));
      $("#accelOut").textContent = usd(Math.round(acc));
      $("#diffOut").textContent = usd(Math.round(acc - adv));
      fill(cash); fill(years);
      cash.setAttribute("aria-valuetext", usd(v));
      years.setAttribute("aria-valuetext", n + " years");
    };
    cash.addEventListener("input", update);
    years.addEventListener("input", update);
    update();
  }

  /* Pilot quick replies */
  var reply = $("#chatReply");
  $$(".chip[data-reply]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      $$(".chip").forEach(function (c) { c.classList.remove("is-on"); });
      chip.classList.add("is-on");
      reply.hidden = false;
      reply.textContent = "";
      var text = chip.dataset.reply;
      if (reduceMotion) { reply.textContent = text; return; }
      var i = 0;
      var typer = setInterval(function () {
        i += 2;
        reply.textContent = text.slice(0, i);
        if (i >= text.length) clearInterval(typer);
      }, 14);
    });
  });

  /* Stat count-up when scrolled into view (numbers are already visible at rest) */
  if (!reduceMotion && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var el = en.target;
        var end = parseFloat(el.dataset.count);
        var pre = el.dataset.prefix || "", suf = el.dataset.suffix || "";
        var t0 = null;
        var tick = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 1400);
          var v = Math.round(end * (1 - Math.pow(1 - p, 3)));
          el.textContent = pre + v.toLocaleString("en-US") + suf;
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    $$("[data-count]").forEach(function (el) { io.observe(el); });
  }

  /* Email capture (static site: validates and confirms locally) */
  var form = $("#ctaForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = $("#email");
      var msg = $("#ctaMsg");
      var val = input.value.trim();
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val);
      msg.className = "cta__msg " + (ok ? "is-ok" : "is-err");
      msg.textContent = ok
        ? "Got it: " + val + ". Accounts open soon, and you will be first in line."
        : "Enter an email like name@example.com to continue.";
      if (ok) input.value = "";
    });
  }

  /* Footer year */
  var y = $("#year");
  if (y) y.textContent = new Date().getFullYear();
})();
