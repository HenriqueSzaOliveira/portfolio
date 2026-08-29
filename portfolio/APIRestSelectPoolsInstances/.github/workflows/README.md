# GitHub Actions - CI do projeto API Pools

Este diretório contém o workflow de integração contínua para a API de seleção de pools.

Mova a pasta .github para a raiz do repositório para funcionar o actions

## O que o workflow faz

O arquivo principal do workflow é `ci.yml` e ele executa as seguintes validações:

- dispara em push em branches diferentes de `main`
- dispara em pull requests para `main`
- também pode ser executado manualmente via `workflow_dispatch`
- entra na pasta do projeto [portfolio/APIRestSelectPoolsInstances](../../portfolio/APIRestSelectPoolsInstances)
- instala as dependências do projeto e dos testes
- roda a suíte de testes com `pytest`
- exige cobertura mínima de `95%`
- falha automaticamente se algum teste quebrar ou se a cobertura cair abaixo do limite
- tenta criar um PR para `main` quando a branch de origem passar no CI

## Caminho do projeto usado pela pipeline

O workflow foi configurado para considerar a pasta abaixo como raiz de execução:

- [portfolio/APIRestSelectPoolsInstances](../../portfolio/APIRestSelectPoolsInstances)

Isso significa que, embora o workflow esteja em `.github/workflows`, a lógica de execução do projeto acontece dentro dessa pasta.

## Importante

O arquivo do workflow precisa ficar na raiz do repositório em:

- `.github/workflows/ci.yml`

Se ele for movido para dentro da pasta do projeto, o GitHub Actions não o reconhece automaticamente.

## Comandos executados pela pipeline

O workflow roda algo equivalente a:

```bash
cd portfolio/APIRestSelectPoolsInstances
python -m pip install -r infra/requirements.txt
python -m pip install -r tests/requirements.txt
python -m pytest tests --cov=portfolio.APIRestSelectPoolsInstances.src --cov-fail-under=95 --cov-report=term-missing
```

## Observação

Esse workflow é leve e compatível com o uso gratuito do GitHub Actions em projetos pequenos. A etapa de criação de PR depende das permissões do token e da configuração do repositório.
