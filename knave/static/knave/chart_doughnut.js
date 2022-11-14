function chart_doughnut(a, b, id){

  const ctx2 = document.getElementById(id);
  const data2 = {
    labels: [
      '악성 댓글',
      '정상 댓글',
    ],
    datasets: [{
      label: '분석 결과',
      data: [a, b],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
      ],
      hoverOffset: 4,
    }]
  };
  const config2 = {
    type: 'doughnut',
    data: data2,
  };
  const myChart = new Chart(
    ctx2,
    config2
  );


}
