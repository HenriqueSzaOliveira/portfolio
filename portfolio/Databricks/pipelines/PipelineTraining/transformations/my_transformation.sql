CREATE OR REFRESH MATERIALIZED VIEW livros_pipe
AS SELECT * FROM read_files('/Volumes/dbportifolio/pipeline/files/*.json');

CREATE OR REFRESH MATERIALIZED VIEW enderecos_pipe
AS SELECT 
    row_number() over(order by endereco) as id,
    endereco.estado,
    endereco.cidade,
    endereco.bairro,
    endereco.rua,
    endereco.numero,
    endereco.cep
FROM (
    SELECT
        distinct endereco
    FROM 
        livros_pipe
);

CREATE OR REFRESH MATERIALIZED VIEW autores_pipe
AS SELECT 
    row_number() over(order by autor) as id,
    autor
FROM (
    SELECT
        distinct autor
    FROM 
        livros_pipe
);

CREATE OR REFRESH MATERIALIZED VIEW vendas_livros_pipe
AS SELECT 
    *
FROM (
    SELECT
        l.* except(endereco, autor),
        a.id as autor_id,
        e.id as endereco_id
    FROM 
        livros_pipe l
        JOIN
            autores_pipe a
        ON l.autor = a.autor
        JOIN
            enderecos_pipe e
        ON l.endereco.estado = e.estado
            AND l.endereco.cidade = e.cidade
            AND l.endereco.bairro = e.bairro
            AND l.endereco.rua = e.rua
            AND l.endereco.numero = e.numero
            AND l.endereco.cep = e.cep
);

CREATE OR REFRESH MATERIALIZED VIEW autor_mais_vendido_pipe
AS SELECT 
    *
FROM (
    SELECT
        a.autor,
        sum(q.quantidade) as total_vendas
    FROM 
        vendas_livros_pipe q
        JOIN
            autores_pipe a
        ON q.autor_id = a.id
    GROUP BY
        a.autor
)
LIMIT 1;

CREATE OR REFRESH MATERIALIZED VIEW vendas_cidades_pipe
AS SELECT 
    c.cidade,
    sum(v.quantidade) as total_vendas
FROM
    vendas_livros_pipe v
    JOIN
        enderecos_pipe c
    ON v.endereco_id = c.id
GROUP BY
    c.cidade;