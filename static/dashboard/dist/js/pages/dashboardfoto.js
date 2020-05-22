$(function () {

  'use strict'

  /* ChartJS
   * -------
   * Here we will create a few charts using ChartJS
   */

  //-----------------------
  //- MONTHLY SALES CHART -
  //-----------------------

  // Get context with jQuery - using jQuery's .get() method.
  var salesChartCanvas = $('#salesChart').get(0).getContext('2d');

  var arrayJSON = JSON.parse(array_compras.replace(/&quot;/g,'"'));

  var prettyArray = []
  for (let item of arrayJSON) {
    prettyArray.push(item.fields)
  }

  var fechasComprasArray = [];
  var dataComprasArray = [];

  for (let item of prettyArray) {
    fechasComprasArray.push(item.fecha);
    dataComprasArray.push(item.compras);
  }

  var salesChartData = {
    labels  : fechasComprasArray,
    datasets: [
      {
        label               : 'Ventas',
        backgroundColor     : 'rgba(60,141,188,0.9)',
        borderColor         : 'rgba(60,141,188,0.8)',
        pointRadius          : false,
        pointColor          : '#3b8bba',
        pointStrokeColor    : 'rgba(60,141,188,1)',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(60,141,188,1)',
        data                : dataComprasArray
      }
    ]
  }


  var salesChartOptions = {
    maintainAspectRatio : false,
    responsive : true,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines : {
          display : false,
        }
      }],
      yAxes: [{
        gridLines : {
          display : false,
        }
      }]
    }
  }

  // This will get the first returned node in the jQuery collection.
  var salesChart = new Chart(salesChartCanvas, {
      type: 'bar',
      data: salesChartData,
      options: salesChartOptions
    }
  )




})
