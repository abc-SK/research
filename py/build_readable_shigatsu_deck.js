const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Codex";
pptx.subject = "Information communication simulation";
pptx.title = "情報通信シミュレーション課題";
pptx.company = "research";
pptx.lang = "ja-JP";
pptx.theme = {
  headFontFace: "Yu Gothic",
  bodyFontFace: "Yu Gothic",
  lang: "ja-JP",
};
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";

const OUT = "C:/Users/kazuy/Documents/research/shigatsu/shigatsunokadai_average_readable.pptx";
const IMG_DIR = "C:/Users/kazuy/Documents/research/py/output_shigatsu";
const C = {
  navy: "19324D",
  blue: "2F6BFF",
  lightBlue: "EAF1FF",
  ink: "1F2933",
  muted: "5B677A",
  line: "D7DEE8",
  green: "1E8E5A",
  orange: "F07C24",
  bg: "F7F9FC",
  white: "FFFFFF",
};

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
      w: 4.5,
      h: 0.25,
      fontFace: "Yu Gothic",
      fontSize: 9,
      color: C.blue,
      bold: true,
      margin: 0,
    });
  }
}

function addTitle(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.55,
    y: 0.67,
    w: 8.6,
    h: 0.55,
    fontFace: "Yu Gothic",
    fontSize: 24,
    bold: true,
    color: C.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.58,
      y: 1.18,
      w: 10.7,
      h: 0.3,
      fontFace: "Yu Gothic",
      fontSize: 10.5,
      color: C.muted,
      margin: 0,
      fit: "shrink",
    });
  }
}

function addFooter(slide, page) {
  slide.addText(`情報通信シミュレーション | ${page}`, {
    x: 10.75,
    y: 7.13,
    w: 2.05,
    h: 0.18,
    fontFace: "Yu Gothic",
    fontSize: 7.5,
    color: "7B8494",
    align: "right",
    margin: 0,
  });
}

function addChip(slide, text, x, y, color = C.blue) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w: 2.25,
    h: 0.36,
    rectRadius: 0.08,
    fill: { color },
    line: { color },
  });
  slide.addText(text, {
    x: x + 0.12,
    y: y + 0.095,
    w: 2.01,
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

function addBulletBlock(slide, items, x, y, w, h, title) {
  if (title) {
    slide.addText(title, {
      x,
      y,
      w,
      h: 0.28,
      fontFace: "Yu Gothic",
      fontSize: 12,
      bold: true,
      color: C.ink,
      margin: 0,
    });
    y += 0.42;
    h -= 0.42;
  }
  const runs = items.map((item) => ({
    text: item,
    options: {
      bullet: { type: "ul" },
      hanging: 4,
      breakLine: true,
    },
  }));
  slide.addText(runs, {
    x,
    y,
    w,
    h,
    fontFace: "Yu Gothic",
    fontSize: 13,
    color: C.ink,
    breakLine: false,
    margin: 0.03,
    paraSpaceAfterPt: 8,
    fit: "shrink",
  });
}

function addMetric(slide, label, value, x, y, color) {
  slide.addText(value, {
    x,
    y,
    w: 2.1,
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
    w: 2.35,
    h: 0.24,
    fontFace: "Yu Gothic",
    fontSize: 8.8,
    color: C.muted,
    margin: 0,
    fit: "shrink",
  });
}

function addImageFrame(slide, path, x, y, w, h) {
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w,
    h,
    fill: { color: C.white },
    line: { color: C.line, transparency: 10 },
    radius: 0.06,
  });
  slide.addImage({ path, x: x + 0.08, y: y + 0.08, w: w - 0.16, h: h - 0.16 });
}

