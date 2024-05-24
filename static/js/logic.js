/***********
  INIT MAP
************/
// Creating the map objects
// Employment map
let employmentMap = L.map("map-employment", {
  center: [38.5, -96],
  zoom: 4,
  maxZoom: 8
});

let incomeMap = L.map("map-income", {
  center: [38.5, -96],
  zoom: 4,
  maxZoom: 8
});

// Adding the tile layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors, © CARTO'
}).addTo(employmentMap);

// Adding the tile layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors, © CARTO'
}).addTo(incomeMap);

// Initialize variables to make them global
let employmentChoroplethLayer;
let employmentLegend;

// Initialize variables to make them global
let incomeChoroplethLayer;
let incomeLegend;

/***********
  FUNCTIONS
************/

// Refresh Employment map
function refreshEmploymentMap(state_code, industry_code, reduction) {
  // Define URL for API
  let geoData = `http://127.0.0.1:5000/api/v1.0/get_employment_map/${state_code}/${industry_code}/${reduction}`;

  // Get the data with d3.
  d3.json(geoData).then(function (data) {
    // Define new variable respose to keep value of data
    let response = data;

    console.log(response);

    // Remove existing choropleth layer and legend if they exist
    if (employmentChoroplethLayer) {
      employmentChoroplethLayer.remove();
      employmentChoroplethLayer = null;
    }
  
    if (employmentLegend) {
      employmentMap.removeControl(employmentLegend);
      employmentLegend = null;
    }

    // Create a new choropleth layer.
    employmentChoroplethLayer = L.choropleth(response, {
      // Define which property in the features to use.
      valueProperty: "reduced_industry_share",

      // Set the color scale.
      scale: ["#ece7f2", "#2b8cbe"],

      // The number of breaks in the step range
      steps: 5,

      // q for quartile, e for equidistant, k for k-means
      mode: "q",

      // Define style
      style: {
        color: '#fff',
        weight: 2,
        fillOpacity: 0.9
      },

      // Binding a popup to each layer
      onEachFeature: function(feature, layer) {

        let bindPopupHTML;

        if (state_code === "US") {
          bindPopupHTML = `<b>State: </b>${feature.properties.NAME}
          <hr><p>Reduced industry share by employment: ${feature.properties.reduced_industry_share.toLocaleString()}%</p>
          <p>Current industry share by employment: ${feature.properties.current_industry_share.toLocaleString()}%</p>`
        } else {
          bindPopupHTML = `<b>State: </b>${feature.properties.STATE_NAME}<br>
          <b>County: </b>${feature.properties.NAME}
          <hr><p>Reduced industry share by employment: ${feature.properties.reduced_industry_share.toLocaleString()}%</p>
          <p>Current industry share by employment: ${feature.properties.current_industry_share.toLocaleString()}%</p>`
        }

        layer.bindPopup(bindPopupHTML);
      }

    }).addTo(employmentMap);

    // Focus map on a selected state or a whole mainland US
    if (state_code === "US") {
      employmentMap.setView([38.5, -96], 4);
    } else {
      employmentMap.fitBounds(employmentChoroplethLayer.getBounds());
    }
    
    // Set up the legend
    employmentLegend = L.control({ position: 'bottomright' })

    // Define a function that creates a legend
    employmentLegend.onAdd = function (map) {
      let div = L.DomUtil.create('div', 'info legend');
      let limits = employmentChoroplethLayer.options.limits;
      let colors = employmentChoroplethLayer.options.colors; 

      div.style.backgroundColor = 'white';    // Set the background color to white
      div.style.padding = '6px';              // Add some padding for aesthetics
      div.style.border = '1px solid #ccc';    // Add a light grey border
      div.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)'; // Add a subtle shadow

      // Loop through all limits to create a set of color strips related to ranges
      limits.forEach(function (limit, index) {
        div.innerHTML += '<b style="background-color: ' + colors[index] + '; display: inline-block;">' + limits[index].toLocaleString() + '</b><br>';
      })

      return div
    }

    // Add the legend to the map
    employmentLegend.addTo(employmentMap);
  });
}

