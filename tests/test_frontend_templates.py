"""
Testes para validar renderização do front-end em diferentes cenários.
Utiliza FastAPI TestClient para simular requisições e verificar templates.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from source.main import app, normalize_process_result_for_template


client = TestClient(app)


class TestHomePageRoute:
    """Testes da página inicial (home)."""
    
    def test_home_page_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
        
    def test_home_page_contains_search_form(self):
        response = client.get("/")
        assert "buscaprocesso" in response.text
        assert '<form' in response.text
        
    def test_home_page_contains_assistant_banner(self):
        response = client.get("/")
        assert "assistant-banner" in response.text
        assert "juridico-bot-amigo" in response.text
        

class TestAboutPageRoute:
    """Testes da página Sobre."""
    
    def test_about_page_returns_200(self):
        response = client.get("/sobre")
        assert response.status_code == 200
        
    def test_about_page_has_content(self):
        """Verifica se a página Sobre carrega com conteúdo."""
        response = client.get("/sobre")
        assert len(response.text) > 500  # Página tem conteúdo
        

class TestProcessoPageWithValidData:
    """Testes da página de processo com dados válidos (1º grau)."""
    
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_renders_valid_first_grau_data(self, mock_get_info):
        """Testa renderização com dados válidos de 1º grau."""
        # Mock de resposta válida
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação Cível",
                    "area": "Cível",
                    "assunto": "Indenização",
                    "data": "2024-01-10",
                    "juiz": "Juiz Silva",
                    "valor": "R$ 5.000,00",
                    "partes": [
                        {
                            "nome": "João Silva",
                            "tipo_de_participacao": "Autor",
                            "advogados": ["Dr. Carlos"]
                        }
                    ],
                    "movimentacoes": [
                        {
                            "data": "2024-01-15",
                            "descricao": "Petição inicial"
                        }
                    ]
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        assert "João Silva" in response.text
        assert "Petição inicial" in response.text
        
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_shows_both_graus_when_available(self, mock_get_info):
        """Testa página quando ambas instâncias têm dados."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação Cível",
                    "area": "Cível",
                    "assunto": "Teste",
                    "data": "2024-01-10",
                    "juiz": "Juiz Silva",
                    "valor": "R$ 1.000,00",
                    "partes": [],
                    "movimentacoes": []
                },
                "Segunda Instância": {
                    "classe": "Recurso de Apelação",
                    "area": "Cível",
                    "assunto": "Teste",
                    "data": "2024-02-10",
                    "juiz": "Desembargador Costa",
                    "valor": "R$ 1.000,00",
                    "partes": [],
                    "movimentacoes": []
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        assert "Primeira Instância" in response.text
        assert "Segunda Instância" in response.text
        assert "Juiz Silva" in response.text
        assert "Desembargador Costa" in response.text
        

class TestProcessoPageWithErrors:
    """Testes da página de processo em cenários de erro."""
    
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_handles_timeout_gracefully(self, mock_get_info):
        """Testa renderização quando há timeout."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "ERROR": "Tempo limite excedido ao consultar"
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        # Verifica que há um alert classe do Bootstrap
        assert "alert" in response.text
        
    def test_processo_page_handles_invalid_cnj_number(self):
        """Testa validação de CNJ inválido."""
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "NUMERO-INVALIDO"}
        )
        
        assert response.status_code == 200
        # Deve renderizar erro de validação
        assert ("Validação" in response.text or "alert" in response.text)
        
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_handles_partial_data(self, mock_get_info):
        """Testa renderização com dados parciais de um grau apenas."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação",
                    "area": "Cível",
                    "assunto": "Teste",
                    "data": "2024-01-10",
                    "juiz": "Juiz",
                    "valor": "R$ 0,00",
                    "partes": [],
                    "movimentacoes": []
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        assert "Primeira Instância" in response.text


class TestNormalizeProcessResult:
    """Testes para a função que normaliza dados antes do template."""
    
    def test_normalize_valid_process_result(self):
        """Testa normalização com resultado válido."""
        result = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {"classe": "Ação"}
        }
        
        normalized = normalize_process_result_for_template("1234567-89.1234.5.67.8900", result)
        
        # Nova estrutura desaninhada: flatten do Resultado
        assert normalized["id"] == "1234567-89.1234.5.67.8900"
        assert normalized["classe"] == "Ação"
        assert "Resultado" not in normalized
        
    def test_normalize_non_dict_result(self):
        """Testa normalização quando resultado não é dict."""
        normalized = normalize_process_result_for_template(
            "1234567-89.1234.5.67.8900",
            None
        )
        
        assert "Erro" in str(normalized.get("ERROR", ""))
        
    def test_normalize_validator_error_dict(self):
        """Testa normalização com erro de validação."""
        error_result = {
            "numero_processo": ["Formato inválido"]
        }
        
        normalized = normalize_process_result_for_template(
            "INVALIDO",
            error_result
        )
        
        assert "ERROR" in normalized
        assert "Formato inválido" in normalized["ERROR"]
        
    def test_normalize_preserves_process_id(self):
        """Testa que a normalização preserva o ID do processo."""
        test_id = "1234567-89.1234.5.67.8900"
        normalized = normalize_process_result_for_template(test_id, None)
        
        assert normalized["id"] == test_id


