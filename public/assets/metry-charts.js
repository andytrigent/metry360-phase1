/* ==========================================================================
   Metry360 — tiny inline-SVG chart helpers. No dependencies.
   Public API (attached to window.MetryCharts):
     donut(el, pct, color, opts)
     sparkline(el, values, color, opts)
     lineChart(el, { series, labels, yMax, ... })
   All helpers render into `el` (an element or a selector string) by setting
   innerHTML to an <svg>. Safe to call repeatedly (re-renders).

   History-awareness: we currently have at most ~2 weeks of real data. The
   line/spark helpers therefore degrade gracefully for 0/1/2-point series —
   they draw the dot markers that DO exist and never fake a trend line the
   data can't support.
   ========================================================================== */
(function (global) {
  "use strict";

  var SVGNS = "http://www.w3.org/2000/svg";

  /* ---- token fallbacks (read from CSS custom props when available) ------- */
  function token(name, fallback) {
    try {
      var v = getComputedStyle(document.documentElement)
        .getPropertyValue(name)
        .trim();
      return v || fallback;
    } catch (e) {
      return fallback;
    }
  }

  function resolve(el) {
    if (typeof el === "string") return document.querySelector(el);
    return el;
  }

  function el(tag, attrs) {
    var node = document.createElementNS(SVGNS, tag);
    if (attrs) {
      for (var k in attrs) {
        if (Object.prototype.hasOwnProperty.call(attrs, k)) {
          node.setAttribute(k, attrs[k]);
        }
      }
    }
    return node;
  }

  // responsive=true  -> width:100%, height derives from viewBox aspect ratio
  //          =false -> explicit px width/height (fixed-size marks: donut/sparkline)
  function svgRoot(w, h, responsive) {
    var attrs = {
      viewBox: "0 0 " + w + " " + h,
      preserveAspectRatio: "xMidYMid meet",
      role: "img"
    };
    if (responsive) {
      attrs.width = "100%";
    } else {
      attrs.width = w;
      attrs.height = h;
    }
    return el("svg", attrs);
  }

  function mount(target, svg) {
    var node = resolve(target);
    if (!node) return null;
    node.innerHTML = "";
    node.appendChild(svg);
    return svg;
  }

  /* ======================================================================
     DONUT
     donut(el, pct, color, { size, thickness, track, showLabel, label })
     - pct: 0..100 (clamped). Arc starts at 12 o'clock, sweeps clockwise.
     - Rounded caps. Center label injected as an overlaid HTML node if the
       parent uses .m-donut (preferred), else drawn as SVG text.
     ==================================================================== */
  function donut(target, pct, color, opts) {
    opts = opts || {};
    var size = opts.size || 140;
    var thickness = opts.thickness || 14;
    var track = opts.track || token("--track", "#E7EDF3");
    var arc = color || token("--donut-health", "#F5A623");
    var value = Math.max(0, Math.min(100, Number(pct) || 0));

    var r = (size - thickness) / 2;
    var cx = size / 2;
    var cy = size / 2;
    var circ = 2 * Math.PI * r;
    var dash = (value / 100) * circ;

    var svg = svgRoot(size, size, false);
    svg.setAttribute("aria-label", "Donut: " + value + "%");

    // track
    svg.appendChild(
      el("circle", {
        cx: cx, cy: cy, r: r,
        fill: "none",
        stroke: track,
        "stroke-width": thickness
      })
    );
    // arc (rotate -90deg so it starts at top; sweep clockwise)
    if (value > 0) {
      svg.appendChild(
        el("circle", {
          cx: cx, cy: cy, r: r,
          fill: "none",
          stroke: arc,
          "stroke-width": thickness,
          "stroke-linecap": "round",
          "stroke-dasharray": dash + " " + (circ - dash),
          "stroke-dashoffset": 0,
          transform: "rotate(-90 " + cx + " " + cy + ")"
        })
      );
    }

    // Center label: prefer an existing .m-donut__center overlay in the DOM.
    var node = resolve(target);
    var hasOverlay = node && node.querySelector && node.querySelector(".m-donut__center");
    if (opts.showLabel !== false && !hasOverlay) {
      var t = el("text", {
        x: cx, y: cy,
        "text-anchor": "middle",
        "dominant-baseline": "central",
        "font-size": Math.round(size * 0.19),
        "font-weight": "700",
        fill: token("--donut-center", "#5B6BB0"),
        "font-family": token("--font-sans", "Inter, sans-serif")
      });
      t.textContent = opts.label != null ? opts.label : value + "%";
      svg.appendChild(t);
    }

    return mount(target, svg);
  }

  /* ======================================================================
     SPARKLINE
     sparkline(el, values, color, { width, height, strokeWidth })
     - Draws a single stroke across the value series with subtle dot at the
       last point. 0 pts -> empty; 1 pt -> single dot; 2 pts -> straight seg.
     ==================================================================== */
  function sparkline(target, values, color, opts) {
    opts = opts || {};
    var w = opts.width || 90;
    var h = opts.height || 24;
    var sw = opts.strokeWidth || 2;
    var stroke = color || token("--green", "#16A34A");
    var pad = sw + 1;

    values = (values || []).map(Number).filter(function (v) { return !isNaN(v); });

    var svg = svgRoot(w, h, false);
    svg.setAttribute("aria-label", "Sparkline");

    if (values.length === 0) {
      return mount(target, svg);
    }

    var min = Math.min.apply(null, values);
    var max = Math.max.apply(null, values);
    var span = max - min || 1;
    var innerW = w - pad * 2;
    var innerH = h - pad * 2;

    function x(i) {
      if (values.length === 1) return w / 2;
      return pad + (i / (values.length - 1)) * innerW;
    }
    function y(v) {
      return pad + innerH - ((v - min) / span) * innerH;
    }

    if (values.length === 1) {
      svg.appendChild(el("circle", { cx: x(0), cy: y(values[0]), r: sw, fill: stroke }));
      return mount(target, svg);
    }

    var d = "";
    values.forEach(function (v, i) {
      d += (i === 0 ? "M" : "L") + x(i).toFixed(1) + " " + y(v).toFixed(1) + " ";
    });
    svg.appendChild(
      el("path", {
        d: d.trim(),
        fill: "none",
        stroke: stroke,
        "stroke-width": sw,
        "stroke-linecap": "round",
        "stroke-linejoin": "round"
      })
    );
    // endpoint dot for 2-pt series so a "trend" of two reads as two marks
    var last = values.length - 1;
    svg.appendChild(el("circle", { cx: x(last), cy: y(values[last]), r: sw * 0.9, fill: stroke }));

    return mount(target, svg);
  }

  /* ======================================================================
     LINE CHART
     lineChart(el, {
       series: [{ values:[...], color }],   // one or more lines
       labels: ["Week 1", ...],             // x-axis tick labels
       yMax: 8,                             // top of y-axis (default auto)
       yTicks: [0,4,8],                     // gridline values (default 0..yMax /2)
       width, height
     })
     - Dotted horizontal gridlines, filled dot markers, tiny gray axis labels.
     - 0/1/2 real points: markers still drawn; no fabricated slope beyond the
       points provided.
     ==================================================================== */
  function lineChart(target, cfg) {
    cfg = cfg || {};
    var w = cfg.width || 520;
    var h = cfg.height || 150;
    var series = cfg.series || [];
    var labels = cfg.labels || [];
    var grid = token("--grid", "#E7EAF0");
    var axis = token("--axis-label", "#9AA0B0");
    var font = token("--font-sans", "Inter, sans-serif");

    // margins: room for y labels (left) and x labels (bottom).
    // marginTop is configurable so the top y-tick label isn't clipped at the card edge.
    var mL = 22, mR = 12, mT = (cfg.marginTop != null ? cfg.marginTop : 10), mB = 22;
    var plotW = w - mL - mR;
    var plotH = h - mT - mB;

    // determine max point count + value range
    var allVals = [];
    series.forEach(function (s) {
      (s.values || []).forEach(function (v) { if (v != null && !isNaN(v)) allVals.push(Number(v)); });
    });
    var yMax = cfg.yMax != null ? cfg.yMax : (allVals.length ? Math.ceil(Math.max.apply(null, allVals)) : 8);
    if (yMax <= 0) yMax = 8;
    var yTicks = cfg.yTicks || [0, yMax / 2, yMax];
    // callers may pass ticks rounded above the data max — the scale must cover them
    var tickMax = Math.max.apply(null, yTicks);
    if (tickMax > yMax) yMax = tickMax;

    var nPoints = 0;
    series.forEach(function (s) { nPoints = Math.max(nPoints, (s.values || []).length); });
    if (labels.length) nPoints = Math.max(nPoints, labels.length);

    var svg = svgRoot(w, h, true);
    svg.setAttribute("aria-label", "Line chart");

    function px(i) {
      if (nPoints <= 1) return mL + plotW / 2;
      return mL + (i / (nPoints - 1)) * plotW;
    }
    function py(v) {
      return mT + plotH - (v / yMax) * plotH;
    }

    // gridlines + y tick labels
    yTicks.forEach(function (tv) {
      var y = py(tv);
      svg.appendChild(
        el("line", {
          x1: mL, y1: y, x2: w - mR, y2: y,
          stroke: grid,
          "stroke-width": 1,
          "stroke-dasharray": "3 4"
        })
      );
      var lbl = el("text", {
        x: mL - 6, y: y,
        "text-anchor": "end",
        "dominant-baseline": "central",
        "font-size": 10,
        fill: axis,
        "font-family": font
      });
      lbl.textContent = String(Math.round(tv));
      svg.appendChild(lbl);
    });

    // x-axis labels
    labels.forEach(function (lab, i) {
      var t = el("text", {
        x: px(i), y: h - 6,
        "text-anchor": "middle",
        "font-size": 10,
        fill: axis,
        "font-family": font
      });
      t.textContent = lab;
      svg.appendChild(t);
    });

    // series lines + markers
    series.forEach(function (s) {
      var color = s.color || token("--line-joiner", "#3B82F6");
      var vals = (s.values || []).map(function (v) { return v == null ? null : Number(v); });

      // build path across non-null points (a single null gap won't fake a line)
      var d = "";
      var started = false;
      vals.forEach(function (v, i) {
        if (v == null || isNaN(v)) { started = false; return; }
        d += (started ? "L" : "M") + px(i).toFixed(1) + " " + py(v).toFixed(1) + " ";
        started = true;
      });
      if (d && vals.filter(function (v) { return v != null; }).length > 1) {
        svg.appendChild(
          el("path", {
            d: d.trim(),
            fill: "none",
            stroke: color,
            "stroke-width": 2,
            "stroke-linecap": "round",
            "stroke-linejoin": "round"
          })
        );
      }
      // dot markers for every real point
      vals.forEach(function (v, i) {
        if (v == null || isNaN(v)) return;
        svg.appendChild(el("circle", { cx: px(i), cy: py(v), r: 3.2, fill: color }));
      });
    });

    return mount(target, svg);
  }

  global.MetryCharts = { donut: donut, sparkline: sparkline, lineChart: lineChart };
})(typeof window !== "undefined" ? window : this);
