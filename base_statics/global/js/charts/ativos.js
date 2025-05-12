

// gráfico tipo pizza de ativos por classe
function chartAtivoPorClasse(data) {
    document.addEventListener("DOMContentLoaded", function() {
    let ativiClasse = JSON.parse(data);  // JSON válido  
    var grafico = echarts.init(document.getElementById('ativo-por-classe'));
    var opcoes = {
        title: {
            show: true,
            text: 'Distribuição de Ativos por Classe',
            left: '50%',
            textAlign: 'center',
            padding: [10, 20],
            textStyle: {
                color: '#FFFFFF'
            }
        },
        tooltip: { trigger: 'item' },
        legend: {
            orient: 'horizontal',
            left: 'center',
            bottom: '10',
            padding: [10, 0],
            data: ativiClasse.categorias,
            textStyle: {
                color: '#FFFFFF'
            }
        },
        series: [{
            name: 'Quantidade',
            type: 'pie',
            radius: '50%',
            data: ativiClasse.categorias.map((classe, index) => ({
                name: classe,
                value: ativiClasse.valores[index]
            })),
            label: {
                show: true,
                formatter: '{b}: {d}%', // Exibe o valor em porcentagem no tooltip
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


     })
    
}

//gráfico tipo barra de ativos por setor
function chartAtivoPorSetor(data){
    document.addEventListener("DOMContentLoaded", function() {
    let dataCharts = JSON.parse(data);  // JSON válido  
    var grafico = echarts.init(document.getElementById('ativo-por-setor'));
    var option = {
        title: {
            show: true,
            text: 'Distribuição de Ativos por Setor',
            left: '50%',
            textAlign: 'center',
            padding: [10, 20],
            textStyle: {
                color: '#FFFFFF'
            }
        },
        // backgroundColor: '#007bff', // Fundo azul da div do gráfico
        // grid: {
        //     backgroundColor: '#1E1E1E', // Cor de fundo da área de plotagem
        //     borderWidth: 0
        // },

        xAxis: {
            max: 'dataMax',
            axisLine: { 
                show: false,  // Exibe a linha do eixo X
                lineStyle: { 
                    color: '#000000' // Define a cor da linha do eixo X como preto
                } 
            },
            splitLine: { show: false }, // Remove as linhas de grade do eixo X
            show: false,  // Não exibe os rótulos do eixo X
            axisLabel: {
                color: 'white', // Cor dos nomes das categorias
                //fontWeight: 'bold' // Deixa o texto mais destacado
            }
        },
        yAxis: {
            splitLine: { show: false }, // Remove as linhas de grade do eixo y
            type: 'category',
            axisLine: { show: false }, // Remove a linha do eixo Y  
            data: dataCharts.categorias,
            inverse: true,
            //max: 5 // Exibe apenas os 5 setores com mais ativos
            axisLabel: {
                color: 'white', // Cor dos nomes das categorias
                //fontWeight: 'bold' // Deixa o texto mais destacado
            }
        },
        series: [
            {
                name: 'Quantidade de Ativos',
                type: 'bar',
                data: dataCharts.valores,
                label: {
                    
                    show: true,
                    position: 'right',
                    color: '#FFFFFF' // Cor dos rótulos dentro das barras
                },
                itemStyle: {
                    color: '#4CAF50' // Cor das barras
                }
            }
        ],
        legend: {
            show: false
        },
        animationDuration: 0,
        animationDurationUpdate: 0,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear'
    };

    grafico.setOption(option);

    // Ajusta o gráfico ao redimensionar a tela
    window.addEventListener('resize', function () {
        grafico.resize();
    });


     })
}

/*********************************************
 * PÁGINA DETALHES DOS ATIVOS
 * *****************************************/
function chartOperacao(data) {
  document.addEventListener("DOMContentLoaded", function () {
    let dataCharts = JSON.parse(data);
    const valores = dataCharts.valor;
    const anos = dataCharts.ano;

    const maxValor = Math.max(...valores);

    const dadosSerie = valores.map(valor => {
      const isMax = valor === maxValor;
      return {
        value: valor,
        itemStyle: {
          color: isMax ? '#a90000' : '#5470C6'
        },
        label: {
          show: true,
          position: 'top',
          color: '#000',
          fontSize: 13,
          formatter: val => val.value.toLocaleString('pt-BR') // sem "R$"
        }
      };
    });

    const grafico = echarts.init(document.getElementById('operaca-ativo'));

    const option = {
      title: { show: false },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: params => {
          const p = params[0];
          return `${p.axisValue}: ${p.value.toLocaleString('pt-BR')}`; // sem "R$"
        }
      },
      xAxis: {
        type: 'category',
        data: anos,
        axisLabel: {
          show: true,
          color: '#000',
          fontSize: 13
        },
        axisLine: { show: true, lineStyle: { color: '#ccc' } },
        axisTick: { show: true }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          show: true,
          color: '#000',
          fontSize: 12,
          formatter: val => val.toLocaleString('pt-BR')
        },
        splitLine: { lineStyle: { color: '#ccc' } }
      },
      series: [{
        name: 'ativos',
        type: 'bar',
        data: dadosSerie
      }]
    };

    grafico.setOption(option);
    window.addEventListener('resize', () => grafico.resize());
  });
}


//dividendos
function chartProventos(data) {
  document.addEventListener("DOMContentLoaded", function () {
    const dados = JSON.parse(data);
    const grafico = echarts.init(document.getElementById('proventos-ativo'));

    const opcoes = {
      grid: {
        left: '0%',
        right: '0%',
        top: '10%',
        bottom: '20%',        // espaço para os anos aparecerem
        containLabel: true    // garante que os rótulos não sejam cortados
      },
      xAxis: {
        type: 'category',
        data: dados.ano,
        axisLine: {
          show: true,
          lineStyle: {
            color: '#ccc'
          }
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          show: true,
          color: '#3f51b5',
          fontSize: 14
        }
      },
      yAxis: {
        type: 'value',
        show: false
      },
      tooltip: {
        trigger: 'axis',
        formatter: params => {
          const valor = params[0].value.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            minimumFractionDigits: 2
          });
          return `${params[0].axisValue} — ${valor}`;
        },
        axisPointer: {
          type: 'line'
        }
      },
      series: [{
        data: dados.valor,
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          color: '#3f51b5',
          width: 2
        },
        itemStyle: {
          color: '#3f51b5'
        },
        areaStyle: {
          color: 'rgba(63, 81, 181, 0.1)'
        },
        label: {
          show: true,
          position: 'top',
          formatter: params => {
            return `R$ ${params.value.toFixed(2).replace('.', ',')}`;
          },
          color: '#3f51b5',
          fontSize: 15
        }
      }]
    };

    grafico.setOption(opcoes);
    window.addEventListener('resize', () => grafico.resize());
  });
}
