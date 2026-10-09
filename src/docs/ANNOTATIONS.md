## 1. Objetivo e organização do processo

Esta etapa teve como objetivo investigar a estrutura e a qualidade da base de propostas de crédito, identificar inconsistências, avaliar valores ausentes e duplicidades e definir os tratamentos necessários antes das análises de negócio.

O processo foi organizado em três módulos principais:

- `data_loader.py`: responsável pelo carregamento do arquivo CSV.
- `data_exploration.py`: responsável pelas verificações de estrutura, tipos, valores ausentes, duplicidades e inconsistências.
- `treatment.py`: responsável pela aplicação dos tratamentos definidos durante a exploração.

A exploração foi realizada antes do tratamento para que as alterações na base fossem fundamentadas nos dados observados e nas regras estabelecidas pelo desafio.

---

## 2. Estrutura do dataset

### 2.1. Verificação da estrutura — `check_dataset_structure()`

O arquivo original possui **6.400 registros e 19 colunas**.

As colunas identificadas foram:

|  Nº | Coluna                     |
| --: | -------------------------- |
|   1 | `id_proposta`              |
|   2 | `data_entrada`             |
|   3 | `canal_origem`             |
|   4 | `cidade`                   |
|   5 | `uf`                       |
|   6 | `tipo_imovel`              |
|   7 | `valor_imovel`             |
|   8 | `valor_solicitado`         |
|   9 | `prazo_meses`              |
|  10 | `score_credito`            |
|  11 | `idade_cliente`            |
|  12 | `renda_mensal_declarada`   |
|  13 | `flag_cliente_recorrente`  |
|  14 | `consultor_id`             |
|  15 | `etapa_max_funil`          |
|  16 | `status_final`             |
|  17 | `tempo_analise_dias`       |
|  18 | `data_assinatura_contrato` |
|  19 | `taxa_juros_aa`            |

### 2.2. Diferença em relação ao dicionário de dados

O dicionário fornecido no desafio apresenta a variável `ltv`, mas essa coluna não está presente diretamente no CSV.

Como o LTV pode ser calculado a partir de `valor_solicitado` e `valor_imovel`, a variável foi derivada durante a análise.

**Decisão:** não foi necessário buscar uma coluna inexistente no arquivo. O indicador foi calculado a partir das informações disponíveis, após a preparação dos valores necessários.

---

## 3. Tipos e padronização dos dados

### 3.1. Verificação dos tipos — `check_data_types()`

A análise dos tipos identificou duas colunas armazenadas como `str`, embora representassem outros tipos de informação:

- `valor_imovel`: valor monetário.
- `data_entrada`: data de entrada da proposta.

A investigação dos valores mostrou que a maioria dos registros seguia um padrão predominante, mas existiam exceções de representação.

Essas diferenças precisaram ser tratadas para permitir conversões consistentes e evitar falhas nos cálculos e nas análises temporais.

### 3.2. Tratamento de `valor_imovel`

**Função de exploração:** `find_invalid_property_values()`

Dos 6.400 registros originais:

- 6.397 valores foram convertidos diretamente para o tipo numérico.
- 3 registros apresentaram o prefixo `R$` e não foram convertidos inicialmente.

#### Registros identificados

| Índice | Valor original  |
| -----: | --------------- |
|    704 | `R$ 574857.06`  |
|   2800 | `R$ 1124062.82` |
|   5999 | `R$ 497076.06`  |

Os três valores apresentavam uma representação textual diferente dos demais. A inspeção não indicou, por si só, que os valores monetários fossem inválidos; a inconsistência estava no prefixo textual.

#### Tratamento realizado

O prefixo `R$` foi removido e a coluna foi convertida para o formato numérico. Após o tratamento, os três registros passaram a permitir a conversão.

#### Resumo estatístico inicial

Considerando os valores convertidos antes da remoção dos terrenos:

| Estatística | Valor aproximado |
| ----------- | ---------------: |
| Mínimo      |       R$ 119.954 |
| Mediana     |       R$ 699.662 |
| Média       |       R$ 782.783 |
| Máximo      |     R$ 3.741.993 |

Não foram identificados valores iguais a zero ou negativos nessa verificação.

A média superior à mediana indica uma distribuição possivelmente influenciada por imóveis de maior valor. Essa observação, isoladamente, não permite determinar a causa da diferença, mas constitui um ponto de atenção para a análise exploratória.

