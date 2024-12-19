# Pipeline - Anotação de Variantes (Versão de Testes)

Script de testes e validação de código para um pipeline de bioinformática que anota variantes genômicas a partir de VCF.

## Estrutura do Projeto

- **pipeline/**  
  - `Snakefile`  
  - `config.yaml`  
  - **scripts/**  
    - `annotate_variants.py`  
  - **envs/**  
    - `pipeline_env.yaml`  

- **api/**  
  - `app.py`  
  - `requirements.txt`  
  - **data/**  

- **web/**  
  - `app.py`  
  - **templates/**  
    - `index.html`  
  - **static/**  
    - `style.css`  
  - `requirements.txt`  

- **data/**  
  - `input_variants.vcf`  

- **results/**  
  - `variants_annotated.tsv`  

- `Dockerfile`  
- `README.md`  

### Descrição dos Diretórios e Arquivos

- pipeline/: Contém o pipeline Snakemake para processar o arquivo VCF e anotar variantes.

  - Snakefile: Define as regras do pipeline.
  - config.yaml: Configurações do pipeline, incluindo caminho para o arquivo VCF de entrada.
  - scripts/: Scripts auxiliares para processar o VCF e consultar a API MyVariant.info.
    - annotate_variants.py: Realiza as consultas à API e anota as variantes.
  - envs/pipeline_env.yaml: Define o ambiente Conda usado pelo pipeline.

- api/: Implementação da API Flask.

  - app.py: O código principal da API.
  - requirements.txt: Dependências da API.
  - data/: Armazena arquivos gerados pela API, como variantes anotadas.

- web/: Implementação da interface web Flask.

  - app.py: O código principal da interface web.
  - templates/index.html: O arquivo HTML principal.
  - static/style.css: Estilo CSS para a interface.
  - requirements.txt: Dependências da interface web.

- data/: Pasta para arquivos de entrada, como o arquivo VCF (input_variants.vcf).

- results/: Pasta para resultados gerados pelo pipeline (variants_annotated.tsv).

- Dockerfile: Arquivo para construir o contêiner Docker.

- README.md: Este arquivo com as instruções do projeto.

## Como Configurar e Executar o Projeto

### Pré-requisitos

- Git: Para clonar o repositório.
- Conda/Miniconda: Para gerenciar o ambiente do pipeline.
- Python 3.9 ou superior.
- Docker (opcional): Para execução via contêiner.

### Passos para Configurar

1. Clone o Repositório:

   bash
   git clone https://github.com/seu-usuario/pipeline-code-validator.git
   cd bioinfo-pipeline
   

2. Crie e Ative o Ambiente Conda:

   bash
   conda env create -f pipeline/envs/pipeline_env.yaml
   conda activate bioinfo_pipeline
   

3. Execute o Pipeline:

   bash
   cd pipeline
   snakemake --use-conda --cores 4
   

   Isso processará o arquivo data/input_variants.vcf e gerará results/variants_annotated.tsv.

4. Inicie a API:

   bash
   cd ../api
   pip install -r requirements.txt
   python app.py
   

   A API estará disponível em http://localhost:5000/variants.

5. Inicie a Interface Web:

   bash
   cd ../web
   pip install -r requirements.txt
   python app.py
   

   A interface web estará disponível em http://localhost:8080/.

### Usando Docker (Opcional)

1. Construa a Imagem Docker:

   bash
   docker build -t bioinfo-pipeline:latest .
   

2. Execute o Contêiner:

   bash
   docker run -p 5000:5000 -p 8080:8080 bioinfo-pipeline:latest
   

3. Acesse a Aplicação:

   - API: http://localhost:5000/variants
   - Interface Web: http://localhost:8080/

## Interface Web

1. Abra http://localhost:8080/ no navegador.
2. Insira os valores desejados nos filtros (AF, DP, QUAL).
3. Clique em "Filtrar" para atualizar os resultados na tabela.
4. Campos exibidos:
   - CHROM, POS, REF, ALT: Identificadores da variante.
   - QUAL, FILTER, DP: Qualidade e profundidade.
   - GENE, RSID: Informações anotadas.
   - GNOMAD_AF: Frequência alélica no banco gnomAD.

## Exemplos de Uso da API

- Obter todas as variantes:

  bash
  curl http://localhost:5000/variants
  

- Filtrar por frequência alélica e profundidade:

  bash
  curl "http://localhost:5000/variants?min_af=0.01&max_af=0.05&min_dp=10"
  

## Contribuindo

- Sugestões de melhorias são bem-vindas!
- Abra uma issue ou envie um pull request no repositório GitHub.

