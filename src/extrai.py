import requests
import time
import pandas as pd

BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros" # /marcas/59/modelos/5940/anos
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
TEMPO_ESPERA = 0.05

def _fazer_requisicao(endpoint: str):
    url = f"{BASE_URL}/{endpoint}"
    try:
        time.sleep(TEMPO_ESPERA)
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f" Erro ao acessar {url}: {e}")
        return None

def requisicao_e_loop_de_precos(codigo_marca: str, codigo_modelo: str): #-> Função criada definida com dois parâmetros de entrada pra receber apenas string.
    
    dados_finais = []
    
    endpoint_lista = f"marcas/{codigo_marca}/modelos/{codigo_modelo}/anos" 
    anos_versao = _fazer_requisicao(endpoint_lista) 
    
    if not isinstance(anos_versao, list) or not anos_versao: 
        return None

    
    for ano in anos_versao:
        codigo_ano = ano.get('codigo') 
        nome_ano = ano.get('nome') 
        endpoint_preco = f"marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
        detalhes_preco = _fazer_requisicao(endpoint_preco) #
        if detalhes_preco and 'Valor' in detalhes_preco: 
            dados_finais.append({ 
                'Marca': detalhes_preco.get('Marca'),
                'Modelo': detalhes_preco.get('Modelo'),
                'Ano/Versão_Bruto': nome_ano,
                'Valor_FIPE_Bruto': detalhes_preco.get('Valor'),
                'Mes_Referencia': detalhes_preco.get('MesReferencia'),
                'Codigo_FIPE': detalhes_preco.get('CodigoFipe')
            })
            
    
    return pd.DataFrame(dados_finais) 

if __name__ == '__main__':
    df_teste = requisicao_e_loop_de_precos('59', '5940')
    if df_teste is not None:
        print("\nDataFrame bruto extraído com sucesso:")
        print(df_teste.head())