**Decisão:** os três registros foram preservados após a normalização, pois a inconsistência identificada estava na representação textual e não justificava a exclusão dos dados.

### 3.3. Tratamento de `data_entrada`

**Função de exploração:** `find_invalid_entry_dates()`

Dos 6.400 registros:

- 6.397 apresentaram o formato predominante.
- 3 apresentaram uma representação diferente.

#### Registros identificados

| Índice | Valor original | Formato identificado |
| -----: | -------------- | -------------------- |
|    150 | `11/04/2025`   | `DD/MM/YYYY`         |
|    151 | `20/04/2025`   | `DD/MM/YYYY`         |
|    152 | `07/12/2024`   | `DD/MM/YYYY`         |

A maior parte dos registros utilizava o formato `YYYY-MM-DD`, enquanto os três casos identificados utilizavam `DD/MM/YYYY`.

Os registros são consecutivos no arquivo. Isso pode indicar uma origem comum, mas não há evidência suficiente para confirmar essa hipótese.

A inconsistência identificada estava no formato de representação das datas, não necessariamente na validade das datas em si.

#### Tratamento realizado

Os formatos foram normalizados para permitir a conversão consistente da coluna para um tipo de data.

Após a conversão, o intervalo observado foi:

| Verificação                 | Resultado    |
| --------------------------- | ------------ |
| Data mínima                 | `2024-01-11` |
| Data máxima                 | `2025-12-29` |
| Datas futuras identificadas | Nenhuma      |

**Decisão:** os três registros foram mantidos e as datas foram padronizadas, preservando a informação temporal original.

---

## 4. Análise de valores ausentes

### 4.1. Verificação — `check_missing_values()`

Foram identificados valores ausentes em duas colunas:

| Coluna                     | Valores ausentes | Valores preenchidos |
| -------------------------- | ---------------: | ------------------: |
| `data_assinatura_contrato` |            5.159 |               1.241 |
| `taxa_juros_aa`            |            5.159 |               1.241 |

Para investigar o significado das ausências, os resultados foram cruzados com a coluna `status_final`.

A análise mostrou que:

- Os 1.241 registros com `status_final = "Contratada"` possuem `data_assinatura_contrato` e `taxa_juros_aa` preenchidas.
- Nos demais status, esses dois campos estão ausentes.

O padrão observado sugere que os campos estão associados à conclusão da contratação e não precisam estar preenchidos para todas as propostas.

### 4.2. Tratamento e justificativa

**Decisão:** os valores ausentes foram mantidos, sem preenchimento artificial ou exclusão dos registros.

Preencher esses campos sem informações reais poderia introduzir dados incorretos. Da mesma forma, remover as propostas por possuírem campos ausentes poderia excluir registros válidos de etapas anteriores do funil.

A decisão foi fundamentada no padrão observado e no significado das variáveis no processo de negócio.

---

## 5. Verificação de duplicidades

Foram realizadas duas verificações distintas para avaliar a possibilidade de registros duplicados.

### 5.1. Duplicidade de identificadores

Foi verificada a coluna `id_proposta`.

**Resultado:** nenhum identificador de proposta repetido foi encontrado.

### 5.2. Duplicidade de linhas completas

Também foi verificada a existência de linhas completamente duplicadas.

**Resultado:** nenhuma linha integralmente duplicada foi encontrada.

### 5.3. Decisão

Nenhuma exclusão foi necessária nessa etapa. Como não foram identificadas duplicidades nas verificações realizadas, não havia evidência que justificasse a remoção de registros por esse motivo.

---

## 6. Exploração de variáveis categóricas

### 6.1. Verificação — `check_categorical_values()`

Foram exploradas as distribuições das seguintes variáveis:

- `uf`
- `cidade`
- `tipo_imovel`
- `canal_origem`
- `etapa_max_funil`
- `flag_cliente_recorrente`
- `status_final`

A análise teve como objetivo identificar categorias inconsistentes, diferenças de representação textual e valores que precisassem ser investigados antes das análises de negócio.

### 6.2. Inconsistências em `canal_origem`

Foram identificadas categorias que representavam a mesma origem, mas apresentavam diferenças de capitalização:

| Representação identificada  | Problema                                |
| --------------------------- | --------------------------------------- |
| `Mídia paga` / `mídia paga` | Diferença entre maiúsculas e minúsculas |
| `Indicação` / `indicação`   | Diferença entre maiúsculas e minúsculas |
| `Organico` / `organico`     | Diferença entre maiúsculas e minúsculas |

Quando utilizadas diretamente em agrupamentos, essas variações poderiam fazer com que uma mesma origem fosse contabilizada como categorias distintas.

### 6.3. Tratamento realizado

As categorias foram padronizadas para uma representação única, com remoção de espaços desnecessários e uniformização da capitalização.

**Decisão:** as categorias equivalentes foram normalizadas, sem alterar o significado das origens registradas.

As demais variáveis categóricas foram examinadas durante a exploração. Não foram registrados aqui problemas adicionais específicos que justificassem tratamentos além dos descritos nas seções seguintes.

---

## 7. Remoção de propostas do tipo `Terreno`

O desafio determina explicitamente que as propostas cujo `tipo_imovel` seja `Terreno` devem ser removidas da análise.

### 7.1. Resultado da identificação

Foram identificadas **535 propostas** classificadas como `Terreno`.

### 7.2. Tratamento realizado

Os 535 registros foram removidos da base utilizada nas análises.

| Etapa                           | Quantidade de registros |
| ------------------------------- | ----------------------: |
| Base original                   |                   6.400 |
| Propostas removidas (`Terreno`) |                     535 |
| Base após a remoção             |                   5.865 |

### 7.3. Justificativa

A remoção foi realizada por se tratar de uma regra explícita do desafio, e não de uma decisão baseada apenas na distribuição estatística dos dados.

**Decisão:** utilizar a base com 5.865 registros nas análises posteriores, respeitando o escopo definido.

---

## 8. Investigação de `etapa_max_funil`

### 8.1. Inconsistência identificada

A coluna `etapa_max_funil` apresentou um registro com valor `7`, embora o dicionário do desafio defina seis etapas para o funil.

A definição oficial é:

| Etapa | Descrição           |
| ----: | ------------------- |
|     1 | Simulação           |
|     2 | Lead                |
|     3 | Análise de crédito  |
|     4 | Avaliação do imóvel |
|     5 | Formalização        |
|     6 | Contratação         |

Foi identificado apenas um registro com etapa 7, que foi investigado separadamente.

### 8.2. Registro investigado

| Campo                      | Valor observado |
| -------------------------- | --------------- |
| `id_proposta`              | `PR-000081`     |
| `etapa_max_funil`          | 7               |
| `status_final`             | `Contratada`    |
| `data_assinatura_contrato` | Preenchida      |
| `taxa_juros_aa`            | Preenchida      |

A combinação de status e campos preenchidos é compatível com uma proposta contratada. Entretanto, o valor 7 não corresponde a nenhuma etapa prevista na definição oficial do funil.

### 8.3. Correção realizada

O valor de `etapa_max_funil` foi corrigido de `7` para `6`, correspondente à etapa de Contratação.

O registro foi mantido na base, pois as informações disponíveis permitiram associá-lo à etapa final prevista no dicionário.

**Decisão:** tratar o caso como uma correção de qualidade dos dados, e não como motivo para excluir a proposta.

### 8.4. Distribuição das etapas após a correção

|     Etapa | Descrição           | Registros |
| --------: | ------------------- | --------: |
|         1 | Simulação           |       256 |
|         2 | Lead                |       909 |
|         3 | Análise de crédito  |     1.657 |
|         4 | Avaliação do imóvel |     1.151 |
|         5 | Formalização        |       764 |
|         6 | Contratação         |     1.128 |
| **Total** |                     | **5.865** |

A distribuição totaliza os 5.865 registros da base tratada e apresenta as seis etapas previstas no dicionário de dados.

---

## 9. Resumo estatístico e investigação de anomalias numéricas

### 9.1. Verificação — `check_numeric_summary()`

Foi realizada uma análise inicial das variáveis numéricas, incluindo a avaliação de mínimos, máximos e possíveis valores que merecessem investigação.

A análise estatística inicial serve para identificar pontos de atenção, mas não é suficiente, isoladamente, para determinar se um registro é inválido. A interpretação também depende das regras de negócio e das demais informações associadas à proposta.

### 9.2. Investigação de `idade_cliente`

O menor valor encontrado na coluna foi **14 anos**.

Foi identificada uma única proposta com essa idade:

| Campo                | Valor observado     |
| -------------------- | ------------------- |
| `id_proposta`        | `PR-000079`         |
| `idade_cliente`      | 14                  |
| `tipo_imovel`        | `Casa`              |
| `etapa_max_funil`    | 3                   |
| `status_final`       | `Reprovada crédito` |
| `tempo_analise_dias` | 41                  |

O valor pode ser inconsistente com o contexto do produto, mas os dados disponíveis não permitem afirmar que houve erro de preenchimento.

### 9.3. Decisão sobre o registro

A proposta foi mantida na base e documentada como uma possível anomalia de qualidade dos dados.

Não foi aplicada uma regra automática de exclusão, pois isso exigiria uma justificativa adicional ou uma regra de negócio explícita.

### 9.4. Demais variáveis numéricas

Na verificação inicial de mínimos e máximos, não foram identificadas outras anomalias evidentes que justificassem tratamento apenas com base nessa análise.

Essa conclusão se limita à exploração realizada. A ausência de anomalias evidentes nessa verificação não significa que todas as variáveis estejam necessariamente livres de problemas.

---

## 10. Cálculo e análise do LTV

### 10.1. Definição da variável

O dicionário de dados apresenta a variável `ltv`, mas ela não está disponível diretamente no CSV original.

O LTV foi derivado a partir das variáveis existentes:

\[
LTV = \frac{valor_solicitado}{valor_imovel}
\]

O desafio estabelece um limite interno de referência de **60%** para o LTV.

Esse limite foi utilizado para comparar grupos de propostas. Valores acima de 60% não foram considerados automaticamente erros de qualidade, pois representam uma condição relacionada à regra de negócio.

### 10.2. Análise inicial

Antes da conclusão de todos os tratamentos, foram identificados 6.397 registros com LTV calculável.

#### Resumo estatístico inicial

| Estatística                    |             Resultado |
| ------------------------------ | --------------------: |
| Média                          |                49,10% |
| Mediana                        |                49,23% |
| Mínimo                         |                23,00% |
| Máximo                         |                79,00% |
| Propostas com LTV acima de 60% |                   981 |
| Percentual acima de 60%        | Aproximadamente 15,3% |

Os três registros que inicialmente não permitiram o cálculo apresentavam o prefixo `R$` na coluna `valor_imovel`. Após a padronização monetária, passaram a permitir a conversão e o cálculo do indicador.

**Interpretação:** a análise inicial mostrou que a maior parte dos registros calculáveis apresentava LTV abaixo ou igual a 60%, embora existisse uma parcela de propostas acima desse limite.

Essa observação foi utilizada como ponto de partida para a comparação na base tratada.

### 10.3. Análise na base tratada

Após os tratamentos e a remoção das 535 propostas de terrenos, a base passou a conter 5.865 registros.

O LTV foi calculado novamente sobre essa base. Em seguida, as propostas foram separadas em duas faixas:

- LTV até 60%.
- LTV acima de 60%.

#### Resultados por faixa de LTV

| Faixa de LTV | Propostas | Contratadas | Taxa de conversão |
| ------------ | --------: | ----------: | ----------------: |
| Até 60%      |     4.961 |       1.019 |            20,54% |
| Acima de 60% |       904 |         109 |            12,06% |
| **Total**    | **5.865** |   **1.128** |        **19,23%** |

A taxa de conversão foi calculada dividindo o número de propostas contratadas pelo total de propostas de cada faixa.

### 10.4. Interpretação dos resultados

A taxa de conversão das propostas com LTV de até 60% foi de 20,54%, enquanto a das propostas acima desse limite foi de 12,06%.

A diferença entre as taxas foi de **8,48 pontos percentuais**.

Na base analisada, portanto, as propostas com LTV de até 60% apresentaram uma taxa de contratação superior à das propostas acima desse limite.

Esse resultado indica uma associação entre a faixa de LTV e a contratação, mas não demonstra que o LTV, isoladamente, determine o resultado. Outras características, como score de crédito, canal de origem e valores solicitados, também podem estar relacionadas à contratação.

### 10.5. Implicações para as análises de negócio

A comparação justificou manter o LTV como uma das variáveis relevantes para investigar diferenças entre propostas contratadas e não contratadas.

O limite de 60% foi utilizado como referência para segmentação e comparação, sem exclusão automática das propostas que ultrapassam esse valor.

