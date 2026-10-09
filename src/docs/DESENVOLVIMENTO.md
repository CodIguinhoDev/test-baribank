# Desenvolvimento

## 1. Desenvolvimento da análise de propostas de crédito

### 1.1. Organização e estruturação do projeto

Iniciei o desenvolvimento organizando o projeto em módulos com responsabilidades separadas. A intenção foi manter o código organizado, facilitar a manutenção e permitir que cada parte da aplicação fosse desenvolvida de maneira independente.

Os principais módulos dessa etapa foram:

- `data_loader.py`: carregamento do arquivo CSV.
- `data_exploration.py`: exploração e verificação da qualidade dos dados.
- `treatment.py`: tratamento e padronização da base.
- `funnel_analysis.py`: análise do funil de propostas.
- `ltv.py`: cálculo e análise do LTV.
- `weekly_analysis.py`: análise semanal das propostas.
- `pdf_report.py`: geração do relatório em PDF.
- `config.py`: centralização de configurações e constantes do projeto.

Essa organização ajudou a separar o carregamento, a exploração, o tratamento e a análise dos dados, evitando concentrar todas as responsabilidades em um único arquivo.

### 1.2. Exploração e preparação da base

Depois de estruturar os módulos, comecei a investigar a base de propostas de crédito para compreender sua organização e identificar possíveis problemas antes de realizar as análises de negócio.

Durante essa etapa, examinei os tipos das colunas, os valores ausentes, as duplicidades, as categorias textuais e possíveis inconsistências nos registros.

A exploração mostrou que algumas informações precisavam ser padronizadas antes de serem utilizadas nos cálculos. Também foi necessário diferenciar problemas reais de qualidade dos dados de situações que poderiam representar regras ou características do próprio processo de crédito.

Com base nessa investigação, implementei os tratamentos necessários e documentei as decisões tomadas.

Os detalhes das verificações, os registros específicos identificados, os valores originais e as justificativas de cada tratamento estão documentados no arquivo **Anotações**.

### 1.3. Tratamento e validação dos dados

Durante a preparação da base, realizei os seguintes tratamentos:

- Conversão de valores monetários para tipos numéricos.
- Padronização de datas registradas em formatos diferentes.
- Uniformização das categorias textuais do canal de origem.
- Manutenção de valores ausentes relacionados a propostas que não chegaram à contratação.
- Correção de um registro com etapa de funil fora da definição oficial.
- Remoção dos registros classificados como `Terreno`, conforme a orientação do desafio.
- Investigação de uma proposta com idade declarada de 14 anos, mantida por não haver evidências suficientes para confirmar um erro.

Uma decisão importante foi não excluir automaticamente todos os valores considerados incomuns. Procurei avaliar o contexto de cada situação antes de alterar ou remover registros, evitando descartar informações sem justificativa suficiente.

Após a remoção dos terrenos, a base utilizada nas análises passou de 6.400 para 5.865 registros.

### 1.4. Cálculo e análise do LTV

Com a base preparada, implementei o cálculo do LTV (_Loan-to-Value_), pois essa variável não estava presente diretamente no arquivo CSV original.

O cálculo foi realizado a partir do valor solicitado e do valor do imóvel. Também defini o limite de referência de 60% em `config.py`, centralizando essa configuração para facilitar sua manutenção.

Em seguida, comparei as propostas com LTV de até 60% às propostas acima desse limite, observando a quantidade de propostas e a taxa de contratação de cada grupo.

Na base tratada, a taxa de conversão foi de 20,54% para propostas com LTV de até 60% e de 12,06% para propostas acima de 60%.

Essa comparação permitiu identificar uma associação entre a faixa de LTV e o resultado das propostas. No entanto, considerei que essa diferença, isoladamente, não comprova que o LTV determine a contratação, pois outros fatores também podem influenciar o resultado.

Os cálculos completos, as tabelas e a interpretação detalhada dos indicadores estão registrados no arquivo Anotações.

