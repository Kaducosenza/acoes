import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Lista de empresas brasileiras para análise (exemplo: setores perenes)
Energia_Elétrica = ['TAEE11.SA','EGIE3.SA','CMIG4.SA','TRPL4.SA','CPLE6.SA','ENBR3.SA', 'ALUP11.SA', 'NEOE3.SA', 'ENGI11.SA', 'CEEB3.SA']
acoes = ['BBSE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ITSA4.SA', 'SANB11.SA', 'SANB4.SA','SANB3.SA','SAPR4.SA','TAEE4.SA','TAEE11.SA','ISAE4.SA','SAPR11.SA','VINO11.SA','HGLG11.SA']
Saneamento =['SBSP3.SA','SAPR4.SA','CSMG3.SA','ABEV3.SA', 'KLBN11.SA', 'SUZB3.SA', 'MRFG3.SA', 'BRFS3.SA']
Bancos = ['ITUB4.SA','BBDC4.SA','BBAS3.SA','SANB11.SA']
Telecomunicações =['VIVT3.SA','TIMS3.SA']
Seguros = ['BBSE3.SA','PSSA3.SA']
saude = ['RDOR3.SA', 'HAPV3.SA', 'FLRY3.SA', 'PARD3.SA', 'QUAL3.SA']
alimentos_bebidas = ['MDIA3.SA', 'SLCE3.SA', 'BRAP4.SA', 'RAIL3.SA', 'ARZZ3.SA']
acoes = list(set(acoes + Energia_Elétrica + Saneamento + Bancos + Telecomunicações + Seguros + saude + alimentos_bebidas))

acoes_america = ['AAPL','MSFT','GOOGL','NVDA','KO','PG','PEP','WMT','JPM','V','MA','JNJ','PFE','UNH','XOM','CVX','NEE','MMM','HON','BA','PG','XOM','CVX','BLK','MSFT','AAPL','O','SPG','T','RF','ALLY','NXST','WEN','FIBK', 'STNG','CRI','VRTS','DHT','MO','BTI', 'PEAK','VZ','T', 'KMI','MMM','DVN','WHR','PFE','NEE']
acoes_america = list(set(acoes_america)) 

acoes_europa = ['NG.L', 'BP.L', 'LGEN.L', 'AV.L', 'ULVR.L', 'BATS.L', 'SHEL.L', 'VOD.L', 'IMB.L', 'RIO.L','OR.PA', 'TTE.PA', 'BN.PA', 'ENGI.PA', 'RMS.PA', 'EL.PA', 'VIV.PA', 'SU.PA', 'CAP.PA', 'AIR.PA','DTE.DE', 'ALV.DE', 'BAS.DE', 'VNA.DE', 'DB1.DE', 'SIE.DE', 'BMW.DE', 'LIN.DE', 'RWE.DE', 'SAP.DE','IBE.MC', 'TEF.MC', 'SAN.MC', 'REP.MC', 'ACS.MC', 'BBVA.MC', 'ITX.MC', 'AENA.MC', 'FER.MC', 'ENA.MC','NOVO-B.CO', 'TELIA.ST', 'EQNR.OL', 'FORTUM.HE', 'MAERSK-B.CO', 'NDAFI.HE', 'ERIC-B.ST', 'SSAB-A.ST', 'ORK.OL', 'STL.OL']
acoes_europa = acoes_europa + ['SHEL.L', 'ULVR.L', 'BATS.L', 'TTE.PA', 'OR.PA', 'BN.PA', 'ALV.DE', 'SIE.DE', 'DTE.DE', 'IBE.MC', 'SAN.MC', 'ELE.MC','NOVO-B.CO', 'EQNR.OL', 'TELIA.ST']
acoes_europa = list(set(acoes_europa))

hoje = datetime.now()
inicio = hoje - timedelta(days=6*365)  # Últimos 6 anos

