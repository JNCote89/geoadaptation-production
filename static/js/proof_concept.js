
/* Script to generate the Folium IFrame from the JSon returned in the template. The goal is to avoid
* using the Django tag {{ map|safe}} for security reasons */
map_iframe = JSON.parse(document.getElementById('map_COVID').textContent);
document.getElementById('map_covid').innerHTML = map_iframe
document.getElementById('map_covid').firstElementChild.setAttribute("sandbox", "")

/* Function to create a table from our data */
function createTable () {
    var table = document.getElementById('COVID_table_stats');
    var covid_data = JSON.parse(document.getElementById('covid_data').textContent);

    for (let i = 16; i > 0; i--) {
        var row = table.insertRow(1);
        var cellRegion = row.insertCell(0);
        var cellFstDose = row.insertCell(1);
        var cellScdDose = row.insertCell(2);
        var cellSocialContact = row.insertCell(3)
        cellRegion.innerHTML = `<th>${covid_data["region"][i-1]}</th>`;
        cellFstDose.innerHTML = `<td><input type="range" min="0" max="100" value="${(covid_data.first_dose[i-1]*100).toFixed(0)}" step="1" id="FstDose${i}" class="UserInputs"> <output for="FstDose${i}" id="FstDoseValue${i}"> ${(covid_data.first_dose[i-1]*100).toFixed(0)} % </output></td>`;
        cellScdDose.innerHTML = `<td><input type="range" min="0" max="100" value="${(covid_data.second_dose[i-1]*100).toFixed(0)}" step="1" id="ScdDose${i}" class="UserInputs"> <output for="ScdDose${i}" id="ScdDoseValue${i}"> ${(covid_data.second_dose[i-1]*100).toFixed(0)} % </output></td>`;
        cellSocialContact.innerHTML = `<td><input type="range" min="0" max="100" value="${(covid_data.CONNECT_lag[i-1]*100).toFixed(0)}" step="1" id="CONNECTLag${i}" class="UserInputs"> <output for="CONNECTLag${i}" id="CONNECTLagValue${i}"> ${(covid_data.CONNECT_lag[i-1]*100).toFixed(0)} % </output></td>`;
    }
}

createTable()

/* Function to manage the value sliders */
$('.UserInputs').on("input", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#FstDoseValue'.concat(i)).value = $('#FstDose'.concat(i)).val() + " %";
    document.querySelector('#ScdDoseValue'.concat(i)).value = $('#ScdDose'.concat(i)).val() + " %";
    document.querySelector('#CONNECTLagValue'.concat(i)).value = $('#CONNECTLag'.concat(i)).val() + " %";
    }
});

$('#randomizeData').on("click", function (){

    var table = document.getElementById('COVID_table_stats');

    for (let i = 16; i > 0 ; i--) {
        first_dose_random = Math.floor(Math.random() * 101)
        second_dose_random = first_dose_random - Math.floor(Math.random() * 26)
        CONNECT_lag_random = Math.floor(Math.random() * 101)

        if (second_dose_random < 0){
            second_dose_random = 0
        }
    document.getElementById('COVID_table_stats').rows[i].cells[1].innerHTML = `<td><input type="range" min="0" max="100" value="${first_dose_random}" step="1" id="FstDose${i}" class="UserInputs"> <output for="FstDose${i}" id="FstDoseValue${i}"> ${first_dose_random} % </output></td>`;
    document.getElementById('COVID_table_stats').rows[i].cells[2].innerHTML = `<td><input type="range" min="0" max="100" value="${second_dose_random}" step="1" id="ScdDose${i}" class="UserInputs"> <output for="ScdDose${i}" id="ScdDoseValue${i}"> ${second_dose_random} % </output></td>`;
    document.getElementById('COVID_table_stats').rows[i].cells[3].innerHTML = `<td><input type="range" min="0" max="100" value="${CONNECT_lag_random}" step="1" id="CONNECTLag${i}" class="UserInputs"> <output for="CONNECTLag${i}" id="CONNECTLagValue${i}"> ${CONNECT_lag_random} % </output></td>`;
    }
    $('.UserInputs').on("change", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#FstDoseValue'.concat(i)).value = $('#FstDose'.concat(i)).val() + " %";
    document.querySelector('#ScdDoseValue'.concat(i)).value = $('#ScdDose'.concat(i)).val() + " %";
    document.querySelector('#CONNECTLagValue'.concat(i)).value = $('#CONNECTLag'.concat(i)).val() + " %";
    }
});
});