Como aprofundamento, os resultados podem ser examinados em conjunto com outras variáveis, incluindo:

- `score_credito`;
- `canal_origem`;
- `status_final`;
- `valor_solicitado`.

Essa abordagem permite investigar se a diferença observada entre as faixas de LTV também aparece em outros segmentos da base.

---

## 11. Síntese das decisões de qualidade dos dados

A tabela a seguir consolida os principais problemas investigados e as decisões adotadas durante a preparação da base.

| Situação identificada                        | Quantidade ou registro                 | Decisão                                                        |
| -------------------------------------------- | -------------------------------------- | -------------------------------------------------------------- |
| Valores monetários com prefixo `R$`          | 3 registros                            | Remover o prefixo e converter para numérico                    |
| Datas com formato diferente do predominante  | 3 registros                            | Padronizar o formato                                           |
| Valores ausentes em campos de contratação    | 5.159 em cada coluna                   | Manter por representarem propostas sem esses dados preenchidos |
| IDs de proposta duplicados                   | Nenhum identificado                    | Nenhuma ação necessária                                        |
| Linhas completamente duplicadas              | Nenhuma identificada                   | Nenhuma ação necessária                                        |
| Variações de capitalização em `canal_origem` | Categorias identificadas na exploração | Padronizar as representações                                   |
| Propostas classificadas como `Terreno`       | 535 registros                          | Remover conforme instrução do desafio                          |
| Etapa de funil inválida                      | `PR-000081`                            | Corrigir a etapa 7 para 6                                      |
| Idade declarada de 14 anos                   | `PR-000079`                            | Manter e documentar para investigação, sem exclusão automática |

As decisões foram tomadas considerando as evidências observadas, as regras explícitas do desafio e o significado das informações no processo de crédito.

---

Etapa de RPA e geração do relatório em PDF

2.1. Objetivo

Esta etapa faz parte do fluxo destinado à geração de um relatório em PDF a partir do conteúdo e dos resultados da análise.

O arquivo de saída previsto no projeto é:

outputs/relatorio_analise.pdf

2.2. Organização do projeto

Os módulos relacionados ao fluxo principal e à geração do relatório incluem:

src/app.py;

src/main.py;

src/reports/pdf_report.py.

O módulo pdf_report.py está relacionado à geração do documento, enquanto os arquivos de entrada da aplicação organizam a execução do fluxo.

A descrição exata das responsabilidades de cada função deve acompanhar a implementação existente no código.

2.3. Registro da execução

O relatório em PDF representa uma saída distinta da base de propostas e do arquivo JSON dos laudos.

Nesta etapa, o documento é produzido a partir do conteúdo da análise. Não se deve confundir essa geração de PDF com a extração estruturada dos campos dos arquivos TXT dos laudos

3. Extração de dados dos laudos de avaliação imobiliária

3.1. Objetivo

Esta funcionalidade tem como objetivo extrair informações estruturadas dos arquivos TXT dos laudos de avaliação imobiliária e consolidá-las em um arquivo JSON.

O processo foi desenvolvido separadamente do fluxo de geração do relatório em PDF.

A entrada é composta por 17 arquivos TXT de laudos de avaliação.

3.2. Organização dos módulos

Os principais módulos envolvidos são:

src/extraction/reader.py: leitura dos arquivos de origem;

src/services/field_extractor.py: extração dos campos de interesse;

src/services/normalizer_data.py: normalização e validação dos valores extraídos;

src/extraction/json_writer.py: gravação dos dados estruturados em JSON;

src/main_extract.py: ponto de entrada associado a esse fluxo.

3.3. Fluxo de processamento

O processamento pode ser entendido em quatro etapas:

Leitura: acesso ao conteúdo dos arquivos TXT.

Extração: identificação dos campos relevantes no texto, utilizando as regras implementadas no extrator.

Normalização: tratamento de inconsistências de formato e normalização de datas e valores numéricos.

Exportação: gravação dos dados estruturados em JSON.

A separação dessas responsabilidades facilita a manutenção do projeto e permite identificar em qual etapa uma eventual inconsistência ocorreu.

3.4. Arquivo de saída

O arquivo produzido por esse fluxo é:

outputs/laudos_extraidos.json

O JSON permite armazenar os dados extraídos em uma estrutura organizada, facilitando seu consumo por outras partes do sistema.