# Função para coletar dados históricos e calcular indicadores
def calcular_indicadores_historicos(acoes, inicio, hoje):
    resultados = []
    for acao in acoes:
        try:
            ticker = yf.Ticker(acao)
            hist = ticker.history(start=inicio, end=hoje)

            # Verificar se 'Dividends' está presente no DataFrame
            if 'Dividends' not in hist.columns:
                print(f"Sem dados de dividendos para {acao}. Pulando.")
                continue

            # Dividendos e número de pagamentos por ano
            dividendos = hist['Dividends'].resample('YE').sum()  # Soma dos dividendos por ano

            # Preço atual e preço médio
            preco_atual = round(hist['Close'].iloc[-1], 2)  # Último preço
            preco_medio = round(hist['Close'].mean(), 2)   # Preço médio no período

            # Informações financeiras
            infos = ticker.info
            lpa = infos.get('trailingEps', 0)  # Lucro por Ação
            vpa = infos.get('bookValue', 0)    # Valor Patrimonial por Ação

            # Calcular indicadores usando Preço Médio
            indicadores = pd.DataFrame()
            indicadores['Dividendos'] = dividendos
            indicadores['Preço Médio'] = preco_medio
            indicadores['Preço Atual'] = preco_atual
            indicadores['DY Médio (%)'] = (indicadores['Dividendos'] / preco_medio) * 100
            indicadores['DY Atual (%)'] = (indicadores['Dividendos'] / preco_atual) * 100
            indicadores['P/L Médio'] = preco_medio / lpa if lpa > 0 else None
            indicadores['P/L Atual'] = preco_atual / lpa if lpa > 0 else None
            indicadores['P/VP Médio'] = preco_medio / vpa if vpa > 0 else None
            indicadores['P/VP Atual'] = preco_atual / vpa if vpa > 0 else None

            # Filtrar e calcular médias
            indicadores = indicadores.dropna()
            media_dy_medio = indicadores['DY Médio (%)'].mean()
            media_dy_atual = indicadores['DY Atual (%)'].mean()
            media_pl_medio = indicadores['P/L Médio'].mean() if 'P/L Médio' in indicadores else None
            media_pl_atual = indicadores['P/L Atual'].mean() if 'P/L Atual' in indicadores else None
            media_pvp_medio = indicadores['P/VP Médio'].mean() if 'P/VP Médio' in indicadores else None
            media_pvp_atual = indicadores['P/VP Atual'].mean() if 'P/VP Atual' in indicadores else None
            Dividendos = (indicadores['Dividendos'].sum())/6

            # Adicionar resultados ao DataFrame final
            resultados.append({
                "Ticker": acao,
                "Preço Atual": preco_atual,
                "Preço Médio": preco_medio,
                "Valor Teto": None,
                "Dividendos": Dividendos,
                "DY Médio (%)": media_dy_medio,
                "DY Atual (%)": media_dy_atual,
                "P/L Médio": media_pl_medio,
                "P/L Atual": media_pl_atual,
                "P/VP Médio": media_pvp_medio,
                "P/VP Atual": media_pvp_atual
            })


        except Exception as e:
            print(f"Erro ao processar {acao}: {e}")
            resultados.append({
                "Ticker": acao,
                "Preço Atual": None,
                "Preço Médio": None,
                "Valor Teto": None,
                "DY Médio (%)": None,
                "DY Atual (%)": None,
                "P/L Médio": None,
                "P/L Atual": None,
                "P/VP Médio": None,
                "P/VP Atual": None,
            })
    return pd.DataFrame(resultados)
def grafico(grafico):
    plt.figure(figsize=(14, 8))
    
    largura_barras = 0.4  # Largura das barras
    x = range(len(grafico))  # Índices para os tickers

    # Barras de DY Atual (azul)
    barras_dy_atual = plt.bar(
        [i - largura_barras / 2 for i in x], 
        grafico['DY Atual (%)'], 
        width=largura_barras, 
        label='DY Atual (%)', 
        color='blue', alpha=0.6
    )

    # Barras de DY Médio (vermelho)
    barras_dy_medio = plt.bar(
        [i + largura_barras / 2 for i in x], 
        grafico['DY Médio (%)'], 
        width=largura_barras, 
        label='DY Médio (%)', 
        color='red', alpha=0.6
    )

    # Adicionar texto dentro das barras de DY Atual
    for barra in barras_dy_atual:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,  # Centro da barra
            altura / 2,                             # Meio da barra
            f"{altura:.2f}%",                       # Texto formatado como porcentagem
            ha='center', va='center', color='white', fontsize=10, fontweight='bold'
        )

    # Adicionar texto dentro das barras de DY Médio
    for barra in barras_dy_medio:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,  # Centro da barra
            altura / 2,                             # Meio da barra
            f"{altura:.2f}%",                       # Texto formatado como porcentagem
            ha='center', va='center', color='white', fontsize=10, fontweight='bold'
        )
    
    # Configurações do gráfico
    plt.xticks(x, grafico['Ticker'], rotation=45)
    plt.ylabel("Dividend Yield (%)")
    plt.title("Comparação do Dividend Yield (DY) - Atual x Médio")
    plt.legend()
    plt.tight_layout()
    plt.show()
