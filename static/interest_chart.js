"use strict";


const ctx = document.getElementById("myChart").getContext('2d');
const myChart = new Chart.Line(ctx, {
    data: {
        labels: $("#myChart").data("chart").label1,
        datasets: [{
            label: $("#salary-table").data("company-name"),
            data: $("#myChart").data("chart").label2,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
            pointHoverBackgroundColor : "rgba(255, 99, 132, 1)",
            pointHoverBorderColor : "rgba(255, 99, 132, 0.2)",
            pointHoverBorderWidth : 2,
            pointHitRadius : 10,
        }]
    },
    options: {
        scales: {
            xAxes: [{
                      display: true,
                      ticks: {
                          callback: function(dataLabel, index) {
                              return index % 2 === 0 ? dataLabel : '';
                          }
                      }
            }],
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }],
        }
    }
});
