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
    var within = function (a, b) { return weekday && ny.mins >= a && ny.mins < b; };
    var items = [
      { name: "RTP", note: "24/7 instant", on: true },
      { name: "FedNow", note: "24/7 instant", on: true },
      { name: "Fedwire", note: "cut-off 18:00 ET", on: within(9 * 60, 18 * 60) },
      { name: "Same-day ACH", note: "last window 16:45 ET", on: within(8 * 60, 16 * 60 + 45) },
      { name: "SEPA Instant", note: "24/7 · EUR", on: true },
      { name: "UK Faster Payments", note: "24/7 · GBP", on: true },
      { name: "SWIFT", note: "138 corridors", on: weekday },
      { fx: "EUR/USD", rate: "1.0842", chg: "+0.12%" },
      { fx: "GBP/USD", rate: "1.2718", chg: "+0.08%" },
      { fx: "USD/JPY", rate: "151.36", chg: "−0.21%" },
      { fx: "USD/INR", rate: "83.92", chg: "+0.03%" },
      { name: "13-wk T-bill", note: "yield 4.31%", on: true, static: true }
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

  /* Treasury calculator */
  var cash = $("#cash");
  if (cash) {
    var BANK = 0.0045, ACCEL = 0.0412, HIRE = 165000;
    var compact = function (n) {
      if (n >= 1e6) return "$" + (n / 1e6).toFixed(n % 1e6 === 0 ? 0 : 1) + "M";
      return usd(n);
    };
    var update = function () {
      var v = parseFloat(cash.value);
      var bank = v * BANK, accel = v * ACCEL, diff = accel - bank;
      $("#cashOut").textContent = usd(v);
      $("#bankOut").textContent = usd(Math.round(bank));
      $("#accelOut").textContent = usd(Math.round(accel));
      $("#diffOut").textContent = usd(Math.round(diff));
      $("#hireOut").textContent = (diff / HIRE).toFixed(1);
      var pct = ((v - cash.min) / (cash.max - cash.min)) * 100;
      cash.style.setProperty("--p", pct + "%");
      cash.setAttribute("aria-valuetext", compact(v));
    };
    cash.addEventListener("input", update);
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

  /* Pricing toggle */
  var priceEls = $$("[data-monthly]");
  $$(".toggle__btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var period = btn.dataset.period;
      $$(".toggle__btn").forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-on", on);
        b.setAttribute("aria-pressed", String(on));
      });
      priceEls.forEach(function (el) {
        el.textContent = el.dataset[period];
        el.classList.remove("price-flip");
        void el.offsetWidth;
        el.classList.add("price-flip");
      });
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
        ? "Got it: " + val + ". Online applications open soon, and you will be first in line."
        : "Enter a work email like name@company.com to continue.";
      if (ok) input.value = "";
    });
  }

  /* Footer year */
  var y = $("#year");
  if (y) y.textContent = new Date().getFullYear();
})();
