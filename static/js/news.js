"use strict";

document.getElementById("myChart").onclick = function(evt){

            const activePoints = myChart.getElementsAtEvent(evt);
            const firstPoint = activePoints[0];
            const date = myChart.data.datasets[0].data[firstPoint._index].x;
            let company_data = { "company_name" : $("#chart").data("label-name"), "from" : date };
            const url = "news.json";

            $.get(url, company_data, (response) => {
                console.log(response);

                if (response.length === 0) {

                    const msg = `
                                    <div class="alert alert-info" id="news-alert" role="alert">
                                        News not found.
                                    </div>
                                `;
                        $("#news-article").html(msg);
                    }

                else {
                    const newsList = [];
                    
                    for (let r of response) {

                        let newsImg = r.urlToImage;
                        
                        if (newsImg === null) {
                            newsImg = "/static/images/placeholder.png";
                        }

                        // card news design source ::: https://www.louistiti.fr/tutoriel-html5-css3-carte-article-ui/33
                        
                        let article = 

                        `
                         <span class="news-span">
                            <div class="card">
                                <div class="card-header"><img id="news-img" src="${newsImg}">
                                    <div class="card-header-mask">
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="card-body-header">
                                        <div class="card-body-header-category">${r.publishedAt.substring(0,10)}</div>
                                        <h1 class="title">${r.title}</h1>
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

                        $("#news-article").html(newsList);
                        // console.log(response);

                    }
                
            });
        };

$("#more").click(function(){
        $('#news-article').animate({ height: $('#news-article').get(0).scrollHeight
                                     }, 1000, function(){
                                                        $(this).height('auto');
                                     });
                                   });

$("#fold").click(function(){
        $('#news-article').animate({ height: 553 }, 1000);
                           });



function recentNews() {

    let company_data = { "company_name" : $("#chart").data("label-name") };
    const recentUrl = "recent_news.json";
    
    $.get(recentUrl, company_data, (response) => {
                    console.log(response);

                    if (response.length === 0) {

                        const msg = "News not found.";
                        $('#news-article').html(msg);
                    }

                    else {
                        const recentNewsList = [];
                        
                        for (let r of response) {

                            let newsImg = r.urlToImage;
                            
                            if (newsImg === null) {
                                newsImg = "/static/images/placeholder.png";
                            }

                            // card news design source ::: https://www.louistiti.fr/tutoriel-html5-css3-carte-article-ui/33
                            
                            let recentArticle = 

                            `
                             <span class="news-span">
                                <div class="card">
                                    <div class="card-header"><img id="news-img" src="${newsImg}">
                                        <div class="card-header-mask">
                                        </div>
                                    </div>
                                    <div class="card-body">
                                        <div class="card-body-header">
                                            <div class="card-body-header-category">${r.publishedAt.substring(0,10)}</div>
                                            <h1 class="title">${r.title}</h1>
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
                            `;
                            recentNewsList.push(recentArticle);
                            
                            }

                            $("#news-article").html(recentNewsList);
                            // console.log(response);

                        }
                    
                });
}

recentNews();

