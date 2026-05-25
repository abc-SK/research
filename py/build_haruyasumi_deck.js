const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";
pptx.author = "Codex";
pptx.subject = "Random graph greedy coloring simulation";
pptx.title = "春休み課題: ランダムグラフの貪欲彩色";
pptx.lang = "ja-JP";
pptx.theme = {
  headFontFace: "Yu Gothic",
  bodyFontFace: "Yu Gothic",
  lang: "ja-JP",
};

const OUT = "C:/Users/kazuy/Documents/research/py/haruyasumi_readable.pptx";
const N = 100;
const TRIALS = 200;
const PS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9];
const SEED = 20260513;

const C = {
  bg: "F7F9FC",
  ink: "1F2933",
  muted: "5B677A",
  line: "D7DEE8",
  white: "FFFFFF",
  blue: "2F6BFF",
  blue2: "4C78A8",
  green: "1E8E5A",
  orange: "F58518",
  paleBlue: "EAF1FF",
  paleOrange: "FFF1E4",
};

function mulberry32(seed) {
  let a = seed >>> 0;
  return function rand() {
    a += 0x6d2b79f5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const rand = mulberry32(SEED);

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

function buildGraph(p) {
  const adj = Array.from({ length: N }, () => Array(N).fill(0));
  let edges = 0;
  for (let i = 0; i < N; i++) {
    for (let j = i + 1; j < N; j++) {
      if (rand() < p) {
        adj[i][j] = 1;
        adj[j][i] = 1;
        edges += 1;
      }
    }
  }
  return { adj, edges };
}

function greedyColoring(adj, order) {
  const color = Array(N).fill(0);
  for (const v of order) {
    const used = Array(N + 1).fill(false);
    for (let u = 0; u < N; u++) {
      if (adj[v][u] === 1 && color[u] !== 0) used[color[u]] = true;
    }
    let c = 1;
    while (used[c]) c += 1;
    color[v] = c;
  }
  return Math.max(...color);
}

function simulate() {
  return PS.map((p) => {
    const { adj, edges } = buildGraph(p);
    const results = [];
    for (let t = 0; t < TRIALS; t++) {
      const order = Array.from({ length: N }, (_, i) => i);
      shuffle(order);
      results.push(greedyColoring(adj, order));
    }
    const avg = results.reduce((a, b) => a + b, 0) / TRIALS;
    const variance = results.reduce((a, x) => a + (x - avg) ** 2, 0) / TRIALS;
    return {
      p,
      edges,
      results,
      avg,
      variance,
      min: Math.min(...results),
      max: Math.max(...results),
    };
  });
}

const stats = simulate();

function histogram(results) {
  const min = Math.min(...results);
  const max = Math.max(...results);
  const labels = [];
  const values = [];
  for (let x = min; x <= max; x++) {
    labels.push(String(x));
    values.push(results.filter((v) => v === x).length);
  }
  return { labels, values };
}

function addBase(slide, kicker) {
  slide.background = { color: C.bg };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 0.18,
    fill: { color: C.blue },
    line: { color: C.blue },
  });
  if (kicker) {
    slide.addText(kicker, {
      x: 0.55,
      y: 0.34,
      w: 4.8,
      h: 0.22,
      fontFace: "Yu Gothic",
      fontSize: 9,
      bold: true,
      color: C.blue,
      margin: 0,
      fit: "shrink",
    });
  }
}

function addTitle(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.55,
    y: 0.68,
    w: 9.2,
    h: 0.52,
    fontFace: "Yu Gothic",
    fontSize: 24,
    bold: true,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.58,
      y: 1.18,
      w: 11.5,
      h: 0.28,
      fontFace: "Yu Gothic",
      fontSize: 10.5,
      color: C.muted,
      margin: 0,
      fit: "shrink",
    });
  }
}

function addFooter(slide, page) {
  slide.addText(`春休み課題: ランダムグラフの貪欲彩色 | ${page}`, {
    x: 9.55,
    y: 7.13,
    w: 3.2,
    h: 0.18,
    fontFace: "Yu Gothic",
    fontSize: 7.5,
    color: "7B8494",
    align: "right",
    margin: 0,
  });
}

