# Projeto Databricks

Projeto de estudo para geração e exploração de dados no Databricks usando arquivos JSON Lines e CSV.

## Objetivos

- Gerar uma base sintética de vendas de livros.
- Gerar uma base sintética de endereços brasileiros.
- Disponibilizar arquivos para leitura, transformação e análise em notebooks Databricks.

## Estrutura

```text
Databricks/
├── files/
│   ├── enderecos.csv
│   └── livros.json
└── SandBox/
    ├── gerar_datasets.py
    └── Tests.ipynb
```

## Dados disponíveis

### `files/livros.json`

Arquivo no formato JSON Lines com 500 registros de vendas. Cada registro contém:

- `id`
- `titulo`
- `autor`
- `genero`
- `preco`
- `quantidade`
- `data_venda`
- `endereco`

O campo `endereco` é um objeto aninhado com rua, número, bairro, cidade, estado e CEP.

### `files/enderecos.csv`

Arquivo CSV com 1.000 endereços brasileiros e as colunas `id`, `rua`, `numero`, `bairro`, `cidade`, `estado` e `cep`.

Os dados são fictícios e servem exclusivamente para estudos e testes.

## Requisitos

- Python 3.9 ou superior
- Biblioteca `Faker`
- Databricks Runtime, caso os arquivos sejam analisados em um workspace Databricks

Instale a dependência localmente com:

```bash
pip install Faker
```

## Geração dos datasets

A partir da pasta `SandBox`, execute:

```bash
python gerar_datasets.py
```

O script cria `livros.json` e `enderecos.csv` no diretório atual. Para atualizar os arquivos versionados em `files`, execute o script a partir dessa pasta ou mova os arquivos gerados para `files` depois da execução.

## Uso no Databricks

Depois de enviar os arquivos para o workspace ou para um volume do Databricks, eles podem ser carregados com Spark:

```python
livros = spark.read.json("/FileStore/tables/livros.json")
enderecos = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/FileStore/tables/enderecos.csv")
)

livros.display()
enderecos.display()
```

Para acessar os campos do endereço aninhado:

```python
livros.select(
    "id",
    "titulo",
    "preco",
    "quantidade",
    "endereco.cidade",
    "endereco.estado"
).display()
```

O caminho `/FileStore/tables/` é apenas um exemplo; substitua-o pelo caminho usado no seu workspace.

## Notebook

O notebook `SandBox/Tests.ipynb` pode ser usado para testar a leitura e a exploração dos datasets. Ao executá-lo, confirme os caminhos dos arquivos conforme o ambiente local ou o workspace Databricks.