def grafico_2(grafico):
    plt.figure(figsize=(14, 8))
    
    largura_barras = 0.25  # Ajustar a largura das barras para acomodar 3 grupos
    x = range(len(grafico))  # Índices para os tickers

    # Barras de DY Atual (azul)
    barras_dy_atual = plt.bar(
        [i - largura_barras for i in x], 
        grafico['Preço Atual'], 
        width=largura_barras, 
        label='Preço Atual', 
        color='blue', alpha=0.6
    )

    # Barras de DY Médio (vermelho)
    barras_dy_medio = plt.bar(
        [i for i in x], 
        grafico['Preço Médio'], 
        width=largura_barras, 
        label='Preço Médio', 
        color='red', alpha=0.6
    )

    # Barras adicionais (verde)
    barras_extra = plt.bar(
        [i + largura_barras for i in x], 
        grafico['Valor Teto'], 
        width=largura_barras, 
        label='Valor Teto', 
        color='green', alpha=0.6
    )

    # Adicionar texto dentro das barras de DY Atual
    def barras (bara):
        for barra in bara:
         altura = barra.get_height()
         plt.text(
            barra.get_x() + barra.get_width() / 2,  # Centro da barra
            altura / 2,                             # Meio da barra
            f"R${altura:.2f}",                       # Texto formatado como porcentagem
            ha='center', va='center', color='black', fontsize=10, fontweight='bold',rotation=90 
        )
    barras(barras_dy_atual)
    barras(barras_dy_medio)
    barras(barras_extra)
    
    # Configurações do gráfico
    plt.xticks(x, grafico['Ticker'], rotation=45)
    plt.ylabel("Preço")
    plt.title("Comparação do Preço - Atual x Médio x Teto")
    plt.legend()
    plt.tight_layout()
    plt.show()
  
def media_geral (acoes):
    DY = acoes['DY Atual (%)'].mean()
    DY_m = acoes["DY Médio (%)"].mean()
    PL = acoes['P/L Atual'].mean()
    PL_m = acoes['P/L Médio'].mean()
    PVP = acoes['P/VP Atual'].mean()
    PVP_m = acoes['P/VP Médio'].mean()
    print(f'DY {DY:.2f}, P/L {PL:.2f},P/VP {PVP:.2f}')
    print(f'DY {DY_m:.2f}, P/L {PL_m:.2f},P/VP {PVP_m:.2f}')



resultados = calcular_indicadores_historicos(acoes, inicio, hoje)
resultados['DY Atual (%)'] = pd.to_numeric(resultados['DY Atual (%)'], errors='coerce')
resultados = resultados.dropna(subset=['DY Atual (%)', 'P/L Atual', 'P/VP Atual'])
DY = 6 
# Filtrar ações que atendem aos critérios do Método Barsi
filtro_barsi = resultados[
    (resultados['DY Atual (%)'] > 6) &   # DY médio acima de 6%
    (resultados['P/L Atual'] < 15) &    # P/L médio abaixo de 15
    (resultados['P/VP Atual'] < 2)      # P/VP médio abaixo de 2
]
filtro_barsi ["Valor Teto"] = round(filtro_barsi["Dividendos"]/ (DY/100) ,2)

print(filtro_barsi)
grafico(filtro_barsi)
grafico_2(filtro_barsi)



resultados_2 = calcular_indicadores_historicos(acoes_america, inicio, hoje)
resultados_2['DY Atual (%)'] = pd.to_numeric(resultados_2['DY Atual (%)'], errors='coerce')
resultados_2 = resultados_2.dropna(subset=['DY Atual (%)', 'P/L Atual', 'P/VP Atual'])
DY_2 = 3

filtro_barsi_2 = resultados_2[
    (resultados_2['DY Atual (%)'] > DY_2) &   # DY médio acima de 3%
    (resultados_2['P/L Atual'] < 20) &    # P/L médio abaixo de 20
    (resultados_2['P/VP Atual'] < 3)      # P/VP médio abaixo de 3
]
filtro_barsi_2 ["Valor Teto"] = round(filtro_barsi_2 ["Dividendos"]/ (DY_2/100) ,2)
print()
print(filtro_barsi_2)
grafico(filtro_barsi_2)
grafico_2(filtro_barsi_2)