function addChip(slide, text, x, y, color) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w: 2.18,
    h: 0.36,
    rectRadius: 0.08,
    fill: { color },
    line: { color },
  });
  slide.addText(text, {
    x: x + 0.11,
    y: y + 0.095,
    w: 1.96,
    h: 0.13,
    fontFace: "Yu Gothic",
    fontSize: 8.5,
    bold: true,
    color: C.white,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
}

function addBulletBlock(slide, title, items, x, y, w, h) {
  if (title) {
    slide.addText(title, {
      x,
      y,
      w,
      h: 0.28,
      fontFace: "Yu Gothic",
      fontSize: 12.5,
      bold: true,
      color: C.ink,
      margin: 0,
    });
    y += 0.42;
    h -= 0.42;
  }
  slide.addText(
    items.map((item) => ({
      text: item,
      options: { bullet: { type: "ul" }, hanging: 4, breakLine: true },
    })),
    {
      x,
      y,
      w,
      h,
      fontFace: "Yu Gothic",
      fontSize: 12.4,
      color: C.ink,
      margin: 0.03,
      paraSpaceAfterPt: 7,
      fit: "shrink",
    }
  );
}

function addMetric(slide, label, value, x, y, color) {
  slide.addText(value, {
    x,
    y,
    w: 2.3,
    h: 0.48,
    fontFace: "Yu Gothic",
    fontSize: 24,
    bold: true,
    color,
    margin: 0,
    fit: "shrink",
  });
  slide.addText(label, {
    x,
    y: y + 0.48,
    w: 2.4,
    h: 0.22,
    fontFace: "Yu Gothic",
    fontSize: 8.8,
    color: C.muted,
    margin: 0,
    fit: "shrink",
  });
}

function addWhitePanel(slide, x, y, w, h) {
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w,
    h,
    fill: { color: C.white },
    line: { color: C.line, transparency: 8 },
  });
}

function chartOptions(title, x, y, w, h, yTitle) {
  return {
    x,
    y,
    w,
    h,
    showTitle: true,
    title,
    titleFontFace: "Yu Gothic",
    titleFontSize: 12,
    showLegend: false,
    catAxisLabelFontFace: "Yu Gothic",
    catAxisLabelFontSize: 8,
    valAxisLabelFontFace: "Yu Gothic",
    valAxisLabelFontSize: 8,
    valAxisTitle: yTitle,
    valAxisTitleFontFace: "Yu Gothic",
    valAxisTitleFontSize: 9,
    showValue: false,
    showCatName: false,
    showValAxis: true,
    showCatAxis: true,
    chartColors: [C.blue2, C.orange],
    valGridLine: { color: "E3E8F0", transparency: 20 },
  };
}

