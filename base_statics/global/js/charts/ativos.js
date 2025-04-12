

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
        let dataCharts = JSON.parse(data);  // Parse do JSON vindo do backend

        const valores = dataCharts.valor;
        const anos = dataCharts.ano;

        // Encontra o maior valor
        const maxValor = Math.max(...valores);

        // Constrói os dados da série, destacando o maior valor com a cor vermelha
        const dadosSerie = valores.map(valor => {
            if (valor === maxValor) {
                return {
                    value: valor,
                    itemStyle: {
                        color: '#a90000'  // vermelho
                    }
                };
            }
            return valor;
        });

        const grafico = echarts.init(document.getElementById('operaca-ativo'));

        const option = {
            title: {
                show: true,
                text: 'Aquisição de Ativos por Ano',
                left: '50%',
                textAlign: 'center',
                padding: [10, 20],
                textStyle: {
                    color: '#FFFFFF'
                }
            },
            tooltip: {
                show:false,
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            xAxis: {
                type: 'category',
                data: anos,
                axisLabel: {
                    color: 'white', // Cor dos rótulos do eixo X
                    rotate: 45,
                    interval: 0
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    color: 'white', // Cor dos nomes das categorias
                    //fontWeight: 'bold' // Deixa o texto mais destacado
                }
            },
            series: [
                {
                    name: 'Quantidade',
                    type: 'bar',
                    data: dadosSerie,
                    label: {
                        show: true,
                        color: '#FFFFFF', // Cor dos rótulos dentro das barras
                        position: 'top'
                    },
                    itemStyle: {
                        color: '#5470C6'  // cor padrão
                    }
                }
            ]
        };

        grafico.setOption(option);

        window.addEventListener('resize', function () {
            grafico.resize();
        });
    });
}