// Refresh Income map
function refreshIncomeMap(state_code, industry_code, reduction) {
  // Define URL for API
  let geoData = `http://127.0.0.1:5000/api/v1.0/get_income_map/${state_code}/${industry_code}/${reduction}`;

  // Get the data with d3.
  d3.json(geoData).then(function (data) {
    // Define new variable respose to keep value of data
    let response = data;

    console.log(response);

    // Remove existing choropleth layer and legend if they exist
    if (incomeChoroplethLayer) {
      incomeChoroplethLayer.remove();
      incomeChoroplethLayer = null;
    }
  
    if (incomeLegend) {
      incomeMap.removeControl(incomeLegend);
      incomeLegend = null;
    }

    // Create a new choropleth layer.
    incomeChoroplethLayer = L.choropleth(response, {
      // Define which property in the features to use.
      valueProperty: "change_in_per_capita_income",

      // Set the color scale.
      scale: ["#b30000", "#fef0d9"],

      // The number of breaks in the step range
      steps: 5,

      // q for quartile, e for equidistant, k for k-means
      mode: "q",

      // Define style
      style: {
        color: '#fff',
        weight: 2,
        fillOpacity: 0.9
      },

      // Binding a popup to each layer
      onEachFeature: function(feature, layer) {

        let bindPopupHTML;

        if (state_code === "US") {
          bindPopupHTML = `<b>State: </b>${feature.properties.NAME}
          <hr><p>Reduced per capita income: ${parseInt(feature.properties.per_capita_reduced_income).toLocaleString()}</p>
          <p>Current per capita income: ${parseInt(feature.properties.per_capita_income).toLocaleString()}</p>
          <p>Current industry wage: ${parseInt(feature.properties.per_capita_industry_wage).toLocaleString()}</p>
          <p>Change in per capita income: ${feature.properties.change_in_per_capita_income.toLocaleString()}%</p>`
        } else {
          bindPopupHTML = `<b>State: </b>${feature.properties.STATE_NAME}<br>
          <b>County: </b>${feature.properties.NAME}
          <hr><p>Reduced per capita income: ${parseInt(feature.properties.per_capita_reduced_income).toLocaleString()}</p>
          <p>Current per capita income: ${parseInt(feature.properties.per_capita_income).toLocaleString()}</p>
          <p>Current industry wage: ${parseInt(feature.properties.per_capita_industry_wage).toLocaleString()}</p>
          <p>Change in per capita income: ${feature.properties.change_in_per_capita_income.toLocaleString()}%</p>`
        }

        layer.bindPopup(bindPopupHTML);
      }

    }).addTo(incomeMap);

    // Focus map on a selected state or a whole mainland US
    if (state_code === "US") {
      incomeMap.setView([38.5, -96], 4);
    } else {
      incomeMap.fitBounds(incomeChoroplethLayer.getBounds());
    }
    
    // Set up the legend
    incomeLegend = L.control({ position: 'bottomright' })

    // Define a function that creates a legend
    incomeLegend.onAdd = function (map) {
      let div = L.DomUtil.create('div', 'info legend');
      let limits = incomeChoroplethLayer.options.limits;
      let colors = incomeChoroplethLayer.options.colors; 

      div.style.backgroundColor = 'white';    // Set the background color to white
      div.style.padding = '6px';              // Add some padding for aesthetics
      div.style.border = '1px solid #ccc';    // Add a light grey border
      div.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)'; // Add a subtle shadow

      // Loop through all limits to create a set of color strips related to ranges
      limits.forEach(function (limit, index) {
        div.innerHTML += '<b style="background-color: ' + colors[index] + '; display: inline-block;">' + limits[index].toLocaleString() + '%</b><br>';
      })

      return div
    }

    // Add the legend to the map
    incomeLegend.addTo(incomeMap);
  });
}

