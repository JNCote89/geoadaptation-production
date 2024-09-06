/* This script is used only with the proof_concept_COVID template */

/* Script to generate the Folium IFrame from the JSon returned in the magog_uhi template. The goal is to avoid
* using the Django tag {{ map|safe}} for security reasons */
map_iframe = JSON.parse(document.getElementById('magog_map').textContent);
document.getElementById('map').innerHTML = map_iframe
document.getElementById('map').firstElementChild.setAttribute("sandbox", "")

/* Function to manage the JQuery UI tabs for the graphs widget */
$(function () {
    $("#tabs").tabs({"active":"daily_graph", heightStyle:"auto"});
});

/*Function to manage the opacity slider and change it's value in real time */
$('#opacitySlider').on('input',function (){
    document.querySelector('#opacityValue').value=$("#opacitySlider").val() + " %";
});

/* Function to change the rendering of the Dasboard if the user change any settings in the menu bar */
$("#inputDate,#inputTime,#opacitySlider,#inputColor").change(function() {

    document.getElementById("invalidDate").setAttribute("style", "display:none;");
    min_date = new Date (document.getElementById("inputDate").getAttribute("min")).getTime();
    max_date = new Date (document.getElementById("inputDate").getAttribute("max")).getTime();
    selected_date = new Date (document.getElementById("inputDate").value).getTime();

    /* Condition to make sure the selected date is valid. If it's the case there is a POST request to update the
    * dashboard */
    if (selected_date >= min_date && selected_date <= max_date) {

        /* Label to indicate the layer is loading */
        document.getElementById("loadingLayer").setAttribute("style", "display:inline;");

        date = $("#inputDate").val();
        num_time = $("#inputTime").val();
        opacity = $('#opacitySlider').val();
        color = $("#inputColor").val();
        dynamic_url = $("#dynamic_url_uhi").val();

        /* Typical ajax post request. The dynamic_url is based on the dynamic_url_uhi div to get the path of the page.
        * It can change depending of the langage (/fr/ or /en/. Since Django Tag can't be used in a JS file, this is
        * a small trick to get easily the information we need. */
        $.ajax({
            type: "POST",
            url: dynamic_url,
            data : {
                "num_date": date,
                "num_time": num_time,
                "opacity": opacity,
                "color" : color,
                "csrfmiddlewaretoken":$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data) {

                /* If the request went through, all the information in the template is updated */
                time = data.times_list

                let html_data_time = "";

                time.forEach(function (time ,i) {
                    html_data_time += `<option value="${time}">${time}:00</option>`
                });

                $("#inputTime").html(html_data_time);
                document.getElementById("inputTime").value = data.time;
                $("#map").html(data.magog_map_updated);
                $("#t_avg_100m").html(data.t_avg_100m_updated);
                $("#t_avg_200m").html(data.t_avg_200m_updated);
                $("#t_avg_300m").html(data.t_avg_300m_updated);
                $("#t_avg_400m").html(data.t_avg_400m_updated);
                $("#t_max_100m").html(data.t_max_100m_updated);
                $("#t_max_200m").html(data.t_max_200m_updated);
                $("#t_max_300m").html(data.t_max_300m_updated);
                $("#t_max_400m").html(data.t_max_400m_updated);
                $("#monthly_max_graph img").attr('src', data.monthly_max_graph_updated);
                $("#daily_max_graph img").attr('src', data.daily_max_graph_updated);
                $("#monthly_avg_graph img").attr('src', data.monthly_avg_graph_updated);
                $("#daily_avg_graph img").attr('src', data.daily_avg_graph_updated);
                document.getElementById("loadingLayer").setAttribute("style", "display:none;");
            }
            });
        }
    /* In the case the date is not valid, a message is displayed to ask the user to choose between the first date of the
    * database and the last entry */
    else {
        min_date = document.getElementById("inputDate").getAttribute("min");
        max_date = document.getElementById("inputDate").getAttribute("max");
        document.getElementById("invalidDate").setAttribute("style", "display:inline;");
    }
});