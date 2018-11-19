"use strict";

const ctx = document.getElementById("myChart").getContext('2d');
const myChart = new Chart.Line(ctx, {
    
    data: {
    datasets: [{
            label: $("#chart").data("label-name"),
            data: $("#myChart").data("chart"),
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
                      type: 'time',
              time: {
                      unit: 'month',
                      unitStepSize: 2,
                      min: $("#myChart").data("chart")[0].x,
                      max: $("#myChart").data("chart")[155].x
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
