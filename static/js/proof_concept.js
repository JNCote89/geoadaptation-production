/* Script to generate the Folium IFrame from the JSon returned in the template. The goal is to avoid
* using the Django tag {{ map|safe}} for security reasons */
map_iframe = JSON.parse(document.getElementById('map_COVID').textContent);
document.getElementById('map_covid').innerHTML = map_iframe
document.getElementById('map_covid').firstElementChild.setAttribute("sandbox", "")

/* The initial values are from the government official data. It has been stored in a div in the HTML template
   from the django backend and we parse it here. */
covid_data = JSON.parse(document.getElementById('covid_data').textContent);

/* Variables to name the cells. We could use strictly indexes, but it's easier to debug with explicit names. Each time
* we refer to the Input Id of the first dose we call cellNameIOArray[0][0], for the Output Id it's
* cellNameIOArray[0][1] and so on... */
cellNameIOArray = [["FstDoseInput", "FstDoseOutput"], ["ScdDoseInput", "ScdDoseOutput"], ["CONNECTLagInput", "CONNECTLagOutput"]]

/* Variable of the table Id in the HTML template. To be called when we modify its content */
tableCOVIDStats = document.getElementById('COVID_table_stats');

/* Number of regions in the database */
numberOfRegions = covid_data["region"].length

/* Function to update the value of a cell in the table. It creates a slider and a label with the slider's value.
* The goal is to let the user input a percentage as an integer from 0 to 100. */
function cellValue(value, input, output, index) {
   return `<td><input type="range" min="0" max="100" value=${value} id=${input}${index} class="UserInputs"> 
               <output for=${input}${index} id=${output}${index}>${value} %</output></td>`;
}


/* Function to create a table from our data. I could have made this a bit shorter, but I made it explicit so it's
* easier to grasp what's going on in the other functions calling the indexes of the table. */
function createTable () {

    /* We add a row for each regions in our data. We start from the last one so it appears at the bottom of the table.
    * We add a row at the index 1 to start after the headers set in the HTML template. */
    for (let i = numberOfRegions; i > 0; i--) {
        row = tableCOVIDStats.insertRow(1);

        /*The index zero correspond to the name of the region. It never changes once its set here */
        cellRegion = row.insertCell(0);
        cellRegion.innerHTML = `<th>${covid_data["region"][i-1]}</th>`;

        /* The index 1 refer to the column where the value for the first dose is set. Each time we need to change its
        * value, we refer to the index 1 for the table column and the index [0] in the cellNameIOArray */
        cellFstDose = row.insertCell(1);
        cellFstDose.innerHTML = cellValue((covid_data.first_dose[i-1]*100).toFixed(0), cellNameIOArray[0][0], cellNameIOArray[0][1], i)

        /* The index 1 refer to the column where the value for the second dose is set. Each time we need to change its
        * value, we refer to the index 2 for the table column and the index [1] in the cellNameIOArray */
        cellScdDose = row.insertCell(2);
        cellScdDose.innerHTML = cellValue((covid_data.second_dose[i-1]*100).toFixed(0), cellNameIOArray[1][0], cellNameIOArray[1][1], i)

        /* The index 1 refer to the column where the value for the second dose is set. Each time we need to change its
        * value, we refer to the index 3 for the table column and the index [2] in the cellNameIOArray */
        cellCONNECT = row.insertCell(3);
        cellCONNECT.innerHTML = cellValue((covid_data.CONNECT_lag[i-1]*100).toFixed(0), cellNameIOArray[2][0], cellNameIOArray[2][1], i)
    }
}

/* We call the function to create the table */
createTable()


/* Function to update the label of the sliders when the user change the value. */
function sliderLabel(input, output, index) {
    document.querySelector(output.concat(index)).value = $(input.concat(index)).val() + " %";
}

/* Function to iterate through every sliders and apply the function sliderLabel on each cell so it can get updated */
function updateSliders(){
    $('.UserInputs').on("input", function (){
        for (let i = 16; i > 0; i--) {
            cellNameIOArray.forEach(item => sliderLabel(`#${item[0]}`, `#${item[1]}`, i))
        }
    });
}

/* We call the function to update every slider each time the user interact with the sliders */
updateSliders()

/*This function update the dashboard with randomize data when the user click on the randomizeData button create in
* the HTML template */
$('#randomizeData').on("click", function (){
    for (let i = 16; i > 0 ; i--) {

        /* The values are set randomly. There is a condition to make sure the second dose doesn't exceed the first
        * dose percentage and is above 0. */
        first_dose_random = Math.floor(Math.random() * 101)
        second_dose_random = first_dose_random - Math.floor(Math.random() * 26)
        CONNECT_lag_random = Math.floor(Math.random() * 101)

        if (second_dose_random < 0){
            second_dose_random = 0
        }

        /* We update the cells for the first dose (index 1), second dose (index 2) and the connect study value (index 3) for each
        * row (i) in the table. */
        tableCOVIDStats.rows[i].cells[1].innerHTML = cellValue(first_dose_random, cellNameIOArray[0][0], cellNameIOArray[0][1],i)
        tableCOVIDStats.rows[i].cells[2].innerHTML = cellValue(second_dose_random, cellNameIOArray[1][0], cellNameIOArray[1][1],i)
        tableCOVIDStats.rows[i].cells[3].innerHTML = cellValue(CONNECT_lag_random, cellNameIOArray[2][0], cellNameIOArray[2][1],i)

        /* We recall the function to update every slider each time the user interact with the sliders in each function*/
        updateSliders()
    }
});

