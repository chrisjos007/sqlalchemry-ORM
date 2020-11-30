fetch('india_plot.json')
.then(response => response.json())
.then(data => {
    x_values = Object.keys(data)
    y_values = Object.values(data)

    Highcharts.chart('india', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Indian population for each year'
        },
        xAxis: {
            title: {
                text: 'Year'
            },
            categories: x_values
        },
        yAxis: {
            title: {
                text: 'Population'
            }
        },
        series: [{
            name: 'yearwise population',
            data: y_values
        }]
    });
});

fetch('asean_plot.json')
.then(response => response.json())
.then(data => {
    x_values = Object.keys(data)
    y_values = Object.values(data)
    Highcharts.chart('asean', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Population data for each ASEAN nation'
        },
        xAxis: {
            title: {
                text: 'Nation'
            },
            categories: x_values
        },
        yAxis: {
            title: {
                text: 'Population'
            }
        },
        series: [{
            name: 'ASEAN population',
            data: y_values
        }]
    });
});


fetch('saarc_plot.json')
.then(response => response.json())
.then(data => {
    x_values = Object.keys(data)
    y_values = Object.values(data)
    Highcharts.chart('saarc', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'SAARC nation total population for each year'
        },
        xAxis: {
            title: {
                text: 'Year'
            },
            categories: x_values
        },
        yAxis: {
            title: {
                text: 'Total Population'
            }
        },
        series: [{
            name: 'SAARC population',
            data: y_values
        }]
    });
});


fetch('asean_group_plot.json')
.then(response => response.json())
.then(data => {
    let y_values = [];
    years = [];
    for (let nation in data) {
      y_values.push({
        name: nation,
        data: data[nation]
      })
    
    }
    for (let year=2004;year<2015;year++) {
        years.push(year)
    }

    Highcharts.chart('asean_group', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Population of ASEAN nations from 2004-14 for each country'
        },
        xAxis: {
            title: {
                text: 'Year'
            },
            categories: years
        },
        yAxis: {
            title: {
                text: 'Total Population'
            }
        },
        series: y_values
        
    });
});