class TestProcessoPageStructure:
    """Testes de estrutura e acessibilidade do template de processo."""
    
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_has_main_container(self, mock_get_info):
        """Verifica se a página tem estrutura de container principal."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação",
                    "area": "Cível",
                    "assunto": "Teste",
                    "data": "2024-01-10",
                    "juiz": "Juiz",
                    "valor": "R$ 1.000,00",
                    "partes": [],
                    "movimentacoes": []
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        assert "process-container" in response.text
        assert "Informações do Processo" in response.text
        
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_has_assistant_panel(self, mock_get_info):
        """Verifica se a página tem painel do assistente jurídico."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação",
                    "area": "Cível",
                    "assunto": "Teste",
                    "data": "2024-01-10",
                    "juiz": "Juiz",
                    "valor": "R$ 1.000,00",
                    "partes": [],
                    "movimentacoes": []
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        assert "assistant-panel" in response.text
        assert "juridico-bot-amigo" in response.text
        
    @patch('source.main.get_processo_info_by_id')
    def test_processo_page_has_floating_assistant_fab(self, mock_get_info):
        """Verifica se há botão flutuante do assistente."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação",
                    "area": "Cível",
                    "assunto": "Teste",
                    "data": "2024-01-10",
                    "juiz": "Juiz",
                    "valor": "R$ 1.000,00",
                    "partes": [],
                    "movimentacoes": []
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        assert response.status_code == 200
        assert "assistant-fab" in response.text
        
    def test_home_page_has_navigation_menu(self):
        """Verifica se menu de navegação está presente."""
        response = client.get("/")
        assert response.status_code == 200
        assert "<nav" in response.text
        assert "Home" in response.text or "Sobre" in response.text


class TestDataRendering:
    """Testes de renderização correta dos dados no template."""
    
    @patch('source.main.get_processo_info_by_id')
    def test_all_process_fields_are_displayed(self, mock_get_info):
        """Testa que todos os campos principais do processo são exibidos."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação Cível",
                    "area": "Família",
                    "assunto": "Guarda",
                    "data": "2024-03-15",
                    "juiz": "Dr. Silva",
                    "valor": "R$ 2.500,00",
                    "partes": [
                        {
                            "nome": "Maria",
                            "tipo_de_participacao": "Autora",
                            "advogados": ["Dr. João"]
                        }
                    ],
                    "movimentacoes": []
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        # Verificar presença de campos principais
        assert "Ação Cível" in response.text
        assert "Família" in response.text
        assert "Guarda" in response.text
        assert "Dr. Silva" in response.text
        assert "R$ 2.500,00" in response.text
        assert "Maria" in response.text
        assert "Dr. João" in response.text
        
    @patch('source.main.get_processo_info_by_id')
    def test_partes_and_movimentacoes_are_in_accordions(self, mock_get_info):
        """Testa que partes e movimentações estão em seções accordion."""
        mock_get_info.return_value = {
            "id": "1234567-89.1234.5.67.8900",
            "Resultado": {
                "Primeira Instância": {
                    "classe": "Ação",
                    "area": "Teste",
                    "assunto": "Teste",
                    "data": "2024-01-10",
                    "juiz": "Juiz",
                    "valor": "R$ 1.000,00",
                    "partes": [{"nome": "Parte 1", "tipo_de_participacao": "Autor", "advogados": []}],
                    "movimentacoes": [{"data": "2024-01-01", "descricao": "Movimentação 1"}]
                }
            }
        }
        
        response = client.post(
            "/buscaprocesso",
            data={"id_processo": "1234567-89.1234.5.67.8900"}
        )
        
        # Verificar que dados estão presentes
        assert "Parte 1" in response.text
        assert "Movimentação 1" in response.text
        # Verificar que há estrutura de accordion
        assert "collapse" in response.text or "accordion" in response.text
