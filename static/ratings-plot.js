// Fetch the plot data and race lookup data from the hidden divs
const plotDataDiv = document.getElementById('plotDataDiv');
const raceLookupDiv = document.getElementById('raceLookupDiv');
const plotData = JSON.parse(plotDataDiv.dataset.plotData);
const raceLookupList = JSON.parse(raceLookupDiv.dataset.raceLookup);

// Convert the raceLookupList into an object for easier access
const raceLookup = raceLookupList.reduce((lookup, race) => {
    lookup[race.id] = race.name;
    return lookup;
}, {});

// Prepare traces dynamically
const data = plotData.map(driverData => {
    const raceNames = driverData.races.map(raceId => raceLookup[raceId]); // Map race IDs to names
    return {
        x: driverData.races,  // x-axis is race numbers
        y: driverData.points, // y-axis is total points
        text: raceNames,      // Hover text showing race names
        type: 'scatter',
        mode: 'lines',
        name: driverData.driver // Legend name
    };
});

// Define layout options
const layout = {
    title: 'Driver Points Over Time',
    xaxis: {
        title: 'Race Number',
        tickmode: 'array',
        tickvals: Array.from({ length: plotData[0].races.length }, (_, i) => i + 1),
        ticktext: Array.from({ length: plotData[0].races.length }, (_, i) => `${i + 1}`)
    },
    yaxis: {
        title: 'Total Points'
    }
};

// Render the Plotly chart
Plotly.newPlot('myDiv', data, layout);