### 1.5. Análises e geração do relatório

Após a preparação dos dados e a implementação das análises, avancei para a organização dos resultados do projeto.

A estrutura contempla módulos específicos para a análise do funil, o cálculo do LTV e a análise semanal das propostas, além do módulo responsável pela geração do relatório em PDF.

O relatório produzido foi salvo em:

`outputs/relatorio_analise.pdf`

Essa etapa reuniu os resultados da análise em um arquivo que pode ser consultado separadamente do código-fonte.

## 2. Extração de dados dos laudos de avaliação

### 2.1. Implementação do processo de extração

Além da análise das propostas de crédito, desenvolvi um processo separado para extrair informações dos arquivos de texto dos laudos de avaliação imobiliária fornecidos no desafio.

Organizei essa funcionalidade em módulos com responsabilidades distintas:

- `reader.py`: leitura dos arquivos de entrada.
- `field_extractor.py`: identificação e extração dos campos utilizando expressões regulares (_regex_).
- `normalizer_data.py`: normalização e validação de datas e valores numéricos.
- `json_writer.py`: gravação dos dados extraídos em um arquivo JSON.

A implementação foi dividida em etapas para separar a leitura dos documentos, a identificação das informações, o tratamento dos valores encontrados e a geração do resultado final.

### 2.2. Normalização e organização dos resultados

Durante o desenvolvimento, trabalhei na identificação dos campos presentes nos textos e na padronização de suas representações.

O uso de expressões regulares permitiu estruturar a extração de informações a partir de documentos textuais. Depois da extração, os dados passaram pelo processo de normalização e validação antes de serem gravados.

Essa separação de responsabilidades tornou o processo mais organizado e facilitou a identificação do módulo responsável por cada operação.

### 2.3. Resultado da extração

Os dados extraídos foram organizados no arquivo:

`outputs/laudos_extraidos.json`

Esse resultado corresponde ao processo de extração dos laudos e é independente da geração do relatório em PDF da análise de propostas.

## 3. Tentativa de análise de textos com inteligência artificial

### 3.1. Objetivo da implementação

Também iniciei uma etapa voltada à análise de textos utilizando inteligência artificial por meio de uma integração com API.

Para organizar essa funcionalidade, criei o módulo `main_extract.py` como ponto de entrada da execução.

### 3.2. Dificuldade encontrada

Durante a tentativa de execução, encontrei o erro de autenticação:

`401 UNAUTHENTICATED ACCESS_TOKEN_TYPE_UNSUPPORTED`

O erro impediu que a integração fosse executada e validada com sucesso.

Como não consegui concluir essa etapa, não considerei a análise por inteligência artificial como uma funcionalidade plenamente operacional. O processo permaneceu incompleto, e a integração ainda precisa ser corrigida e testada para que seus resultados possam ser avaliados.

## 4. Aprendizados e considerações finais

O desenvolvimento do desafio envolveu diferentes atividades, desde a organização do código e a exploração de dados até a implementação de análises, a extração de informações de documentos e a tentativa de integração com uma API.

Durante o processo, precisei investigar inconsistências, definir critérios de tratamento e tomar decisões sobre a manutenção ou correção de registros. Também trabalhei na separação das responsabilidades dos módulos, buscando manter uma estrutura que facilitasse a compreensão e a manutenção do projeto.

Outro aprendizado foi a importância de distinguir as etapas concluídas daquelas que ainda precisam de ajustes. Embora a análise das propostas e a extração dos dados dos laudos tenham produzido arquivos de saída, a integração de inteligência artificial não foi concluída devido ao problema de autenticação.

Ao final, o projeto reuniu diferentes abordagens de processamento e análise de dados, além de evidenciar pontos que ainda podem ser aprimorados. A documentação técnica complementar, presente no arquivo Anotações, registra com maior profundidade as verificações, os resultados numéricos e as decisões tomadas durante a preparação e a análise da base.
