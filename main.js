const socket = io.connect(window.location.href);

let barCtx = document.getElementById("myBarChart").getContext("2d");
let barChart = new Chart(barCtx, {
  type: "bar",
  data: {
    labels: [],
    datasets: [{
      label: "Amount ($)",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
      data: [],
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

socket.on('connect', function() {
    socket.emit('request_bar_chart_data');
});

socket.on('bar_chart_data', function(data) {
    console.log("Received bar chart data from server.");
    // Load bar chart data
    barChart.data.labels = data.labels;
    barChart.data.datasets[0].data = data.values;
    barChart.update();
    $("#current_refresh_time").html(data.current_refresh_time);
});
