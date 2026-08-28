# Decisões Arquiteturais - API REST Seleção de Pools

## 1. Objetivo
Criar uma API REST em Python capaz de retornar, a qualquer momento, o melhor pool de instâncias para execução de Spark jobs, minimizando falhas por indisponibilidade de instâncias spot.

---

## 2. Linguagem e Framework
- **Linguagem:** Python (>3.9)
- **Framework escolhido:** FastAPI
  - Justificativa: moderno, rápido, suporte nativo a OpenAPI/Swagger, fácil de escalar e documentar.
  - Alternativa considerada: Flask (mais simples, mas exigiria configuração manual da documentação).

---

## 3. Estrutura da API
- Endpoint principal: `/get-pool`
- Parâmetros:
  - `instance_type` (opcional): restringe retorno a tipos específicos de instância (ex.: `r6.xlarge`, `c6.xlarge`).
- Resposta:
  ```json
  {
    "best_pool": "pool-r6.xlarge-us-east-1c"
  }
  ```

---

## 4. Dados
- **Fonte:** arquivos JSON em S3 (um evento por linha).
- **Desenvolvimento local:** leitura de arquivo `jobs.json` simulando dados do S3.
- **Estrutura dos eventos:**
  - `finished_at`: timestamp UTC
  - `job_id`: identificador do job
  - `pool_id`: identificador do pool (formato `pool-<instance-type>-<az>`)
  - `status`: `SUCCESS` ou `FAILED`
  - `reason`: motivo da falha (`SPOT_INSTANCE_TERMINATION`, `TIMED_OUT`, `SPARK_EXECUTION_ERROR`)

---

## 5. Lógica de Seleção
- Agrupar eventos por `pool_id`.
- **Calcular métricas:**
  - Sucessos vs falhas.
  - Taxa de falha por `SPOT_INSTANCE_TERMINATION`.
- Selecionar o pool com maior proporção de sucessos (menor taxa de falha).

---

## 6. Escalabilidade e Deploy
- **Docker:** ambiente isolado, um único comando para subir (`docker-compose up`).
- **CI/CD:** GitHub Actions para rodar testes (caso falhar não faz deploy), valida cobertura de testes >90% e build automático.
- **Alta disponibilidade:** arquitetura preparada para rodar em Kubernetes/ECS se necessário.

---

## 7. Documentação
- **README.md:** instruções de uso, decisões arquiteturais, como rodar localmente.
- **Swagger/OpenAPI:** gerado automaticamente pelo FastAPI.
- **Testes unitários:** pytest para validar lógica de seleção.

---

## 8. Cronograma (3 dias)
- **Dia 1:** Estrutura mínima da API + endpoint `/get-pool`.
- **Dia 2:** Filtros, Dockerfile, README inicial, testes básicos.
- **Dia 3:** Documentação final, CI/CD, revisão e entrega no GitHub/GitLab.