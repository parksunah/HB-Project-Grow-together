// css source ::: https://codemyui.com/gooey-circular-spinner/

// Loading fuction for homepage.
function loading(){
    let loadingDiv = `
                        <div class="container" id="dot-container">
                            <div class="dot dot-1"></div>
                            <div class="dot dot-2"></div>
                            <div class="dot dot-3"></div>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                          <defs>
                            <filter id="goo">
                              <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                              <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 21 -7"/>
                            </filter>
                            </defs>
                        </svg>
                    `
    $("#loading").html(loadingDiv);
    $("#loading").show();
    $("#content").hide();       
}

// Loading fuction for main page.
function loading2(){
    let loadingDiv = `
                        <div class="dot-container">
                            <div class="dot dot-1"></div>
                            <div class="dot dot-2"></div>
                            <div class="dot dot-3"></div>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                          <defs>
                            <filter id="goo">
                              <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                              <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 21 -7"/>
                            </filter>
                            </defs>
                        </svg>
                    `
    $("#loading2").html(loadingDiv);
    $("#loading2").show();
    $("#wrapper").hide();       
}

// Loading fuction for ranking page.
function loading3(){
    let loadingDiv = `
                        <div class="dot-container">
                            <div class="dot dot-1"></div>
                            <div class="dot dot-2"></div>
                            <div class="dot dot-3"></div>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                          <defs>
                            <filter id="goo">
                              <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                              <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 21 -7"/>
                            </filter>
                            </defs>
                        </svg>
                    `
    $("#loading3").html(loadingDiv);
    $("#loading3").show();
    $("#ranking-wrapper").hide();       
}