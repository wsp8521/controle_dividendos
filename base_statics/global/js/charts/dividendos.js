function chartDividendosMensal(data) {
    document.addEventListener("DOMContentLoaded", function() {
    let dados = JSON.parse(data);  // JSON válido  
    var grafico = echarts.init(document.getElementById('chart-proventos-mensais'));

    opcoes = {
        title: {
          show: true,
          text: 'Distribuição de Dividendos do ano',
          left: '50%',
          textAlign: 'center',
          padding: [10, 20],
          textStyle: {
              color: '#FFFFFF'
          }
      },
        xAxis: {
          type: 'category',
          data: dados.labels,
          axisLabel: {
            color: '#fff',
            interval: 0  // <-- mostra todos os rótulos
        }

        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: dados.valores,
            type: 'line',
            smooth: true
          }
        ],

        tooltip: {
          trigger: 'axis',
          formatter: params => 'R$ ' + params[0].value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })
        },
      };

    grafico.setOption(opcoes);

    // Ajusta o gráfico ao redimensionar a tela
    window.addEventListener('resize', function () {
        grafico.resize();
    });

    })
  
}
//Grafico tipo pizza composição dos diveidendos
function chartComposicaoDividendos(data) {
  document.addEventListener("DOMContentLoaded", function() {
      let dados = JSON.parse(data);  // JSON válido  
      console.log(dados)
      var grafico = echarts.init(document.getElementById('chart-composicao-dividendos'))
      
      var opcoes = {
          title: {
              show: true,
              text: 'Composição dos dividendos',
              left: '50%',
              textAlign: 'center',
              padding: [10, 20],
              textStyle: {
                  color: '#FFFFFF'
              }
          },
          tooltip: { 
              show:true,
              trigger: 'item',
              formatter: ({ value }) => `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
          },
          legend: {
              show: true,
              orient: 'horizontal',
              left: 'center',
              bottom: '10',
              padding: [10, 0],
              data: dados.categorias,
              textStyle: {
                  color: '#FFFFFF'
              }
          },
          series: [{
              name: 'Composição por Classe',
              type: 'pie',
              radius: '50%',
              data: dados.categorias.map((classe, index) => ({
                  name: classe,
                  value: dados.valores[index]
              })),
              label: {
                  show: true,
                  formatter: '{d}%', // Exibe o valor em porcentagem no tooltip
                  textStyle: {
                      color: '#FFFFFF'
                  }
              },
              emphasis: {
                  itemStyle: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
              }
          }],
          grid: {
              top: '20',
              bottom: '30'
          }
      };
      grafico.setOption(opcoes);

      // Ajusta o gráfico ao redimensionar a tela
      window.addEventListener('resize', function () {
          grafico.resize();
      });
  });
}


/*********************************************
 * PÁGINA DETALHES DOS ATIVOS
 * *****************************************/
