// Fetch the plot data from the hidden div
const plotDataDiv = document.getElementById('plotDataDiv');
const plotData = JSON.parse(plotDataDiv.dataset.plotData);

// Prepare traces dynamically
const data = plotData.map(driverData => ({
    x: driverData.races,  // x-axis is race numbers
    y: driverData.points, // y-axis is total points
    type: 'scatter',
    mode: 'lines+markers',
    name: driverData.driver // Legend name
}));

// Define layout options
const layout = {
    title: 'Driver Points Over Time',
    xaxis: {
        title: 'Race Number',
        tickmode: 'array',
        tickvals: Array.from({ length: plotData[0].races.length }, (_, i) => i + 1),
        ticktext: Array.from({ length: plotData[0].races.length }, (_, i) => `Race ${i + 1}`)
    },
    yaxis: {
        title: 'Total Points'
    }
};

// Render the Plotly chart
Plotly.newPlot('myDiv', data, layout);
