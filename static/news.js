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

                    const newsImg = r.urlToImage;
                    if (newsImg === "null") {
                        newsImg = "/static/images/placeholder.png";
                    }

                    console.log(newsImg);

                    // card news design source ::: https://www.louistiti.fr/tutoriel-html5-css3-carte-article-ui/33
                    const article = 

                    `
                     <span>
                        <div class="card">
                            <div class="card-header"><img id="news-img" src="${newsImg}">
                                <div class="card-header-mask">
                                </div>
                            </div>
                            <div class="card-body">
                                <div class="card-body-header">
                                    <div class="card-body-header-category">${r.publishedAt}</div>
                                    <h1>${r.title}</h1>
                                    <p class="card-body-header-sentence">
                                        ${r.source.name}</span>
                                    </p>
                                </div>
                                <p class="card-body-description">
                                    ${r.description}
                                </p>
                                <div class="card-body-footer">
                                    <a href="${r.url}" target="_blank"> Read More.. </a>
                                </div>
                            </div>
                        </div>
                    </span>
                    `
                    newsList.push(article);
                    
                    }

                    // console.log(newsList.length);
                    $('#news-article').html(newsList);
                    // console.log(response);

                }
                
    });
        };


// <div>
//                       <h3> ${r.title}</h3>
//                       <p>  ${r.publishedAt} </p>
//                       <p>  ${r.source.name} </p>
//                       <p>  ${r.publishedAt} </p>
//                       <p>  ${r.url} </p>
//                       <p>  ${r.description} </p>
//                       <p>  ${r.urlToImage} </p>
//                     </div>




