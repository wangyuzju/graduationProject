(function(){
  /**
   *var_dump
   */
  function var_dump(arrayLike){
    var list = Array.prototype.slice.call(arrayLike, 0);
    console.log(list.join('****'));
  }
  /**
   * 
   * @param x grid start point x -- (left, top)
   * @param y grid start point y -- (left, top)
   * @param w width value
   * @param h height value
   * @param wv divide width into wv count
   * @param hv divide height into hv count 
   * @param coordValue
   * @returns {*}
   */
  Raphael.fn.drawGrid = function (x, y, w, h, wv, hv, coordValue) {
    var color = "#ccc";
    var path = [],//["M", Math.round(x) + .5, Math.round(y) + .5, "L", Math.round(x + w) + .5, Math.round(y) + .5, Math.round(x + w) + .5, Math.round(y + h) + .5, Math.round(x) + .5, Math.round(y + h) + .5, Math.round(x) + .5, Math.round(y) + .5],
      rowHeight = h / hv,
      columnWidth = w / wv,
      stepX = (coordValue.x[1] - coordValue.x[0]) / wv,
      stepY = (coordValue.y[1] - coordValue.y[0]) / hv;
    /*Add coordinate*/
    var distance = 5;
    var coordLength = 8.5;
    var coordX = ["M", Math.round(x) + .5, Math.round(y + h + distance) + .5, "H", Math.round(x + w) + .5];
    var coordY = ["M", Math.round(x - distance) + .5, Math.round(y) + .5, "V", Math.round(y + h) + .5];
    for (var i = 0; i <= hv; i++) {
      path = path.concat(["M", Math.round(x) + .5, Math.round(y + i * rowHeight) + .5, "H", Math.round(x + w) + .5]);
      var startX = Math.round(x - distance) + .5,
        startY = Math.round(y + i * rowHeight) + .5,
        endX = Math.round(x - distance) - coordLength;
      coordY = coordY.concat(["M", startX, startY, "H", endX]);
      this.text(startX - 4 * distance, startY, coordValue.y[0] + i * stepY);
    }
    for (i = 0; i <= wv; i++) {
      path = path.concat(["M", Math.round(x + i * columnWidth) + .5, Math.round(y) + .5, "V", Math.round(y + h) + .5]);
      var startX = Math.round(x + i * columnWidth) + .5,
        startY = Math.round(y + h + distance) + .5,
        endY = Math.round(y + h + distance) + coordLength;
      coordX = coordX.concat(["M", startX, startY, "V", endY]);
      this.text(startX, startY + 3 * distance, coordValue.x[0] + i * stepX);
    }

    this.path([].concat(coordX, coordY).join(",")).attr({'stroke': '#000'});
    return this.path(path.join(",")).attr({stroke: color,'stroke-width': '1', 'stroke-dasharray': '- '});
  };
  
  var labels = [];
  labels[50]=0;
  
  var width = 1001,
    height = 581,
    leftgutter = 40,
    rightgutter = 20,
    bottomgutter = 50,
    topgutter = 20,
    colorhue = .6 || Math.random(),
    color = "hsl(" + [colorhue, .5, .5] + ")",
    //r = Raphael("holder", width, height),
    txt = {font: '12px Helvetica, Arial', fill: "#fff"},
    txt1 = {font: '10px Helvetica, Arial', fill: "#fff"},
    txt2 = {font: '12px Helvetica, Arial', fill: "#000"},
    X = (width - leftgutter) / labels.length, //every point's actually width
    //max = Math.max.apply(Math, data),
    max = 100,
    Y = (height - bottomgutter - topgutter) / max; // every point's value height
  var paper = Raphael(document.getElementById("graphic"), width, height);
  console.log(X);
  paper.drawGrid(leftgutter + X * .5 + .5, topgutter + .5, width - leftgutter - X - rightgutter,
    height - topgutter - bottomgutter, 10, 10, {x:[0,12000], y:[-2000,2000]})
  
  var st = paper.set();
  st.push(
    /*Coordinate*/
    //paper.path("M0.5,"+height/2+"L"+width+","+height/2),
    //paper.path("M10.5,0L10.5,"+height)
  )
  st.attr({
    stroke: '#000',
    'stroke-width': 1
  });

})();


