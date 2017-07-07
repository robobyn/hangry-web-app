var options = {
      responsive: false,
      maintainAspectRatio: false
    };

var ctx = $("#donutChart").get(0).getContext("2d");

$.get("/cuisine-count.json", function (data) {
      console.log(data);
      var myDonutChart = new Chart(ctx, {
                                          type: 'doughnut',
                                          data: data,
                                          options: options,
                                        });
      });
