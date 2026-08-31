# Portfólio

Repositório com projetos práticos de engenharia de dados e desenvolvimento de APIs em Python.

## Links minhas redes
- https://medium.com/@henrique.sza.oliveira
- https://www.linkedin.com/in/henriquecomputerscience/

## Projetos

### API REST: seleção de pools de instâncias

A [API REST de seleção de pools](portfolio/APIRestSelectPoolsInstances/README.md) usa FastAPI para escolher o melhor pool de instâncias Spark com base em logs de jobs, falhas de spot instances, tipo de instância e zona de disponibilidade (AZ).

Principais recursos:

- Endpoint `GET /get-pool`.
- Filtros opcionais por tipo de instância e AZ.
- Leitura de logs JSON.
- Cache de resultados por cinco segundos.
- Execução local ou via Docker.
- Testes automatizados.

### Databricks

O [projeto Databricks](portfolio/Databricks/README.md) reúne dados sintéticos e um notebook para estudos de ingestão e exploração com Apache Spark.

Inclui:

- Dataset JSON Lines com vendas fictícias de livros.
- Dataset CSV com endereços brasileiros fictícios.
- Script Python para geração dos dados.
- Notebook para testes e análises no Databricks.

## Estrutura

```text
portfolio/
├── portfolio/
│   ├── APIRestSelectPoolsInstances/
│   │   ├── bucket/              # Logs simulados de jobs Spark
│   │   ├── decisionLogs/        # Registros de decisões do projeto
│   │   ├── infra/               # Dependências e configuração Docker
│   │   ├── src/                 # Implementação da API
│   │   └── tests/               # Testes automatizados
│   └── Databricks/
│       ├── files/               # Datasets de exemplo
│       └── SandBox/              # Scripts e notebook de exploração
└── README.md
```

## Tecnologias

- Python
- FastAPI
- Apache Spark / Databricks
- Docker
- Pytest

## Como explorar

Cada projeto possui seu próprio README com requisitos, instruções de execução e exemplos de uso:

- [APIRestSelectPoolsInstances](portfolio/APIRestSelectPoolsInstances/README.md)
- [Databricks](portfolio/Databricks/README.md)
