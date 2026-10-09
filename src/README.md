Projeto desenvolvido com foco em análise de dados, extração e tratamento de informações, geração de relatórios e experimentação com inteligência artificial.

## Objetivos

O projeto foi desenvolvido para explorar dados relacionados ao funil de propostas, gerar informações úteis para a análise do negócio e automatizar etapas de processamento de documentos.

## Etapas do projeto

### 1. Análise do funil de propostas

- Carregamento e exploração dos dados fornecidos.
- Tratamento e normalização dos dados.
- Análise do funil de propostas e de seus resultados.
- Análise de indicadores relacionados ao LTV (_Lifetime Value_) e ao LTV em relação ao valor do imóvel (LTV ratio).
- Análise dos resultados para identificar oportunidades de melhoria e apoiar decisões de negócio.
- Geração de um relatório em PDF com os resultados da análise.

**Principal saída:** `outputs/relatorio_analise.pdf`

### 2. Extração e normalização de dados dos laudos

Implementação de uma etapa de leitura e processamento dos arquivos de laudos imobiliários fornecidos no desafio.

- Leitura dos arquivos de entrada.
- Extração de campos específicos utilizando expressões regulares (regex).
- Correção de inconsistências identificadas nos campos extraídos.
- Normalização e validação de datas e valores numéricos.
- Exportação dos dados processados para JSON.

**Principal saída:** `outputs/laudos_extraidos.json`

### 3. Análise de textos com inteligência artificial

Implementação de uma etapa voltada à análise de textos com o uso de inteligência artificial.

A integração foi iniciada, mas não foi concluída devido a um erro de autenticação da API (`401 UNAUTHENTICATED ACCESS_TOKEN_TYPE_UNSUPPORTED`). Portanto, essa etapa permanece incompleta e precisa de ajustes para funcionar corretamente.

## Estrutura do projeto

```text
test-baribank
├── outputs/
│   ├── relatorio_analise.pdf
│   └── laudos_extraidos.json
├── src/
│   ├── analysis/
│   │   ├── data_loader.py
│   │   ├── treatment.py
│   │   └── funnel_analysis.py
│   ├── config/
│   │   └── config.py
│   ├── data/
│   │   ├── laudos_avaliacao/
│   │   └── propostas_creditos.csv
│   ├── docs/
│   ├── errors/
│   │   └── constants.py
│   ├── extraction/
│   │   ├── reader.py
│   │   └── json_writer.py
│   ├── reports/
│   │   └── pdf_report.py
│   ├── services/
│   │   ├── field_extractor.py
│   │   ├── normalizer_data.py
│   │   ├── ltv.py
│   │   └── weekly_analysis.py
│   ├── utils/
│   │   └── data_exploration.py
│   ├── app.py
│   ├── main.py
│   └── main_extract.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Como executar o projeto

### Pré-requisitos

- Python instalado.
- Git instalado.
- Acesso aos arquivos de entrada do desafio.
- Credenciais de API, caso sejam necessárias para executar alguma etapa que dependa de serviços externos.

### 1. Clonar o repositório

```bash
git clone https://github.com/CodIguinhoDev/test-baribank
cd test-baribank
```

### 2. Criar e ativar o ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example` e preencha as variáveis necessárias.

### 5. Executar a aplicação

A aplicação para rodar a primeira/segunda etapa pode ser iniciada pelo ponto de entrada `src/main.py`. Considerando que o projeto esteja organizado como um pacote Python, o comando é:

```bash
python -m src.main ou python main.py
```

A etapa de análise de textos com IA possui um ponto de entrada separado:

```bash
python -m src.main_extract ou python main_extract.py
```

A segunda execução depende da configuração correta da integração de IA e, no estado atual, falhou devido ao problema de autenticação mencionado anteriormente.

## Resultados e limitações

- O projeto contempla o processamento e a análise dos dados disponibilizados no desafio.
- O relatório em PDF registra os resultados da análise do funil de propostas.
- Os laudos processados são exportados para um arquivo JSON.
- A integração de inteligência artificial permanece incompleta devido a um erro de autenticação da API.

## Tecnologias utilizadas

- **Python** — desenvolvimento e processamento de dados.
- **Pandas** — manipulação e análise de dados tabulares.
- **Regex** — extração e tratamento de campos textuais.
- **JSON** — armazenamento estruturado dos dados extraídos.
- **reportlab** — geração do relatório da análise (pdf).
- **APIs de inteligência artificial** — tentativa de integração para análise de textos.

> Consulte `requirements.txt` para verificar as dependências efetivamente utilizadas pelo projeto.

## Tempo de desenvolvimento

**Tempo total:**: 34 horas
