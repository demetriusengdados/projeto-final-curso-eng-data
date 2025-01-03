-- Subdimensão Cidade
CREATE TABLE dim_cidade (
    cidade_id INT PRIMARY KEY,
    cidade_nome VARCHAR(50),
    estado_nome VARCHAR(50)
);

-- Dimensão Cliente normalizada
CREATE TABLE dim_cliente (
    cliente_id INT PRIMARY KEY,
    nome_cliente VARCHAR(100),
    idade INT,
    genero VARCHAR(10),
    cidade_id INT,
    FOREIGN KEY (cidade_id) REFERENCES dim_cidade(cidade_id)
);

-- Subdimensão Categoria
CREATE TABLE dim_categoria (
    categoria_id INT PRIMARY KEY,
    nome_categoria VARCHAR(50)
);

-- Dimensão Produto normalizada
CREATE TABLE dim_produto (
    produto_id INT PRIMARY KEY,
    nome_produto VARCHAR(100),
    categoria_id INT,
    preco DECIMAL(10, 2),
    FOREIGN KEY (categoria_id) REFERENCES dim_categoria(categoria_id)
);

-- Subdimensão Ano-Mês
CREATE TABLE dim_ano_mes (
    ano INT,
    mes INT,
    PRIMARY KEY (ano, mes)
);

-- Dimensão Tempo normalizada
CREATE TABLE dim_tempo (
    tempo_id INT PRIMARY KEY,
    data DATE,
    ano INT,
    mes INT,
    dia INT,
    trimestre INT,
    FOREIGN KEY (ano, mes) REFERENCES dim_ano_mes(ano, mes)
);

-- Tabela Fato Vendas com referências às dimensões normalizadas
CREATE TABLE fato_vendas (
    venda_id INT PRIMARY KEY,
    cliente_id INT,
    produto_id INT,
    tempo_id INT,
    quantidade INT,
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (cliente_id) REFERENCES dim_cliente(cliente_id),
    FOREIGN KEY (produto_id) REFERENCES dim_produto(produto_id),
    FOREIGN KEY (tempo_id) REFERENCES dim_tempo(tempo_id)
);
