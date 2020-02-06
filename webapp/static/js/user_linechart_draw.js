var framesize = {width: 900, height: 300}; // 960, 500
var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = framesize.width - margin.left - margin.right,
    height = framesize.height - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y%m%d").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

/*
var data = [
    { "date": "20111001",
      "Exploring Resources": 63.4,
      "Taking Exercises": 62.7,
      "Social Interaction": 72.2
    },
    { "date": "20111002",
      "Exploring Resources": 58.0,
      "Taking Exercises": 59.9,
      "Social Interaction": 67.7
    },
    { "date": "20111003",
      "Exploring Resources": 53.3,
      "Taking Exercises": 59.1,
      "Social Interaction": 69.4
    },
    { "date": "20111004",
      "Exploring Resources": 55.7,
      "Taking Exercises": 58.8,
      "Social Interaction": 68.0
    },
    { "date": "20111005",
      "Exploring Resources": 64.2,
      "Taking Exercises": 58.7,
      "Social Interaction": 72.4
    }
  ]
*/
color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

data.forEach(function(d) {
    console.log(d.date)
    d.date = parseDate(d.date);
  });

var cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, value: +d[name]};
      })
    };
  });

x.domain(d3.extent(data, function(d) { return d.date; }));

y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.value; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.value; }); })
  ]);

svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Activity Count");

var attribute = svg.selectAll(".attribute")
      .data(cities)
    .enter().append("g")
      .attr("class", "attribute");

attribute.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .attr("data-legend",function(d) { return d.name})
      .style("stroke", function(d) { return color(d.name); });

attribute.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.value) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });


legend = svg.append("g")
    .attr("class","legend")
    .attr("transform","translate(50,30)")
    .style("font-size","12px")
    .call(d3.legend)