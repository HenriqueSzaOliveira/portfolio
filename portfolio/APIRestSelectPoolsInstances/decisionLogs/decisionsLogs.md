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

**Justificativa para não usar banco de dados:**
Neste cenário, os dados são consumidos em formato de log de eventos fixo que nao muda a estrutura. A API não precisa fazer inserções, mas sim responder rapidamente a consultas sobre o histórico recente paseado em logs. Em vez de persistir tudo em um banco relacional ou NoSQL, a solução foi pensada para ler os arquivos em lote do bucket, transformar em DataFrame e aplicar a lógica de decisão em memória. Isso reduz custo operacional, evita sobrecarga de infraestrutura e mantém a implementação mais simples e previsível.

Além disso, para um volume de milhares de requisições por minuto, uma abordagem com banco de dados exigiria esquema, índices, manutenção de consistência, limites de escrita/consulta e maior custo de operação. Como a decisão do melhor pool depende de agregações por `pool_id` sobre um conjunto de eventos, a leitura em lote combinada com cache em memória é suficiente para atender a demanda com baixa latência e alta simplicidade (até 5500 requisições por segundo que élimite s3 aws). Mas pode evoluir para um armazenamento mais estruturado apenas se houver necessidade real de consulta histórica em escala muito maior ou de latência de leitura crítica.

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

**Sobre Escalonamento** a imagem publicada no Docker Hub pode servir como base para deploy em um ambiente orquestrado, como Kubernetes, ECS, EC2 ou uma infraestrutura com balanceamento de carga. A ideia seria manter a API stateless, rodando múltiplas réplicas da mesma imagem atrás de um load balancer, permitindo aumentar o número de instâncias conforme o volume de requisições crescer. Com o cache em memória e o processamento em lote de eventos, esse modelo é simples, barato e escala bem até uma certa capacidade. Se a demanda aumentar de forma consistente, as próximas etapas seriam otimizar a leitura dos logs, adicionar cache distribuído em redis por exemplo e eventualmente migrar parte do histórico para um armazenamento caso a leitura de arquivos se torne um problema.

---

## 8. Publicação e entrega
O projeto foi preparado para ser publicado como um container Docker.

O processo de entrega usa Docker Hub para armazenar a imagem final.

A imagem é exposta de forma simples para deploy em ambientes locais, de teste ou em infraestrutura externa.