function cover() {
  const slide = pptx.addSlide();
  slide.background = { color: "F3F7FE" };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 0.28,
    h: 7.5,
    fill: { color: C.blue },
    line: { color: C.blue },
  });
  slide.addText("ランダムグラフの\n貪欲彩色シミュレーション", {
    x: 0.82,
    y: 1.05,
    w: 6.9,
    h: 1.72,
    fontFace: "Yu Gothic",
    fontSize: 29,
    bold: true,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("辺ができる確率 P を変えて、必要な色数の平均と分散を見る", {
    x: 0.86,
    y: 3.0,
    w: 6.8,
    h: 0.32,
    fontFace: "Yu Gothic",
    fontSize: 13,
    color: C.muted,
    margin: 0,
  });
  addChip(slide, "N = 100", 0.86, 3.62, C.blue);
  addChip(slide, "TRIALS = 200", 3.24, 3.62, C.green);
  addChip(slide, "P = 0.1 ... 0.9", 5.62, 3.62, C.orange);
  slide.addShape(pptx.ShapeType.line, {
    x: 8.1,
    y: 0.86,
    w: 0,
    h: 5.85,
    line: { color: C.line, width: 1 },
  });
  addMetric(slide, "最大の平均色数", stats.at(-1).avg.toFixed(2), 8.55, 1.25, C.blue);
  addMetric(slide, "最大の分散", Math.max(...stats.map((s) => s.variance)).toFixed(2), 10.78, 1.25, C.orange);
  addMetric(slide, "最も密なグラフの辺数", String(stats.at(-1).edges), 8.55, 3.0, C.green);
  addMetric(slide, "乱数シード", String(SEED), 10.78, 3.0, C.blue);
  slide.addText("目的: グラフが密になるほど、貪欲彩色の結果がどう変わるかを確認する。", {
    x: 8.55,
    y: 5.0,
    w: 3.95,
    h: 0.62,
    fontFace: "Yu Gothic",
    fontSize: 13,
    bold: true,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide, "1");
}

function setupSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "実験設定");
  addTitle(slide, "haruyasumi.py が行っていること", "ランダムグラフを1つ作り、頂点の処理順を変えながら貪欲彩色を200回実行する。");
  addBulletBlock(
    slide,
    "処理の流れ",
    [
      "頂点数 N=100 のグラフを用意する",
      "各頂点ペアに対して、確率 P で辺を追加する",
      "隣接行列を作り、辺の有無を 0/1 で管理する",
      "頂点の順番をランダムに並べ替えて貪欲彩色する",
      "200回の結果から平均と分散を計算する",
    ],
    0.75,
    1.88,
    5.35,
    4.2
  );
  addWhitePanel(slide, 6.8, 1.76, 5.55, 4.45);
  const rows = [
    ["入力", "P = 0.1, 0.2, ..., 0.9"],
    ["試行", "各Pにつき200回"],
    ["評価", "必要だった色数"],
    ["出力", "色数の分布・平均・分散"],
  ];
  rows.forEach((r, i) => {
    const y = 2.1 + i * 0.84;
    slide.addText(r[0], {
      x: 7.25,
      y,
      w: 1.0,
      h: 0.22,
      fontFace: "Yu Gothic",
      fontSize: 11,
      bold: true,
      color: C.blue,
      margin: 0,
    });
    slide.addText(r[1], {
      x: 8.3,
      y,
      w: 3.25,
      h: 0.24,
      fontFace: "Yu Gothic",
      fontSize: 11,
      color: C.ink,
      margin: 0,
      fit: "shrink",
    });
  });
  slide.addText("貪欲彩色は頂点の順番で結果が変わるため、同じグラフでも試行ごとに必要色数が揺れる。", {
    x: 7.25,
    y: 5.25,
    w: 4.25,
    h: 0.42,
    fontFace: "Yu Gothic",
    fontSize: 11.5,
    bold: true,
    color: C.ink,
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide, "2");
}

function summaryChartSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "結果1");
  addTitle(slide, "P が大きいほど必要な色数は増える", "辺が増えるほど隣接制約が強くなり、貪欲彩色で使う色数の平均も上がる。");
  addWhitePanel(slide, 0.6, 1.65, 12.15, 4.95);
  const labels = stats.map((s) => String(s.p));
  slide.addChart(
    pptx.ChartType.line,
    [{ name: "Average colors", labels, values: stats.map((s) => Number(s.avg.toFixed(2))) }],
    {
      ...chartOptions("P vs Average colors", 0.9, 1.96, 5.55, 3.85, "Average colors"),
      showLegend: false,
      chartColors: [C.blue],
      valAxisMinVal: 0,
    }
  );
  slide.addChart(
    pptx.ChartType.line,
    [{ name: "Variance", labels, values: stats.map((s) => Number(s.variance.toFixed(3))) }],
    {
      ...chartOptions("P vs Variance", 6.92, 1.96, 5.45, 3.85, "Variance"),
      showLegend: false,
      chartColors: [C.orange],
      valAxisMinVal: 0,
    }
  );
  addFooter(slide, "3");
}

function tableSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "結果2");
  addTitle(slide, "平均・分散・色数範囲の一覧", "Pごとの統計量をまとめると、平均色数はほぼ単調に増加している。");
  const rows = [
    [
      { text: "P", options: { bold: true } },
      { text: "辺数", options: { bold: true } },
      { text: "平均色数", options: { bold: true } },
      { text: "分散", options: { bold: true } },
      { text: "最小-最大", options: { bold: true } },
    ],
    ...stats.map((s) => [
      String(s.p),
      String(s.edges),
      s.avg.toFixed(2),
      s.variance.toFixed(3),
      `${s.min}-${s.max}`,
    ]),
  ];
  slide.addTable(rows, {
    x: 0.75,
    y: 1.72,
    w: 7.1,
    h: 4.8,
    border: { color: C.line, pt: 1 },
    fill: { color: C.white },
    color: C.ink,
    fontFace: "Yu Gothic",
    fontSize: 10,
    margin: 0.06,
    valign: "mid",
    fit: "shrink",
    autoFit: false,
    colW: [0.8, 1.35, 1.55, 1.25, 1.3],
    rowH: [0.38, ...Array(stats.length).fill(0.38)],
  });
  addBulletBlock(
    slide,
    "読み取り",
    [
      "P=0.1では平均約7色、P=0.9では平均約48色",
      "密なグラフほど使える色の選択肢が減り、色数が増える",
      "分散は全体として小さく、試行順序による揺れは限定的",
      "ただし分散の山はPによって変わるため、順序依存性も残る",
    ],
    8.45,
    1.92,
    3.55,
    3.9
  );
  addFooter(slide, "4");
}

function histSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "結果3");
  addTitle(slide, "色数分布の例", "疎なグラフ・中間・密なグラフの3条件で、200回の色数分布を比較する。");
  const selected = [0.1, 0.5, 0.9].map((p) => stats.find((s) => s.p === p));
  selected.forEach((s, idx) => {
    const x = 0.65 + idx * 4.18;
    addWhitePanel(slide, x, 1.72, 3.72, 4.75);
    const h = histogram(s.results);
    slide.addChart(
      pptx.ChartType.bar,
      [{ name: "Trials", labels: h.labels, values: h.values }],
      {
        ...chartOptions(`P=${s.p}`, x + 0.24, 2.02, 3.22, 3.05, "Trials"),
        catAxisTitle: "Colors",
        catAxisTitleFontFace: "Yu Gothic",
        catAxisTitleFontSize: 8,
        chartColors: [idx === 0 ? C.blue2 : idx === 1 ? C.green : C.orange],
        valAxisMinVal: 0,
      }
    );
    slide.addText(`平均 ${s.avg.toFixed(2)} 色 / 分散 ${s.variance.toFixed(3)}`, {
      x: x + 0.32,
      y: 5.42,
      w: 3.05,
      h: 0.24,
      fontFace: "Yu Gothic",
      fontSize: 9.5,
      bold: true,
      color: C.ink,
      align: "center",
      margin: 0,
      fit: "shrink",
    });
  });
  addFooter(slide, "5");
}

function summarySlide() {
  const slide = pptx.addSlide();
  addBase(slide, "まとめ");
  addTitle(slide, "結果のまとめ", "Pが大きくなるほど辺が増え、貪欲彩色で必要な色数も増加した。");
  addBulletBlock(
    slide,
    "分かったこと",
    [
      "辺が少ないグラフでは、比較的少ない色数で彩色できる",
      "辺が多いグラフでは、隣り合う頂点が増えるため必要色数が増える",
      "貪欲彩色は頂点順序に依存するので、同じPでも結果にばらつきが出る",
      "200回試行することで、平均と分散から傾向を確認できる",
    ],
    0.85,
    1.82,
    5.45,
    3.85
  );
  addWhitePanel(slide, 7.05, 1.78, 4.8, 3.75);
  slide.addText("次にできる改善", {
    x: 7.38,
    y: 2.12,
    w: 3.4,
    h: 0.28,
    fontFace: "Yu Gothic",
    fontSize: 14,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  addBulletBlock(
    slide,
    "",
    [
      "Pごとにグラフ自体も複数生成して平均する",
      "貪欲彩色以外の手法と比較する",
      "最大次数や辺数との関係もグラフ化する",
    ],
    7.38,
    2.72,
    3.95,
    2.1
  );
  addFooter(slide, "6");
}

cover();
setupSlide();
summaryChartSlide();
tableSlide();
histSlide();
summarySlide();

pptx.writeFile({ fileName: OUT });
