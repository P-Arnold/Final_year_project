var ctx = document.getElementById('myChart').getContext('2d');

var namexx = './jquery.csv.js';
var csv = require([namexx]);
var csvData;
labelArray = [];
dataArray = [];
labelArray2 = [];
rev_deps = [318,992,173,639,804,696,27,329,433,265,338,168,247,194,99,256,91,297,57,120,253,156,169,117,9,145,108,83,125,104,115,129,53,94,75,108,21,111,47,57,63,50,39,67,86,51,89,64,58,60,70,55,75,44,44,52,36,51,42,66]
jQuery.get('/test.csv', function(data) {
    jQuery.get('/packageNamesTest.csv', function(names) {
         labelArray2 = $.csv.toArrays(names);
        // console.log(csvData2)
        // csvData.forEach( function(element) {
        //     labelArray.push(element[0]);
        //     dataArray.push(parseFloat(element[1]))
        });

        
    csvData = $.csv.toArrays(data);
    csvData.forEach( function(element) {
        labelArray.push(element[0]);
        dataArray.push(parseFloat(element[1]))
    });
    // console.log(csvData);
    console.log(dataArray);
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labelArray,
            datasets: [{
                label: 'PageRank',
                data: dataArray,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                // borderColor: [
                //     'rgba(255, 99, 132, 1)',
                //     'rgba(54, 162, 235, 1)',
                //     'rgba(255, 206, 86, 1)',
                //     'rgba(75, 192, 192, 1)',
                //     'rgba(153, 102, 255, 1)',
                //     'rgba(255, 159, 64, 1)'
                // ],
                borderWidth: 1
            }
        //     ,{
        //     label: 'Reverse Dependencies',
        //     data: rev_deps,
        //     backgroundColor: 'rgba(132, 99, 255, 0.2)',
        //     borderWidth: 1
        // }
    ]
        },
        options: {
            responsive: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});

// let data = $.csv.toArray('/new.csv');
// console.log(data)



