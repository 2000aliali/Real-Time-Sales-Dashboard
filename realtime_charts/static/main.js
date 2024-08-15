// Initialize socket connection
const socket = io.connect(window.location.href);

// Initialize the Pie Chart
let pieCtx = document.getElementById("myPieChart").getContext("2d");
let pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: [],  // Will be populated with labels from server
        datasets: [{
            label: 'Sales Distribution',
            data: [],  // Will be populated with data from server
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Sales by Card Type'
            }
        }
    }
});

// Initialize the Bar Chart
let barCtx = document.getElementById("myBarChart").getContext("2d");
let barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: [],  // Will be populated with labels from server
        datasets: [{
            label: 'Amount ($)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: []  // Will be populated with data from server
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Category'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Amount ($)'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Sales by Category'
            }
        }
    }
});

// Function to load Bar Chart data
function loadBarChartData(endpoint) {
    $.ajax({
        url: endpoint,
        type: 'GET',
        dataType: 'json',
        success: function(jsonResponse) {
            barChart.data.labels = jsonResponse.data.labels;
            barChart.data.datasets[0].data = jsonResponse.data.datasets[0].data;
            barChart.update();
        },
        error: function() {
            console.log('Failed to fetch bar chart data from ' + endpoint + '!');
        }
    });
}

// Function to load Pie Chart data
function loadPieChartData(endpoint) {
    $.ajax({
        url: endpoint,
        type: 'GET',
        dataType: 'json',
        success: function(jsonResponse) {
            pieChart.data.labels = jsonResponse.data.labels;
            pieChart.data.datasets[0].data = jsonResponse.data.datasets[0].data;
            pieChart.update();
        },
        error: function() {
            console.log('Failed to fetch pie chart data from ' + endpoint + '!');
        }
    });
}

// On document ready
$(document).ready(function() {
    // Fetch filter options for dropdown
    $.ajax({
        url: '/chart/filter-options/',
        type: 'GET',
        dataType: 'json',
        success: function(jsonResponse) {
            jsonResponse.options.forEach(function(option) {
                $("#salesby").append(new Option(option, option));
            });
            // Load initial data for both charts
            const initialValue = $("#salesby").val();
            loadBarChartData(`/chart/sales-by/${initialValue}/`);
            loadPieChartData(`/chart/sales-by/${initialValue}/`);
        },
        error: function() {
            console.log('Failed to fetch chart filter options!');
        }
    });

    // Handle form submission
    $("#filterForm").on('submit', function(event) {
        event.preventDefault();
        const salesby = $("#salesby").val();
        loadBarChartData(`/chart/sales-by/${salesby}/`);
        loadPieChartData(`/chart/sales-by/${salesby}/`);
    });
});

// Handle socket events
socket.on('connect', function() {
    socket.emit('request_bar_chart_data');
});

socket.on('bar_chart_data', function(data) {
    console.log('Received bar chart data from server.');
    barChart.data.labels = data.labels;
    barChart.data.datasets[0].data = data.values;
    barChart.update();
    $("#current_refresh_time").html(data.current_refresh_time);
});
