import unittest
from pathlib import Path
from processamento_de_dados import carregar_tabelas, filtrar_dados_pelo_mes, gerar_numero_de_vendas, gerar_volume_de_vendas, gerar_ticket_medio
import pandas as pd

class TestProcessamentoDeDados(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais para os testes
        self.mes_referencia = '2023-01'
        self.pasta_dados = Path(__file__).parent.parent / 'dados'
        self.arquivo_excel = 'dados.xlsx'
        self.dados_brutos = pd.DataFrame({
            'Data/Hora': pd.date_range(start='2023-01-01', periods=5, freq='D'),
            'Vendedor': ['A', 'B', 'A', 'B', 'A'],
            'Produto': ['X', 'Y', 'X', 'Y', 'X'],
            'Quantidade': [10, 20, 30, 40, 50],
            'Valor Venda': [100, 200, 300, 400, 500]
        })

    def test_filtrar_dados_pelo_mes(self):
        dados_filtrados = filtrar_dados_pelo_mes(self.dados_brutos, self.mes_referencia)
        self.assertEqual(len(dados_filtrados), 5)
        self.assertTrue((dados_filtrados['Data/Hora'].dt.strftime('%Y-%m') == self.mes_referencia).all())

    def test_gerar_numero_de_vendas(self):
        dados_filtrados = filtrar_dados_pelo_mes(self.dados_brutos, self.mes_referencia)
        tabela_vendas = gerar_numero_de_vendas(dados_filtrados)
        self.assertEqual(tabela_vendas.loc['A', 'X'], 90)
        self.assertEqual(tabela_vendas.loc['B', 'Y'], 60)

    def test_gerar_volume_de_vendas(self):
        dados_filtrados = filtrar_dados_pelo_mes(self.dados_brutos, self.mes_referencia)
        tabela_volume = gerar_volume_de_vendas(dados_filtrados)
        self.assertEqual(tabela_volume.loc['A', 'X'], 900.0)
        self.assertEqual(tabela_volume.loc['B', 'Y'], 600.0)

    def test_gerar_ticket_medio(self):
        dados_filtrados = filtrar_dados_pelo_mes(self.dados_brutos, self.mes_referencia)
        tabela_ticket_medio = gerar_ticket_medio(dados_filtrados)
        self.assertAlmostEqual(tabela_ticket_medio.loc['A', 'Valor Venda'], 300.0)
        self.assertAlmostEqual(tabela_ticket_medio.loc['B', 'Valor Venda'], 200.0)

if __name__ == '__main__':
    unittest.main()