// Refresh bar chart
function refreshBarChart(state_code, industry_code, reduction) {
  // Define URL for API
  let url = `http://127.0.0.1:5000/api/v1.0/get_unemployment_rate/${state_code}/${industry_code}/${reduction}`;

  // Make API call
  d3.json(url).then(function (data) {
    // Define new variable respose to keep value of data
    let response = data;

    console.log(response);

    // Declare empty variables
    let areas, unemploymentRate, forecastedUnemploymentRate, averageUnemploymentRate, averageLine, plotData;

    // Read data from API response
    areas = response.map(res => res.area_name);
    unemploymentRate = response.map(res => res.unemployment_rate);
    forecastedUnemploymentRate = response.map(res => res.forecasted_unemployment_rate);
    averageUnemploymentRate = response.map(res => res.average_unemployment_rate);

    // Reverse arrays to show them alphabetically
    areas.reverse();
    unemploymentRate.reverse();
    forecastedUnemploymentRate.reverse();

    // set average line
    averageLine = {
      name: 'Average Unemployment Rate, %',
      x: averageUnemploymentRate,
      y: areas,
      mode: 'lines',
      type: 'scatter',
      line: {
          color: 'green',
          width: 2
      },
      showlegend: true,
      hoverinfo: 'x' // it shows only x-value in the tooltip
    };

    // Horizontal bar for Unemployment rate
    let barUnemploymentRate = {
      name: 'Current Unemployment Rate, %',
      x: unemploymentRate,
      y: areas,
      type: 'bar',
      orientation: 'h',
      marker: {
        color: '#2b8cbe'
      },
      opacity: 0.75,
      showlegend: true,
      text: unemploymentRate.map(metric => metric.toLocaleString()),
      hoverinfo: 'text'
    };

    // Horizontal bar for Forecasted Unemployment rate
    let barForecastedUnemploymentRate = {
      name: 'Forecasted Unemployment Rate, %',
      x: forecastedUnemploymentRate,
      y: areas,
      type: 'bar',
      orientation: 'h',
      opacity: 0.5,
      marker: {
        color: '#de2d26'
      },
      showlegend: true,
      text: forecastedUnemploymentRate.map(metric => metric.toLocaleString()),
      hoverinfo: 'text'
    };

    // Define plot data
    plotData = [barForecastedUnemploymentRate, barUnemploymentRate, averageLine];

    // Layout configuration
    let layout = {
      barmode: 'group',
      bargap: 0.2,  // Controls the gap between bars within a group
      xaxis: {
          title: "Unemployment rate, %"
      },
      margin: { t: 10, b: 40, r: 10 },
      height: areas.length * 20, 
      yaxis: {
        automargin: true, // Automatically adjust the margin to fit labels if needed
        tickfont: {
            size: 12 
        },
        range: [-1.0, areas.length + 3.2]  // Adjust y-axis to make sure that there are no white spaces before and after bars
      },
      legend: {
          x: 0.5, // Center the legend horizontally
          y: 1, // Position the legend just above the top of the chart
          xanchor: 'center', // Anchor the legend based on its center
          yanchor: 'top', // Anchor the legend at the top
          orientation: 'h' // Horizontal orientation of the legend items
      },
      hovermode: 'closest', // Can help with tooltip precision
    };

    Plotly.newPlot('bar-chart', plotData, layout);
  });
}

