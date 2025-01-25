-- Create Brand Table
CREATE TABLE Brand (
    Brandid SERIAL PRIMARY KEY,
    Brandname VARCHAR(100) NOT NULL
);

-- Create Drink Table
CREATE TABLE Drink (
    Drinkid SERIAL PRIMARY KEY,
    Brandid INTEGER NOT NULL REFERENCES Brand(Brandid),
    Drinkname VARCHAR(100) NOT NULL,
    Drinkvolume FLOAT NOT NULL,
    Drinkcaffeine FLOAT NOT NULL,
    Drinkstrength FLOAT NOT NULL
);

-- Create Store Table
CREATE TABLE Store (
    Storeid SERIAL PRIMARY KEY,
    Storename VARCHAR(100) NOT NULL
);

-- Create Transaction Table
CREATE TABLE Transaction (
    Transactionid SERIAL PRIMARY KEY,
    Drinkid INTEGER NOT NULL REFERENCES Drink(Drinkid),
    Storeid INTEGER NOT NULL REFERENCES Store(Storeid),
    Transactioncost FLOAT NOT NULL,
    Transactiondate TIMESTAMP NOT NULL
);