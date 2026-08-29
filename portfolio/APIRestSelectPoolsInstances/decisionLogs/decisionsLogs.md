# Decisões Arquiteturais - API REST Seleção de Pools

## 1. Objetivo
Criar uma API REST em Python capaz de retornar, a qualquer momento, o melhor pool de instâncias para execução de Spark jobs, minimizando falhas por indisponibilidade de instâncias spot e otimizando a resiliência operacional.

---

## 2. Stack tecnológica
**Linguagem:** Python 3.11+

**Framework:** FastAPI
Justificativa: produtividade, documentação automática com OpenAPI/Swagger, validação de schemas, e baixo custo de manutenção.

**Testes:** pytest
Justificativa: excelente integração com FastAPI e fácil automação em CI.

**Cobertura:** pytest-cov
Estratégia: manter cobertura mínima de 95% para bloquear regressões.

**Containerização:** Docker
Justificativa: empacotar a aplicação para execução consistente em qualquer ambiente.


---

## 3. Estrutura do projeto
A API foi organizada em uma estrutura modular, com foco em separação de responsabilidades:

`src/api.py`: endpoints HTTP da API e lógica de exposição.

`src/utils/data_loader.py`: carregamento e parsing dos arquivos de eventos.

`src/utils/pool_selector.py`: algoritmo de escolha do melhor pool.

`tests/`: suíte automatizada para validar endpoints e regras de negócio.

`infra/Dockerfile`: imagem Docker da aplicação.

`.github/workflows/`: automação de CI/CD no GitHub Actions.

> Observação importante: embora o projeto da API viva em `portfolio/APIRestSelectPoolsInstances`, o GitHub Actions precisa ficar em `.github/workflows` na raiz do repositório para ser reconhecido automaticamente.

---

## 4. API e interface
Endpoint principal: `/get-pool`

Parâmetros opcionais:
  - `instance_type`: filtra o tipo de instância (ex.: `r6.xlarge`)
  - `az`: filtra zona de disponibilidade (ex.: `us-east-1c`)

Resposta esperada:

```json
{
  "best_pool": "pool-r6.xlarge-us-east-1c"
}
```

A API também expõe documentação interativa via Swagger (`/docs`).

---

## 5. Fonte de dados e modelo de eventos

**Origem dos dados:** arquivos JSON em um bucket de logs, simulando eventos de execução de Spark jobs.


**Estrutura de cada evento:**
  - `finished_at`: timestamp UTC
  - `job_id`: identificador do job
  - `pool_id`: identificador do pool (formato `pool-<instance-type>-<az>`)
  - `status`: `SUCCESS` ou `FAILED`
  - `reason`: motivo da falha (`SPOT_INSTANCE_TERMINATION`, `TIMED_OUT`, `SPARK_EXECUTION_ERROR`)

A lógica interpreta esses eventos para avaliar risco e confiabilidade por pool.

---

## 6. Lógica de seleção de pools
A estratégia decidiu priorizar uma análise por pool, calculando:

Volume total de execuções por `pool_id`

Proporção de `SUCCESS` vs `FAILED`

Taxa de falha por `SPOT_INSTANCE_TERMINATION`

Comparação entre pools para selecionar o melhor candidato

A decisão final favorece o pool com melhor equilíbrio entre disponibilidade e menor risco de interrupção por spot termination.

---

## 7. CI/CD e automação
A automação foi organizada em dois workflows no GitHub Actions:

### 7.1 CI
- roda em push e pull_request
- instala dependências
- executa a suíte de testes
- valida cobertura mínima de 95%
- falha caso algum teste quebre

### 7.2 CD
- dispara na branch `main`
- executa os testes e a cobertura novamente
- faz build da imagem Docker
- realiza login no Docker Hub
- publica a imagem com tags `latest` e `sha`

Isso garante um pipeline mais seguro e reprodutível para entrega da solução.

---

## 8. Publicação e entrega
O projeto foi preparado para ser publicado como um container Docker.

O processo de entrega usa Docker Hub para armazenar a imagem final.

A imagem é exposta de forma simples para deploy em ambientes locais, de teste ou em infraestrutura externa.

