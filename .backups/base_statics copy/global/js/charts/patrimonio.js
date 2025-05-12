function chartComposicaoPatrimonio(data) {
    document.addEventListener("DOMContentLoaded", function() {
        let ativiClasse = JSON.parse(data);  // JSON válido  
        var grafico = echarts.init(document.getElementById('chart-patrimonio'));
        
        var opcoes = {
            title: {
                show: true,
                text: 'Composição do Patrimônio',
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
                formatter: ({value }) => `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
            },
            legend: {
                show: true,
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
                name: 'Composição por Classe',
                type: 'pie',
                radius: '50%',
                data: ativiClasse.classe.map((classe, index) => ({
                    name: classe,
                    value: ativiClasse.valores[index]
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
