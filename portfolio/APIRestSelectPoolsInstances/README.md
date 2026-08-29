# API REST - Seleção de Pools de Instâncias

Este projeto implementa uma API REST em Python/FastAPI para selecionar o melhor pool de instâncias Spark, considerando falhas de spot instances e filtros por tipo de instância e zona de disponibilidade (AZ).

imagine que um serviço externo coloca em um bucket arquivos json com as informações:
```json
{
    "finished_at": "2024-08-07T00:04:52.767830",
    "job_id": "my-job",
    "pool_id": "pool-r6.xlarge-us-east-1c",
    "status": "FAILED",
    "reason": "SPOT_INSTANCE_TERMINATION"
}
```

Em que:
- **finished_at** : momento em que o Spark job foi finalizado (timestamp em UTC,
formato ISO)
- **job_id** : nome do Spark job, geralmente escolhido pelo dono do job (string)
- **pool_id** : ID dos pools de instância, no formato ex. pool-<instance-type>-<az> (pool-i3.xlarge-us-east-1a ) (string)
- **status** : estado final do job, se finalizou com sucesso ou falha (string)
- **reason** : motivo da falha, que pode ser SPOT_INSTANCE_TERMINATION , TIMED_OUT ou SPARK_EXECUTION_ERROR (string)

---

# 🚀 Rodando sem Docker

### Pré-requisitos
- Python 3.11+
- Pip

### Instalação
```bash
pip install -r infra/requirements.txt
```

### Executando
Lembre-se de estar na pasta cd portfolio/APIRestSelectPoolsInstances/

```bash
uvicorn src.api:app --reload --port 5050
```

### Testando
#### Sem filtros:

```Code
http://localhost:5050/get-pool
```

#### Com filtros:

```Code
http://localhost:5050/get-pool?instance_type=r6.xlarge&az=us-east-1c
```

### executando em uma linha
```bash
pip install -r infra/requirements.txt & uvicorn src.api:app --reload --port 5050
```

---

# 🐳 Rodando com Docker

## 🛠️ Pré-req: Instalando Docker

### Windows

1. Baixe o Docker Desktop: https://www.docker.com/products/docker-desktop (docker.com in Bing)
2. Instale e reinicie o computador.
3. Verifique instalação:
    ```bash
    docker --version
    ```

OBS: instale WSL via powershell (wsl --install)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
docker --version
```

### macOS

1. Baixe o Docker Desktop: https://www.docker.com/products/docker-desktop (docker.com in Bing)
2. Instale e abra o Docker Desktop.
3. Verifique instalação:
    ```bash
    docker --version
    ```

## Executando API

Lembre-se de estar na pasta cd portfolio/APIRestSelectPoolsInstances/

1. Build da imagem
```bash
docker build -t api-pools -f infra/Dockerfile .
```

2. Executando o container
```bash
docker run -p 5050:5050 api-pools
```

3. Testando
    **Sem filtros:**
    ```Code
    http://localhost:5050/get-pool
    ```
    **Com filtros:**
    ```Code
    http://localhost:5050/get-pool?instance_type=r6.xlarge&az=us-east-1c
    ```
4. Em um comando
    ```bash
    docker build -t api-pools -f infra/Dockerfile . & docker run -p 5050:5050 api-pools
    ```

---

## 📚 Documentação da API

A API expõe automaticamente documentação interativa via **Swagger UI** e **ReDoc**.

### 🔎 Como acessar durante execução

- **Swagger UI (HTML dinâmico interativo)**  

```bash
http://localhost:5050/docs
```

### 📂 Exportando para arquivo

Você pode salvar a especificação para uso em Postman, Insomnia ou CI/CD:

```bash
# JSON
curl http://localhost:5050/openapi.json -o openapi.json
```

---

## 📚 Estrutura do Projeto
```Code
APIRestSelectPoolsInstances/
├── bucket/              # Logs JSON simulando jobs Spark
├── decisionLogs/        # Documentação de decisões
├── infra/               # Dockerfile e requirements.txt
├── src/                 # Código da API
│   ├── api.py
│   └── utils/
│       ├── data_loader.py
│       └── pool_selector.py
└── tests/               # Testes unitários
```

---
# Testes e CI/CD

Veja o readme das correspondentes pastas

**CI/CD**:  .github/workflows/README.md
**Testes**: tests/README.md