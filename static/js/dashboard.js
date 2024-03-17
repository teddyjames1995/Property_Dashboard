// Initialization of global chart variables to access them for updates
var sectorAllocationChart, leaseExpiryChart;

// Function to render Sector Allocation Chart using Chart.js
function renderSectorAllocationChart() {
    var ctxPie = document.getElementById('sector-allocation-chart').getContext('2d');
    sectorAllocationChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: sectorAllocationData.labels, // Using labels from parsed data
            datasets: [{
                label: 'Sector Allocation',
                data: sectorAllocationData.values, // Using values from parsed data
                backgroundColor: sectorAllocationData.backgroundColors,
                borderColor: sectorAllocationData.borderColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Function to render Lease Expiry Chart using Chart.js
function renderLeaseExpiryChart() {
    var ctxBar = document.getElementById('lease-expiry-chart').getContext('2d');
    leaseExpiryChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: leaseExpiryData.labels, // Using labels from parsed data
            datasets: [{
                label: 'Lease Expiry',
                data: leaseExpiryData.values, // Using values from parsed data
                backgroundColor: leaseExpiryData.backgroundColors,
                borderColor: leaseExpiryData.borderColors,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{ ticks: { beginAtZero: true } }]
            },
            responsive: true
        }
    });
}

// Dummy function to simulate data fetching based on dropdowns
// Update this function as necessary to fetch and process real data
function fetchDataForCharts() {
    // Here you would fetch new data based on the dropdown selection
    // For demonstration, we're using the initial data
    renderSectorAllocationChart();
    renderLeaseExpiryChart();
}

// Function to update charts based on dropdown changes (placeholder content)
function updateChartsOnDropdownChange() {
    // Placeholder logic - fetch new data and update charts accordingly
    fetchDataForCharts();
}

// Event listeners for dropdown changes to update charts
document.getElementById('portfolio-dropdown').addEventListener('change', updateChartsOnDropdownChange);
document.getElementById('property-dropdown').addEventListener('change', updateChartsOnDropdownChange);
document.getElementById('date-dropdown').addEventListener('change', updateChartsOnDropdownChange);

// Parse JSON data embedded in the HTML page
var sectorAllocationData = JSON.parse(document.getElementById('sector-allocation-data').textContent);
var leaseExpiryData = JSON.parse(document.getElementById('lease-expiry-data').textContent);

// Render the charts initially
renderSectorAllocationChart();
renderLeaseExpiryChart();
