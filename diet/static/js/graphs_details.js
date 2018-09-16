google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {


  var caloriesData = google.visualization.arrayToDataTable(caloriesHash['calories_data']);

  var caloriesOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: {
      position: 'labeled'
    },
    slices: pastelColors,
    chartArea:{left:0,top:20,width:'100%',height:'90%'}
  };

  var carbData = google.visualization.arrayToDataTable(carbsHash['carbs_data']);

  var carbOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: 'none',
    slices: pastelColors,
    chartArea:{left:15,top:10,width:'90%',height:'90%'}
  };

  var proteinData = google.visualization.arrayToDataTable(proteinHash['protein_data']);

  var proteinOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: 'none',
    slices: pastelColors,
    chartArea:{left:15,top:10,width:'90%',height:'90%'}
  };

  var fatData = google.visualization.arrayToDataTable(fatHash['fat_data']);

  var fatOptions = {
    pieHole: 0.4,
    pieSliceTextStyle: {
      color: 'black',
    },
    legend: 'none',
    slices: pastelColors,
    chartArea:{left:15,top:10,width:'90%',height:'90%'}
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
