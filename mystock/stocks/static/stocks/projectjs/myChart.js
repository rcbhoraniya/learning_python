
const labels = [{%for data in stock_hist%}'{{data.date|date:'d-m-Y'}}',{%endfor%}];
const data = {
  labels,
  datasets: [
    {
      label: 'Close Price',
      data: [{%for data in stock_hist%}{{data.close}},{%endfor%}],
      borderColor: 'Blue',
      borderWidth: 1,
      tension: 0.1,
      pointStyle:'star',
      fill:true,
      yAxisID: 'y',
    },
{
      label: 'Volume',
      data: [{%for data in stock_hist%}{{data.volume}},{%endfor%}],
      borderColor: 'red',
      borderWidth: 1,
      tension: 0.1,
      pointStyle:'star',
      yAxisID: 'y1',
    }
  ],
};

const config = {
  type: 'line',
  data:data,
  options: {
    radius:2,
    hitRedius:30,
    hoverRedius:60,
    tension:0.3,
    responsive: true,
    scales: {
        y: {
            beginAt: {{maxmindata.ylow}}
            },
        },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '{{stock_hist.0.company}}',
      }
    }
  },
};
const ctx = document.getElementById('myChart');

const myChart = new Chart(ctx, config);
