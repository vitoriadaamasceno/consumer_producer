CREATE TABLE IF NOT EXISTS noticias (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    data_publicacao VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL
);