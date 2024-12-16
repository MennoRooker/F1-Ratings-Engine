const getData = (plotData) => {
    // Find the longest season (max number of races)
    const maxRaces = Math.max(...plotData.map(driverData => driverData.races.length));

    // Prepare traces for Plotly
    return plotData.map(driverData => {
        // Extend the x and y data to align with the longest season
        const extendedRaces = Array.from({ length: maxRaces }, (_, i) => i + 1);
        const extendedPoints = extendedRaces.map((raceNum, index) =>
            index < driverData.points.length ? driverData.points[index] : null // Use null for missing data
        );

        return {
            x: extendedRaces,          // Align x-axis with the longest season
            y: extendedPoints,         // Extend points with nulls for missing races
            text: driverData.races,    // Use original race names for hover text
            type: 'scatter',
            mode: 'lines',
            name: driverData.driver    // Legend label
        };
    });
};

const getLayout = (plotData) => {
    // Find the longest season to define x-axis ticks
    const maxRaces = Math.max(...plotData.map(driverData => driverData.races.length));

    // Define layout options
    return {
        title: 'Driver Points Over Time',
        xaxis: {
            title: 'Race Number',
            tickmode: 'array',
            tickvals: Array.from({ length: maxRaces }, (_, i) => i + 1), // Number all races sequentially
            ticktext: Array.from({ length: maxRaces }, (_, i) => `Race ${i + 1}`) // Use "Race 1", "Race 2", ...
        },
        yaxis: {
            title: 'Total Points'
        },
        legend: {
            orientation: 'h',
            x: 0.5,
            xanchor: 'center',
            y: -0.2
        }
    };
};

// Fetch the plot data from the hidden div
const plotDataDiv = document.getElementById('plotDataDiv');
const plotData = plotDataDiv ? JSON.parse(plotDataDiv.dataset.plotData) : [];

if (plotData.length > 0) {
    // Render the Plotly chart
    Plotly.newPlot('myDiv', getData(plotData), getLayout(plotData));
}
