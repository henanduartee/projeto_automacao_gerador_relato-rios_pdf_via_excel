import pandas as pd

def carregar_tabelas(mes_referencia, pasta_dados, arquivo_excel):
    """
    Carrega e processa os dados do arquivo Excel para o mês de referência especificado.

    Args:
        mes_referencia (str): Mês de referência no formato 'YYYY-MM'.
        pasta_dados (Path): Caminho para o diretório de dados.
        arquivo_excel (str): Nome do arquivo Excel.

    Returns:
        dict: Dicionário contendo as tabelas de vendas, volume de vendas e ticket médio.
    """
    caminho_dados = pasta_dados / arquivo_excel
    dados_brutos = pd.read_excel(caminho_dados)
    dados_filtrados = filtrar_dados_pelo_mes(dados_brutos=dados_brutos, mes_referencia=mes_referencia)
    tabela_vendas = gerar_numero_de_vendas(dados=dados_filtrados)
    tabela_volume = gerar_volume_de_vendas(dados=dados_filtrados)
    tabela_ticket_medio = gerar_ticket_medio(dados=dados_filtrados)
    return {
        'tabela_vendas': tabela_vendas,
        'tabela_volume': tabela_volume,
        'tabela_tm': tabela_ticket_medio,
    }

def filtrar_dados_pelo_mes(dados_brutos, mes_referencia, coluna_data_hora='Data/Hora'):
    """
    Filtra os dados pelo mês de referência.

    Args:
        dados_brutos (DataFrame): Dados brutos do Excel.
        mes_referencia (str): Mês de referência no formato 'YYYY-MM'.
        coluna_data_hora (str): Nome da coluna que contém a data e hora.

    Returns:
        DataFrame: Dados filtrados pelo mês de referência.

    Raises:
        ValueError: Se nenhum dado for encontrado para o mês de referência.
    """
    filtro = dados_brutos[coluna_data_hora].apply(lambda dt: dt.strftime('%Y-%m')) == mes_referencia
    dados_filtrados = dados_brutos.loc[filtro]
    if dados_filtrados.empty:
        raise ValueError(
            f"Nenhum dado encontrado para o mês {mes_referencia}. Confirme se o mês de referência "
            "está no formato YYYY-MM, e se há dados para este mês."
        )
    return dados_filtrados

def gerar_numero_de_vendas(dados, coluna_vendedor="Vendedor", coluna_produto="Produto", coluna_quantidade="Quantidade"):
    """
    Gera a tabela de número de vendas por vendedor e produto.

    Args:
        dados (DataFrame): Dados filtrados.
        coluna_vendedor (str): Nome da coluna do vendedor.
        coluna_produto (str): Nome da coluna do produto.
        coluna_quantidade (str): Nome da coluna da quantidade.

    Returns:
        DataFrame: Tabela de número de vendas.
    """
    return dados.pivot_table(
        index=coluna_vendedor,
        columns=coluna_produto,
        values=coluna_quantidade,
        aggfunc='sum',
        margins=True,
        margins_name="TOTAL",
    ).sort_values(by='TOTAL')

def gerar_volume_de_vendas(dados, coluna_vendedor="Vendedor", coluna_produto="Produto", coluna_volume="Valor Venda"):
    """
    Gera a tabela de volume de vendas por vendedor e produto.

    Args:
        dados (DataFrame): Dados filtrados.
        coluna_vendedor (str): Nome da coluna do vendedor.
        coluna_produto (str): Nome da coluna do produto.
        coluna_volume (str): Nome da coluna do volume de vendas.

    Returns:
        DataFrame: Tabela de volume de vendas.
    """
    return dados.pivot_table(
        index=coluna_vendedor,
        columns=coluna_produto,
        values=coluna_volume,
        aggfunc='sum',
        margins=True,
        margins_name="TOTAL",
    ).sort_values(by='TOTAL').astype(float)

def gerar_ticket_medio(dados, coluna_vendedor="Vendedor", coluna_volume="Valor Venda"):
    """
    Gera a tabela de ticket médio por vendedor.

    Args:
        dados (DataFrame): Dados filtrados.
        coluna_vendedor (str): Nome da coluna do vendedor.
        coluna_volume (str): Nome da coluna do volume de vendas.

    Returns:
        DataFrame: Tabela de ticket médio.
    """
    return dados.groupby(coluna_vendedor)[[coluna_volume]].mean()

if __name__ == '__main__':  # Testando o código
    from caminhos import PASTA_DADOS
    tabelas = carregar_tabelas(mes_referencia='2023-01', pasta_dados=PASTA_DADOS, arquivo_excel='dados.xlsx')
    for nome_tabela, tabela in tabelas.items():
        print('\n -----', nome_tabela)
        print(tabela)
