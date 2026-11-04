-- 00_creation_tables.sql : crée les 4 tables de la base pizza.db (auteur : Zohair)
DROP TABLE IF EXISTS order_details;   -- on supprime d'abord les tables qui dépendent des autres
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS pizzas;
DROP TABLE IF EXISTS pizza_types;

CREATE TABLE pizza_types (
    pizza_type_id TEXT PRIMARY KEY,   -- identifiant unique du type
    name TEXT,
    category TEXT,
    ingredients TEXT
);

CREATE TABLE pizzas (
    pizza_id TEXT PRIMARY KEY,
    pizza_type_id TEXT,
    size TEXT,
    price REAL,                       -- REAL = nombre décimal
    FOREIGN KEY (pizza_type_id) REFERENCES pizza_types(pizza_type_id)   -- chaque pizza a un type existant
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    date TEXT,                        -- SQLite n'a pas de type date : on garde le format AAAA-MM-JJ
    time TEXT
);

CREATE TABLE order_details (
    order_details_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    pizza_id TEXT,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (pizza_id) REFERENCES pizzas(pizza_id)
);