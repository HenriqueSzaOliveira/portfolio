# Testes e Cobertura

Este diretório reúne os testes automatizados da API de seleção de pools.
Cobertura aceitável >95%

## 1) Pré-requisitos

Execute os comandos a partir da raiz do repositório

Instale as dependências do projeto e dos testes:

```bash
python -m pip install -r portfolio/APIRestSelectPoolsInstances/infra/requirements.txt
python -m pip install -r portfolio/APIRestSelectPoolsInstances/tests/requirements.txt
```

> Se você estiver no Windows, pode usar o PowerShell ou o Prompt de Comando com os mesmos comandos.

## 2) Executar os testes

### Todos os testes

```bash
python -m pytest portfolio/APIRestSelectPoolsInstances/tests -q
```

### Testes com saída detalhada

```bash
python -m pytest portfolio/APIRestSelectPoolsInstances/tests
```

### Executar um arquivo específico

```bash
python -m pytest portfolio/APIRestSelectPoolsInstances/tests/test_api.py -q
python -m pytest portfolio/APIRestSelectPoolsInstances/tests/test_data_loader.py -q
python -m pytest portfolio/APIRestSelectPoolsInstances/tests/test_pool_selector.py -q
```

## 3) Verificar cobertura de testes

### Cobertura no terminal

```bash
python -m pytest portfolio/APIRestSelectPoolsInstances/tests --cov=portfolio.APIRestSelectPoolsInstances.src --cov-report=term-missing
```

Esse comando mostra:
- a porcentagem de cobertura por arquivo;
- quais linhas não foram cobertas;
- o total geral da suíte.

### Cobertura em HTML

```bash
python -m pytest portfolio/APIRestSelectPoolsInstances/tests --cov=portfolio.APIRestSelectPoolsInstances.src --cov-report=html
```

Depois, abra o relatório gerado na raiz do repositório:

```text
htmlcov/index.html
```

> Importante: quando o comando é executado a partir da raiz do projeto, o relatório HTML é criado em `htmlcov/` no diretório raiz do repositório, e não dentro de `portfolio/APIRestSelectPoolsInstances/tests`.

No navegador, a página exibirá a cobertura por arquivo e por módulo.

## 4) Fluxo rápido

Se quiser rodar tudo em um passo só, a partir da raiz do repositório:

```bash
python -m pip install -r portfolio/APIRestSelectPoolsInstances/infra/requirements.txt
python -m pip install -r portfolio/APIRestSelectPoolsInstances/tests/requirements.txt
python -m pytest portfolio/APIRestSelectPoolsInstances/tests --cov=portfolio.APIRestSelectPoolsInstances.src --cov-report=term-missing
```

## 5) Dicas

- Use `-q` para reduzir a saída do pytest.
- Use `-k "nome_do_teste"` para executar apenas testes específicos.
- Use `--cov` para medir a qualidade da suíte e identificar trechos sem cobertura.

Exemplo:

```bash
python -m pytest portfolio/APIRestSelectPoolsInstances/tests -k pool -q --cov=portfolio.APIRestSelectPoolsInstances.src --cov-report=term-missing
```