// Refresh line chart
function refreshLineChart(state_code, industry_code, reduction) {
  // Define URL for API
  let url = `http://127.0.0.1:5000/api/v1.0/get_employment_trend/${state_code}/${industry_code}/${reduction}`;

  // Make API call
  d3.json(url).then(function (data) {
    // Define new variable respose to keep value of data
    let response = data;
    
    console.log(response);

    // Declare empty variables
    let years, trend, trace, plotData;

    // Read data from API response
    years = response.map(res => res.year);

    // Define trend and trace
    trend = response.map(res => res.metric);

    trace = {
      x: years,
      y: trend,
      type: 'scatter',        // Scatter used for line charts in Plotly
      mode: 'lines+markers',  // Display both lines and markers
      name: 'Employment trend',
      marker: {
          color: 'red'
      },
      line: {
          color: 'red',
          width: 2
      },
      showlegend: true
    }

    // Define plot data
    plotData = [trace] 
    
    // Layout configuration
    let layout = {
      xaxis: {
        title: 'Year',
        tickmode: 'linear',
        automargin: true // Automatically adjust the margin to fit labels if needed
      },
      yaxis: {
        automargin: true // Automatically adjust the margin to fit labels if needed
      },
      margin: { t: 10, b: 10, r: 10, l: 10 },
      legend: {
        x: 0.5, // Center the legend horizontally
        y: 1.1, // Position the legend just above the top of the chart
        xanchor: 'center', // Anchor the legend based on its center
        yanchor: 'top', // Anchor the legend at the top
        orientation: 'h' // Horizontal orientation of the legend items
      }
    }

    Plotly.newPlot('line-chart', plotData, layout);
  });
}

// Refresh page
function refreshPage(state_code, industry_code, industry_name, reduction) {
  // Update map employment title
  let mapEmploymentTitle = d3.select("#map-employment-title");
  let mapEmploymentTitleHTML = `Change in employment (over population) for "${industry_name}"`
  mapEmploymentTitle.html(mapEmploymentTitleHTML);

  // Update map income title
  let mapIncomeTitle = d3.select("#map-income-title");
  let mapIncomeTitleHTML = `Change in income (over population) for "${industry_name}"`
  mapIncomeTitle.html(mapIncomeTitleHTML);

  // Update line chart title
  let lineChartTitle = d3.select("#line-chart-title");
  let lineChartTitleHTML = `Change in employment (over population) for "${industry_name}" trend over time`
  lineChartTitle.html(lineChartTitleHTML);

  // Update bar chart title
  let barChartTitle = d3.select("#bar-chart-title");
  let barChartTitleHTML = `Area with highest unemployment (over population) after change for "${industry_name}"`
  barChartTitle.html(barChartTitleHTML);

  refreshEmploymentMap(state_code, industry_code, reduction);
  refreshIncomeMap(state_code, industry_code, reduction);
  refreshLineChart(state_code, industry_code, reduction);
  refreshBarChart(state_code, industry_code, reduction);
}

// Handing selector changes
d3.selectAll("select").on("change", function() {
  // Getting the current values of selectors
  let selArea = d3.select("#selArea");
  let selIndustry = d3.select("#selIndustry");
  let selReduction = d3.select("#selReduction");

  let state_code = selArea.property("value");
  let industry_code = parseInt(selIndustry.property("value"));
  let industry_name = selIndustry.select("option:checked").text();
  let reduction = parseInt(selReduction.property("value"));

  refreshPage(state_code, industry_code, industry_name, reduction);
});

// Initial page load
function init() {
  // Fill out areas selector
  let selArea = d3.select("#selArea");

  // Call API to get a list of states
  let url_states = "http://127.0.0.1:5000/api/v1.0/get_states";

  d3.json(url_states).then(function (data) {
    data.forEach((s) => {
      selArea
        .append("option")
        .text(s.state_name)
        .property("value", s.state_code);
    });
  })

  // Fill out industries selector
  let selIndustry = d3.select("#selIndustry");

  // Call API to get a list of industries
  let url_industries = "http://127.0.0.1:5000/api/v1.0/get_industries";

  d3.json(url_industries).then(function (data) {
    data.forEach((i) => {
      selIndustry
        .append("option")
        .text(i.industry_name)
        .property("value", i.industry_code);
    });
  })

  // Set default values for main variables, corresponsed to first elements of drop-downs
  let state_code = "US";
  let industry_code = "1011";
  let industry_name = "1011 - National resources and mining";
  let reduction = 5;

  // Call refresh_page function
  refreshPage(state_code, industry_code, industry_name, reduction);
}

/***********
  INIT
************/
//  Call init() function - this code will be executed once, during the initial page load
init();