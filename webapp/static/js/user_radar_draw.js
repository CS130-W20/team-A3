RadarChart.defaultConfig.color = function() {};
RadarChart.defaultConfig.radius = 3;
RadarChart.defaultConfig.w = 330;
RadarChart.defaultConfig.h = 330;
/*
var data = [
  {
    className: 'Long-Term', // optional can be used for styling
    axes: [
      {axis: "participation", value: 12}, 
      {axis: "breadth of knowledge", value: 6}, 
      {axis: "contribution", value: 5},  
      {axis: "social interaction", value: 9},  
      {axis: "mastery of skills", value: 2}
    ]
  },
  {
    className: 'Recent',
    axes: [
      {axis: "variety of knowledge", value: 6}, 
      {axis: "intelligence", value: 7}, 
      {axis: "charisma", value: 10},  
      {axis: "dexterity", value: 12},  
      {axis: "luck", value: 9}
    ]
  }
];
*/
function randomDataset() {
  return data.map(function(d) {
    return {
      className: d.className,
      axes: d.axes.map(function(axis) {
        //return {axis: axis.axis, value: Math.ceil(Math.random() * 10)};
        return {axis: axis.axis, value: axis.value};
      })
    };
  });
}
var chart = RadarChart.chart();
var cfg = chart.config(); // retrieve default config
var svg = d3.select('#analyze_radar').append('svg')
  .attr('width', cfg.w)
  .attr('height', cfg.h);
svg.append('g').classed('single', true).datum(randomDataset()).call(chart); 

d3.select('#analyze_radar').select('svg').selectAll('polygon')
  .attr("data-legend", function(d) {return d.className}) //;
  .attr("title", function(d) {return d.className});

d3.select('#analyze_radar').select('svg')
  .attr("class", function(d,i) { console.log(d); return d; })

legend = svg.append("g")
    .attr("class","legend")
    .attr("transform","translate(50,30)")
    .style("font-size","12px")
    .call(d3.legend);


