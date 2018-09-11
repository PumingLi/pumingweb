google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

  var caloriesData = google.visualization.arrayToDataTable(dietData["calories_data"]);

  var caloriesOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: {
      position: 'labeled'
    },
    chartArea:{left:0,top:10,width:'100%',height:'90%'}
  };

  var carbData = google.visualization.arrayToDataTable([
    ['Daily Serving', 'Grams'],
    ['Amount Eaten',     50],
    ['Amount Left',     50],
  ]);

  var carbOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: 'none',
    slices: {
      0: { color: '#ffcc66' },
      1: { color: '#e6e6e6' }
    },
    chartArea:{left:10,top:10,width:'80%',height:'90%'}
  };

  var proteinData = google.visualization.arrayToDataTable([
    ['Daily Serving', 'Grams'],
    ['Amount Eaten',     70],
    ['Amount Left',     50],
  ]);

  var proteinOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: 'none',
    slices: {
      0: { color: '#cc3300' },
      1: { color: '#e6e6e6' }
    },
    chartArea:{left:10,top:10,width:'80%',height:'90%'}
  };

  var fatData = google.visualization.arrayToDataTable([
    ['Daily Serving', 'Grams'],
    ['Amount Eaten',     510],
    ['Amount Left',     50],
  ]);

  var fatOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: 'none',
    slices: {
      0: { color: '#ff9999' },
      1: { color: '#e6e6e6' }
    },
    chartArea:{left:10,top:10,width:'80%',height:'90%'}
  };

  var carbChart = new google.visualization.PieChart(document.getElementById('carb-donut'));
  carbChart.draw(carbData, carbOptions);

  var proteinChart = new google.visualization.PieChart(document.getElementById('protein-donut'));
  proteinChart.draw(proteinData, proteinOptions);

  var fatChart = new google.visualization.PieChart(document.getElementById('fat-donut'));
  fatChart.draw(fatData, fatOptions);

  var caloriesChart = new google.visualization.PieChart(document.getElementById('calories-donut'));
  caloriesChart.draw(caloriesData, caloriesOptions);
}
