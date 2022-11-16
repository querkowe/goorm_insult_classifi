function chart_bar(label, good_num, bad_num, id){

    const ctx1 = document.getElementById(id)
    const data1 = {
      labels: label,

      datasets: [{
        type: 'bar',
        label: '일반 댓글',
        data: good_num,
        borderColor: 'rgb(0, 0, 0)',
        backgroundColor: 'rgba(233, 237, 241, 1)'
      }, {
        type: 'bar',
        label: '악성 댓글',
        data: bad_num,
        fill: false,
        borderColor: 'rgb(0, 0, 0)',
        backgroundColor: 'rgba(166, 184, 196, 0.5)'
      }]
    };
    const config1 = {
      type: 'scatter',
      data: data1,
      options: {

        scales: {y: {beginAtZero: true}

      }}

    };
    const one_chart = new Chart(
      ctx1,
      config1
    );



}
