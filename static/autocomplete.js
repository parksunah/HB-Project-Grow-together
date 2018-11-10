"use strict";

    $(document).ready(function () {
    const companies=[];
    function loadCompanies(){
        $.getJSON('/companies', function(data, status, xhr){
            for (let i = 0; i < data.length; i++ ) {
                companies.push(data[i].name);
            }
    });
    };
    loadCompanies();
    $("#company").autocomplete({
                    source: companies, 
                    minLength:3
                });
    });