function cover() {
  const slide = pptx.addSlide();
  slide.background = { color: "F3F7FE" };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 7.5,
    fill: { color: "F3F7FE" },
    line: { color: "F3F7FE" },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 0.28,
    h: 7.5,
    fill: { color: C.blue },
    line: { color: C.blue },
  });
  slide.addText("情報通信\nシミュレーション", {
    x: 0.82,
    y: 1.1,
    w: 6.2,
    h: 1.7,
    fontFace: "Yu Gothic",
    fontSize: 32,
    bold: true,
    color: C.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addText("Random Waypoint による端末移動と情報拡散の比較（20回平均）", {
    x: 0.86,
    y: 3.05,
    w: 6.4,
    h: 0.34,
    fontFace: "Yu Gothic",
    fontSize: 13,
    color: C.muted,
    margin: 0,
  });
  addChip(slide, "1000m x 1000m", 0.86, 3.65, C.blue);
  addChip(slide, "1000 time steps", 3.28, 3.65, C.green);
  addChip(slide, "50 / 100 / 150m", 5.7, 3.65, C.orange);
  slide.addShape(pptx.ShapeType.line, {
    x: 8.1,
    y: 0.85,
    w: 0,
    h: 5.85,
    line: { color: C.line, width: 1 },
  });
  addMetric(slide, "端末数（基本実験）", "20", 8.58, 1.32, C.blue);
  addMetric(slide, "移動速度", "10m", 10.7, 1.32, C.green);
  addMetric(slide, "記録間隔", "100", 8.58, 3.0, C.orange);
  addMetric(slide, "限定領域実験", "N=100", 10.7, 3.0, C.blue);
  slide.addText("要点: 乱数によるばらつきを抑えるため、各条件を20回実行して平均値で比較する。", {
    x: 8.58,
    y: 5.12,
    w: 3.95,
    h: 0.58,
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
  addTitle(slide, "シミュレーションの流れ", "端末をランダム配置し、Random Waypoint モデルで移動させながら受信済み端末数の平均を記録する。");
  addBulletBlock(
    slide,
    [
      "1000m x 1000m の領域に端末を配置する",
      "端末同士が近づきすぎないよう最小距離を設定する",
      "各端末はランダムな目的地へ等速 10m/単位時間で移動する",
      "情報を持つ T0 から一定距離以内に入ると受信済みになる",
      "各条件を20回実行し、時刻ごとの受信数を平均する",
    ],
    0.75,
    1.85,
    5.4,
    4.2,
    "実装している処理"
  );
  slide.addShape(pptx.ShapeType.rect, {
    x: 6.75,
    y: 1.74,
    w: 5.75,
    h: 4.45,
    fill: { color: C.white },
    line: { color: C.line },
  });
  const steps = [
    ["1", "初期配置", "20点をランダム配置"],
    ["2", "移動", "1000単位時間くり返し"],
    ["3", "通信判定", "距離条件と領域条件を確認"],
    ["4", "集計", "100, 200, ... , 1000で記録"],
  ];
  steps.forEach((s, i) => {
    const y = 2.05 + i * 0.9;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: 7.15,
      y,
      w: 0.42,
      h: 0.42,
      fill: { color: C.blue },
      line: { color: C.blue },
    });
    slide.addText(s[0], {
      x: 7.15,
      y: y + 0.11,
      w: 0.42,
      h: 0.12,
      fontFace: "Yu Gothic",
      fontSize: 9,
      bold: true,
      color: C.white,
      align: "center",
      margin: 0,
    });
    slide.addText(s[1], {
      x: 7.78,
      y: y - 0.03,
      w: 2.0,
      h: 0.24,
      fontFace: "Yu Gothic",
      fontSize: 12,
      bold: true,
      color: C.ink,
      margin: 0,
    });
    slide.addText(s[2], {
      x: 7.78,
      y: y + 0.28,
      w: 3.9,
      h: 0.22,
      fontFace: "Yu Gothic",
      fontSize: 9.5,
      color: C.muted,
      margin: 0,
    });
  });
  addFooter(slide, "2");
}

function fullAreaSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "実験1");
  addTitle(slide, "全領域での通信距離比較", "通信距離が長いほどT0のみでも受信数は増え、拡散ありでは短時間で全端末に到達しやすい。");
  addImageFrame(slide, `${IMG_DIR}/original_average_non_comm_area.png`, 0.55, 1.62, 8.15, 4.88);
  addBulletBlock(
    slide,
    [
      "50mではT0のみの到達が遅く、最終平均16.2/20",
      "100mではT0のみで最終平均19.6/20まで到達",
      "150mではT0のみでも最終平均19.9/20",
      "拡散ありでは50mでも400時点で平均20/20に到達",
    ],
    9.08,
    1.82,
    3.45,
    3.75,
    "読み取り"
  );
  addFooter(slide, "3");
}

function limitedAreaSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "実験2");
  addTitle(slide, "通信可能領域を中央に限定した比較", "通信できる場所を中央に限定すると、領域が小さいほどT0のみの到達数が大きく下がる。");
  addImageFrame(slide, `${IMG_DIR}/original_average_limited_area_exp1.png`, 0.55, 1.62, 8.15, 4.88);
  addBulletBlock(
    slide,
    [
      "全領域ではT0のみでも最終平均97.7/100",
      "100x100領域ではT0のみが最終平均12.9/100",
      "200x200領域では拡散ありが最終平均98.9/100",
      "限定領域ではT0や中継端末が領域内にいる時間が重要になる",
    ],
    9.08,
    1.82,
    3.45,
    3.75,
    "読み取り"
  );
  addFooter(slide, "4");
}

function areaSizeSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "実験3");
  addTitle(slide, "通信領域サイズを変えた比較", "中央領域を広くすると、拡散ありではより早く全体へ到達する。");
  addImageFrame(slide, `${IMG_DIR}/original_average_area_size_exp2.png`, 0.55, 1.62, 8.15, 4.88);
  addBulletBlock(
    slide,
    [
      "100x100でも拡散ありは最終平均87.5/100まで到達",
      "200x200以上では拡散ありが最終平均99/100以上",
      "T0のみは領域サイズの影響を強く受ける",
      "平均化により、領域サイズが大きいほど受信数が増える傾向が見やすくなった",
    ],
    9.08,
    1.82,
    3.45,
    3.95,
    "読み取り"
  );
  addFooter(slide, "5");
}

function nodeCountSlide() {
  const slide = pptx.addSlide();
  addBase(slide, "実験4");
  addTitle(slide, "端末数を変えた比較", "端末数が増えると、拡散ありでは受信済み端末が中継点となり高い受信率になりやすい。");
  addImageFrame(slide, `${IMG_DIR}/original_average_node_count_exp3.png`, 0.55, 1.62, 8.15, 4.88);
  addBulletBlock(
    slide,
    [
      "拡散ありでは全条件で平均92%以上に到達",
      "N=100以上では拡散ありがほぼ100%に到達",
      "T0のみの受信率はおよそ38〜44%で大きく伸びにくい",
      "端末が増えるほど中継機会が増え、拡散の効果が安定する",
    ],
    9.08,
    1.82,
    3.45,
    4.1,
    "読み取り"
  );
  addFooter(slide, "6");
}

function summarySlide() {
  const slide = pptx.addSlide();
  addBase(slide, "まとめ");
  addTitle(slide, "結果のまとめ", "20回平均により、通信範囲、通信可能領域、情報拡散の有無による傾向が見やすくなった。");
  slide.addText("分かったこと", {
    x: 0.75,
    y: 1.78,
    w: 4.8,
    h: 0.34,
    fontFace: "Yu Gothic",
    fontSize: 15,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  addBulletBlock(
    slide,
    [
      "通信距離が長いほどT0のみでも情報が届きやすい",
      "受信済み端末も送信すると、到達速度と最終受信数が大きく改善する",
      "通信可能領域を中央に限定すると、領域サイズが結果を左右する",
      "端末数が増えると、拡散ありでは中継機会が増えて高い受信率になりやすい",
    ],
    0.95,
    2.35,
    5.45,
    3.5,
    ""
  );
  slide.addShape(pptx.ShapeType.rect, {
    x: 7.15,
    y: 1.72,
    w: 4.75,
    h: 3.85,
    fill: { color: C.white },
    line: { color: C.line },
  });
  slide.addText("次に改善できる点", {
    x: 7.45,
    y: 2.08,
    w: 3.2,
    h: 0.28,
    fontFace: "Yu Gothic",
    fontSize: 14,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  addBulletBlock(
    slide,
    [
      "平均だけでなく標準偏差もグラフに加える",
      "試行回数を増やして結果をさらに安定させる",
      "通信領域に入った時間の割合も分析する",
    ],
    7.45,
    2.65,
    4.05,
    2.1,
    ""
  );
  addFooter(slide, "7");
}

cover();
setupSlide();
fullAreaSlide();
limitedAreaSlide();
areaSizeSlide();
nodeCountSlide();
summarySlide();

pptx.writeFile({ fileName: OUT });
