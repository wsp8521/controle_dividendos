function chartComposicaoPatrimonio(data) {
    document.addEventListener("DOMContentLoaded", function () {
        let ativiClasse = JSON.parse(data);
        var grafico = echarts.init(document.getElementById('chart-patrimonio'));

        const total = ativiClasse.valores.reduce((acc, val) => acc + val, 0);

        const option = {
            title: {
                text: 'Composição da Carteira',
                left: 'center',
                top: '5%',
                textStyle: {
                    color: '#000000',
                    fontSize: 16,
                    fontWeight: 'bold'
                }
            },
            tooltip: {
                trigger: 'item',
                show: true,
                formatter: ({ value, percent }) =>
                    `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</br>${percent}%`
            },
            legend: {
                bottom: '5%',
                left: 'center',
                data: ativiClasse.categorias,
                textStyle: { color: '#000000' }
            },
            series: [
                {
                    name: 'Composição por Classe',
                    type: 'pie',
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: true,
                        position: 'center',
                        fontSize: 18,
                        fontWeight: 'bold',
                        color: '#000000',
                        formatter: `R$ ${total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                    },
                    /*emphasis: {
                      label: {
                        show: false,
                        fontSize: 12,
                        fontWeight: 'bold',
                        color: '#000000',
                        formatter: ({ value, percent }) =>
                          `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}\n${percent}%`
                      },
                      itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                      }
                    },*/
                    labelLine: { show: false },
                    data: ativiClasse.classe.map((classe, index) => ({
                        name: classe,
                        value: ativiClasse.valores[index]
                    }))
                }
            ],
            grid: {
                top: '20',
                bottom: '30'
            }
        };

        grafico.setOption(option);

        // Evento quando passa o mouse em uma fatia (hover)
        grafico.on('highlight', function (params) {
            const { value, percent } = params;
            grafico.setOption({
                series: [{
                    label: {
                        formatter: `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}\n${percent}%`
                    }
                }]
            });
        });

        // Evento quando tira o mouse (mouse out)
        grafico.on('downplay', function () {
            grafico.setOption({
                series: [{
                    label: {
                        formatter: `R$ ${total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                    }
                }]
            });
        });

        window.addEventListener('resize', () => grafico.resize());
    });
}
