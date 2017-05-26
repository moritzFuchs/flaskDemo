var active_stocks = [];

$(function() {
    
    $("#stock_names").tagsInput({
       'height':'100px',
       'width':'600px',
       'interactive':true,
       'defaultText':'Add a stock token (e.g. GOOG), then press \'\,\'',
       'onAddTag':plotStocks,
       'onRemoveTag':plotStocks,
       'delimiter': [','],
       'removeWithBackspace' : true,
       'minChars' : 0,
       'maxChars' : 0, // if not provided there is no limit
       'placeholderColor' : '#666666'
    });
    
    function plotStocks(elem, elem_tags) {
       
       if($("#stock_names").val() == "") {
           return;
       }
       
       
       $("#bokeh_wrapper").append("<div id='overlay'><img src='static/loading.svg'></div>");
       
       $.getJSON("get_stock_plot", 
        {stock_names : $("#stock_names").val()},
        function(data) {
            $("#error").remove();
            $("#bokeh_wrapper").remove();
            $("#content").append("<div id='bokeh_wrapper'>" + data.div + data.script + "</div>");
            if (data.notFound != undefined) {
            
                $('.tag', elem_tags).each(function(index, tag) {
                   if ($.inArray($(tag).text().substr(0,$(tag).text().length-3), data.notFound) != -1) {
                       $(tag).addClass("badTag");
                   } 
                });
            
                html = "<div id='error'>";
                html += "The following stock tokens could not be found: ";
                html += "<ul>";
                $.each(data.notFound, function(index, value) {
                   html += "<li>" + value + "</li>"; 
                });
                html += "</ul>";
                html += "</div>";
                //$(html).insertBefore("#bokeh_wrapper");
                $("#error").fadeOut(3000);
            }
            $("#stock_name").val("");
        }
       );
    }
    
});