$('#noVaccination').on("click", function (){

    var table = document.getElementById('COVID_table_stats');

    for (let i = 16; i > 0 ; i--) {
        first_dose_none = 0
        second_dose_none = 0

    document.getElementById('COVID_table_stats').rows[i].cells[1].innerHTML = `<td><input type="range" min="0" max="100" value="${first_dose_none}" step="1" id="FstDose${i}" class="UserInputs"> <output for="FstDose${i}" id="FstDoseValue${i}"> ${first_dose_none} % </output></td>`;
    document.getElementById('COVID_table_stats').rows[i].cells[2].innerHTML = `<td><input type="range" min="0" max="100" value="${second_dose_none}" step="1" id="ScdDose${i}" class="UserInputs"> <output for="ScdDose${i}" id="ScdDoseValue${i}"> ${second_dose_none} % </output></td>`;
    }
    $('.UserInputs').on("change", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#FstDoseValue'.concat(i)).value = $('#FstDose'.concat(i)).val() + " %";
    document.querySelector('#ScdDoseValue'.concat(i)).value = $('#ScdDose'.concat(i)).val() + " %";
    }
});
});
$('#lowVaccination').on("click", function (){

    var table = document.getElementById('COVID_table_stats');

    for (let i = 16; i > 0 ; i--) {
        first_dose_random = 11 + Math.floor(Math.random() * 15)
        second_dose_random = first_dose_random - Math.floor(Math.random() * 10)

    document.getElementById('COVID_table_stats').rows[i].cells[1].innerHTML = `<td><input type="range" min="0" max="100" value="${first_dose_random}" step="1" id="FstDose${i}" class="UserInputs"> <output for="FstDose${i}" id="FstDoseValue${i}"> ${first_dose_random} % </output></td>`;
    document.getElementById('COVID_table_stats').rows[i].cells[2].innerHTML = `<td><input type="range" min="0" max="100" value="${second_dose_random}" step="1" id="ScdDose${i}" class="UserInputs"> <output for="ScdDose${i}" id="ScdDoseValue${i}"> ${second_dose_random} % </output></td>`;
    }
    $('.UserInputs').on("change", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#FstDoseValue'.concat(i)).value = $('#FstDose'.concat(i)).val() + " %";
    document.querySelector('#ScdDoseValue'.concat(i)).value = $('#ScdDose'.concat(i)).val() + " %";
    }
});
});


$('#highVaccination').on("click", function (){

    var table = document.getElementById('COVID_table_stats');

    for (let i = 16; i > 0 ; i--) {
        first_dose_random = 70 + Math.floor(Math.random() * 20)
        second_dose_random = first_dose_random - Math.floor(Math.random() * 15)

        if (second_dose_random < 0){
            second_dose_random = 0
        }
    document.getElementById('COVID_table_stats').rows[i].cells[1].innerHTML = `<td><input type="range" min="0" max="100" value="${first_dose_random}" step="1" id="FstDose${i}" class="UserInputs"> <output for="FstDose${i}" id="FstDoseValue${i}"> ${first_dose_random} % </output></td>`;
    document.getElementById('COVID_table_stats').rows[i].cells[2].innerHTML = `<td><input type="range" min="0" max="100" value="${second_dose_random}" step="1" id="ScdDose${i}" class="UserInputs"> <output for="ScdDose${i}" id="ScdDoseValue${i}"> ${second_dose_random} % </output></td>`;
    }
    $('.UserInputs').on("change", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#FstDoseValue'.concat(i)).value = $('#FstDose'.concat(i)).val() + " %";
    document.querySelector('#ScdDoseValue'.concat(i)).value = $('#ScdDose'.concat(i)).val() + " %";
    }
});
});

$('#lowSocialContact').on("click", function (){

    var table = document.getElementById('COVID_table_stats');

    for (let i = 16; i > 0 ; i--) {
        CONNECT_lag_random = 15 + Math.floor(Math.random() * 13)

    document.getElementById('COVID_table_stats').rows[i].cells[3].innerHTML = `<td><input type="range" min="0" max="100" value="${CONNECT_lag_random}" step="1" id="CONNECTLag${i}" class="UserInputs"> <output for="CONNECTLag${i}" id="CONNECTLagValue${i}"> ${CONNECT_lag_random} % </output></td>`;
    }
    $('.UserInputs').on("change", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#CONNECTLagValue'.concat(i)).value = $('#CONNECTLag'.concat(i)).val() + " %";
    }
});
});

$('#highSocialContact').on("click", function (){

    var table = document.getElementById('COVID_table_stats');

    for (let i = 16; i > 0 ; i--) {
        CONNECT_lag_random = 70 + Math.floor(Math.random() * 20)

    document.getElementById('COVID_table_stats').rows[i].cells[3].innerHTML = `<td><input type="range" min="0" max="100" value="${CONNECT_lag_random}" step="1" id="CONNECTLag${i}" class="UserInputs"> <output for="CONNECTLag${i}" id="CONNECTLagValue${i}"> ${CONNECT_lag_random} % </output></td>`;
    }
    $('.UserInputs').on("change", function (){
    for (let i = 16; i > 0; i--) {
    document.querySelector('#CONNECTLagValue'.concat(i)).value = $('#CONNECTLag'.concat(i)).val() + " %";
    }
});
});



/* Function to change the rendering of the Dasboard if the user change any settings in the menu bar */
$("#predict").on("click", function() {

        dose_1 = []
        dose_2 = []
        connect_covid = []
        dynamic_url = $("#dynamic_url_covid").val();
        console.log(dose_1)
        console.log(dose_2)
        console.log(connect_covid)
        for (let i = 1; i < 17; i++) {
            dose_1.push(document.querySelector('#FstDoseValue'.concat(i)).value.replace('%','').trim()/100)
            dose_2.push(document.querySelector('#ScdDoseValue'.concat(i)).value.replace('%','').trim()/100)
            connect_covid.push(document.querySelector('#CONNECTLagValue'.concat(i)).value.replace('%','').trim()/100)
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
            success: function(data) {
            $('#map_covid').html(data.map_COVID_updated)
            }
            });
        });