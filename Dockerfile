# Etapa base: Usar uma imagem mínima com Python
FROM python:3.9-slim

# Atualizar o sistema e instalar dependências básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    libbz2-dev \
    zlib1g-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Criar um diretório para o aplicativo
WORKDIR /app

# Copiar o conteúdo do projeto para o contêiner
COPY . .

# Instalar o Miniconda para gerenciar o ambiente do Snakemake
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh && \
    /opt/miniconda/bin/conda init

# Adicionar o Miniconda ao PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Criar o ambiente Conda para o pipeline
RUN conda env create -f pipeline/envs/pipeline_env.yaml && \
    conda clean -a

# Instalar dependências da API e Web
RUN pip install -r api/requirements.txt && \
    pip install -r web/requirements.txt

# Definir portas expostas
EXPOSE 5000 8080

# Script para iniciar o pipeline, API e Web
CMD ["bash", "-c", "snakemake --use-conda --cores 4 && cd api && python app.py & cd ../web && python app.py"]