/* Function to set the vaccination to zero when the user press the noVacination button in the HTML template */
$('#noVaccination').on("click", function (){
    for (let i = 16; i > 0 ; i--) {
        first_dose_none = 0
        second_dose_none = 0

        tableCOVIDStats.rows[i].cells[1].innerHTML = cellValue(first_dose_none, cellNameIOArray[0][0], cellNameIOArray[0][1],i)
        tableCOVIDStats.rows[i].cells[2].innerHTML = cellValue(second_dose_none, cellNameIOArray[1][0], cellNameIOArray[1][1],i)
        updateSliders()
    }
});

/* Function to set the vaccination between 11 and 25 % when the user press the lowVacination button
in the HTML template */
$('#lowVaccination').on("click", function (){
    for (let i = 16; i > 0 ; i--) {
        first_dose_random = 11 + Math.floor(Math.random() * 15)
        second_dose_random = first_dose_random - Math.floor(Math.random() * 10)

        tableCOVIDStats.rows[i].cells[1].innerHTML = cellValue(first_dose_random, cellNameIOArray[0][0], cellNameIOArray[0][1],i)
        tableCOVIDStats.rows[i].cells[2].innerHTML = cellValue(second_dose_random, cellNameIOArray[1][0], cellNameIOArray[1][1],i)
        updateSliders()
        }
});

/* Function to set the vaccination between 70 and 90 % when the user press the highVacination button
in the HTML template */
$('#highVaccination').on("click", function (){
    for (let i = 16; i > 0 ; i--) {
        first_dose_random = 70 + Math.floor(Math.random() * 20)
        second_dose_random = first_dose_random - Math.floor(Math.random() * 15)

        if (second_dose_random < 0){
            second_dose_random = 0
        }
        tableCOVIDStats.rows[i].cells[1].innerHTML = cellValue(first_dose_random, cellNameIOArray[0][0], cellNameIOArray[0][1],i)
        tableCOVIDStats.rows[i].cells[2].innerHTML = cellValue(second_dose_random, cellNameIOArray[1][0], cellNameIOArray[1][1],i)
        updateSliders()
    }
});

/* Function to set the social contact from the CONNECT study between 15 and 28 % when the user press the
lowSocialContact button in the HTML template */
$('#lowSocialContact').on("click", function (){
    for (let i = 16; i > 0 ; i--) {
        CONNECT_lag_random = 15 + Math.floor(Math.random() * 13)
        tableCOVIDStats.rows[i].cells[3].innerHTML = cellValue(CONNECT_lag_random, cellNameIOArray[2][0], cellNameIOArray[2][1],i)
        updateSliders()
    }
});

/* Function to set the social contact from the CONNECT study between 70 and 90 % when the user press the
highSocialContact button in the HTML template */
$('#highSocialContact').on("click", function (){
    for (let i = 16; i > 0 ; i--) {
        CONNECT_lag_random = 70 + Math.floor(Math.random() * 20)

        tableCOVIDStats.rows[i].cells[3].innerHTML = cellValue(CONNECT_lag_random, cellNameIOArray[2][0], cellNameIOArray[2][1],i)
        updateSliders()
    }
});

/* Function to launch the prediction with the AI based on the value in the table when the user click the
predict button */
$("#predict").on("click", function() {

        document.getElementById("loadingLayerCOVID").setAttribute("style", "display:inline;");

        /* Array to store the value in the dashboard */
        dose_1 = []
        dose_2 = []
        connect_covid = []

        /* Variable to get the url of the page to make it easier to set the langage */
        dynamic_url = $("#dynamic_url_covid").val();

        /* loop to collect the info in the table so the AI can adjust the predictions on the map */
        for (let i = 1; i < 17; i++) {
            dose_1.push(document.querySelector(`#${cellNameIOArray[0][0]}`.concat(i)).value.replace('%','').trim()/100)
            dose_2.push(document.querySelector(`#${cellNameIOArray[1][0]}`.concat(i)).value.replace('%','').trim()/100)
            connect_covid.push(document.querySelector(`#${cellNameIOArray[2][0]}`.concat(i)).value.replace('%','').trim()/100)
    }
        /* Typical ajax post request. The dynamic_url is based on the dynamic_url_uhi div to get the path of the page.
        * It can change depending of the langage (/fr/ or /en/. Since Django Tag can't be used in a JS file, this is
        * a small trick to get easily the information we need. */
        $.ajax({
            type: "POST",
            url: dynamic_url,
            data : {
                "dose_1": dose_1,
                "dose_2": dose_2,
                "connect_covid": connect_covid,
                "csrfmiddlewaretoken":$('input[name=csrfmiddlewaretoken]').val(),
            },
            /* The function return the map updated */
            success: function(data) {
            $('#map_covid').html(data.map_COVID_updated)
            document.getElementById("loadingLayerCOVID").setAttribute("style", "display:none;");
            updateSliders()
            }
            });
        });