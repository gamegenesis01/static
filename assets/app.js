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

  /* Commitment log ticker: last 12 trading days (sample fingerprints) */
  var rails = $("#rails");
  if (rails) {
    var hex = function (seed) {
      var h = 2166136261 >>> 0, out = "";
      for (var k = 0; k < seed.length; k++) { h ^= seed.charCodeAt(k); h = Math.imul(h, 16777619) >>> 0; }
      for (var n = 0; n < 16; n++) {
        h ^= h << 13; h >>>= 0; h ^= h >>> 17; h ^= h << 5; h >>>= 0;
        out += (h & 15).toString(16);
      }
      return out;
    };
    var days = [], d = new Date();
    while (days.length < 12) {
      var wd = d.getDay();
      if (wd !== 0 && wd !== 6) days.push(new Date(d));
      d.setDate(d.getDate() - 1);
    }
    var fmt = function (x) { return x.toISOString().slice(0, 10); };
    var html = days.map(function (x) {
      var key = fmt(x), hsh = hex(key);
      var trades = 150 + (parseInt(hsh.slice(0, 2), 16) % 90);
      return "<li><b>" + key + "</b><span>sha256 " + hsh.slice(0, 4) + "…" + hsh.slice(-4) + '</span><span class="pill pill--on">locked</span><span>' + trades + " trades</span></li>";
    }).join("") + '<li><b>Sample log</b><span>fingerprints shown for illustration</span></li>';
    rails.innerHTML = html;
    var clone = rails.cloneNode(true);
    clone.removeAttribute("id");
    clone.setAttribute("aria-hidden", "true");
    rails.parentNode.appendChild(clone);
  }

  /* Skill vs luck: one-sided confidence that true Sharpe > 0 after T years */
  var sharpe = $("#sharpe"), years = $("#years");
  if (sharpe && years) {
    var erf = function (x) {
      var s = x < 0 ? -1 : 1; x = Math.abs(x);
      var t = 1 / (1 + 0.3275911 * x);
      var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
      return s * y;
    };
    var phi = function (z) { return 0.5 * (1 + erf(z / Math.SQRT2)); };
    var fill = function (el) {
      var pct = ((el.value - el.min) / (el.max - el.min)) * 100;
      el.style.setProperty("--p", pct + "%");
    };
    var update = function () {
      var s = parseFloat(sharpe.value), t = parseFloat(years.value);
      var conf = phi(s * Math.sqrt(t));
      var need = Math.pow(1.645 / s, 2);
      $("#sharpeOut").textContent = s.toFixed(2);
      $("#yearsOut").textContent = t.toFixed(1) + (t === 1 ? " year" : " years");
      $("#confOut").textContent = (conf * 100).toFixed(conf > 0.995 ? 1 : 0) + "%";
      $("#needOut").textContent = need < 1 ? Math.round(need * 12) + " months" : need.toFixed(1) + " yrs";
      var bar = $("#confBar");
      bar.style.width = (conf * 100) + "%";
      bar.classList.toggle("is-ok", conf >= 0.95);
      [sharpe, years].forEach(fill);
      sharpe.setAttribute("aria-valuetext", "Sharpe " + s.toFixed(2));
      years.setAttribute("aria-valuetext", t.toFixed(1) + " years");
    };
    [sharpe, years].forEach(function (el) { el.addEventListener("input", update); });
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
        ? "You\u2019re on the list: " + val + ". The next monthly letter will land in your inbox."
        : "Enter an email like name@example.com to continue.";
      if (ok) input.value = "";
    });
  }

  /* Footer year */
  var y = $("#year");
  if (y) y.textContent = new Date().getFullYear();
})();
