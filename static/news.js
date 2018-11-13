"use strict";

document.getElementById("myChart").onclick = function(evt){
            const activePoints = myChart.getElementsAtEvent(evt);
            const firstPoint = activePoints[0];
            const label = myChart.data.labels[firstPoint._index];
            const value = myChart.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
            let company_data = { "company_name" : $("#salary-table").data("company-name"), "from" : label};
            
            const url = "news.json";
            $.get(url, company_data, (response) => {
                console.log(response);

                if (response.length === 0) {
                    console.log("msg");
                    const msg = "News not found.";
                    alert(msg);
                    $('#news-article').html(msg);
                }

                else {
                    const newsList = [];
                    
                    for (let r of response) {

                    const article = 

                    `<div>
                      <h3> ${r.title}</h3>
                      <p>  ${r.publishedAt} </p>
                      <p>  ${r.url} </p>
                      <p>  ${r.description} </p>
                    </div>
                    `
                    newsList.push(article);
                    
                    }

                    // console.log(newsList.length);
                    $('#news-article').html(newsList);
                    // console.log(response);

                }
                
    });
        };
