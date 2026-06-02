# Scraper de Licitações - Portal de Compras da Prefeitura de São José / SC

Este projeto consiste num robô de automação (Web Scraper) desenvolvido em Python para capturar, tratar e exportar dados de processos licitatórios diretamente do portal de transparência e compras do município de São José / SC (plataforma Paradigma EGOV).

## 🚀 O que o sistema faz?

1. **Navegação Automatizada:** Abre o navegador de forma autónoma, acede ao Portal do Mural de Licitações de São José/SC e força o carregamento de múltiplos registos através de rolagem infinita (`scroll`).
2. **Interceção de Rede (API):** Em vez de raspar apenas o HTML visual, o robô monitoriza o tráfego de rede em segundo plano e captura diretamente as respostas das requisições JSON vindas da API interna do portal (`PesquisarProcessosPorSituacoesAgrupadas`).
3. **Tratamento de Dados:** * Converte formatos complexos de data (padrão .NET Unix como `/Date(...)/`) para o formato padrão legível (`AAAA-MM-DD HH:MM:SS`).
   * Normaliza os nomes dos órgãos, modalidades e objetos para corrigir eventuais falhas ou caracteres corrompidos de codificação do banco de dados deles (ex: remoção de caracteres invisíveis como `\x13\x12\x12\x13`).
4. **Exportação:** Guarda todas as informações estruturadas e limpas em arquivos locais `.json` prontos para consumo por outros sistemas, dashboards ou relatórios.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Selenium Wire** (Extensão do Selenium que permite intercetar e inspecionar requisições HTTP/HTTPS em tempo de execução)
* **Chrome WebDriver** (Para a emulação e controlo do navegador Chrome)
* **JSON & Datetime** (Para a manipulação, limpeza e formatação dos dados)

## 📌 Status do Projeto
O script cumpre o objetivo de extrair a massa de dados inicial de forma robusta e limpa, eliminando a necessidade de consulta e recolha manual de editais no portal do município.
