Caffeine Tracker 🥤☕

Welcome to the Caffeine Tracker! This application helps you track your energy drink consumption, including details like brands, drinks, stores, and transactions. It's hosted on Replit and uses PostgreSQL for data storage.
Features ✨

    Track Energy Drinks: Log your energy drink consumption with details like brand, drink name, volume, caffeine content, and strength.

    Store Information: Record where you purchased your energy drinks.

    Transaction History: Keep track of purchase dates and costs.

    Simple Interface: Easy-to-use command-line interface (CLI) for logging and viewing data.

    PostgreSQL Database: Reliable and scalable data storage using PostgreSQL.

Database Schema 📊

The application uses the following PostgreSQL tables:
Brand Table

Stores information about energy drink brands.
sql
Copy

CREATE TABLE Brand (
    Brandid SERIAL PRIMARY KEY,
    Brandname VARCHAR(100) NOT NULL
);

Drink Table

Stores information about specific energy drinks, linked to a brand.
sql
Copy

CREATE TABLE Drink (
    Drinkid SERIAL PRIMARY KEY,
    Brandid INTEGER NOT NULL REFERENCES Brand(Brandid),
    Drinkname VARCHAR(100) NOT NULL,
    Drinkvolume FLOAT NOT NULL,
    Drinkcaffeine FLOAT NOT NULL,
    Drinkstrength FLOAT NOT NULL
);

Store Table

Stores information about stores where energy drinks are purchased.
sql
Copy

CREATE TABLE Store (
    Storeid SERIAL PRIMARY KEY,
    Storename VARCHAR(100) NOT NULL
);

Transaction Table

Stores transaction details, including the drink, store, cost, and date.
sql
Copy

CREATE TABLE Transaction (
    Transactionid SERIAL PRIMARY KEY,
    Drinkid INTEGER NOT NULL REFERENCES Drink(Drinkid),
    Storeid INTEGER NOT NULL REFERENCES Store(Storeid),
    Transactioncost FLOAT NOT NULL,
    Transactiondate TIMESTAMP NOT NULL
);

Getting Started 🚀
Prerequisites

    A Replit account (sign up at replit.com).

    Basic knowledge of Python and SQL.

    A PostgreSQL database (you can use Replit's built-in database or an external one).

Installation

    Fork the Replit Project:

        Click the "Fork" button on the Replit project page to create your own copy.

    Set Up PostgreSQL:

        If using Replit's built-in database, follow the prompts to set up PostgreSQL.

        If using an external database, update the DATABASE_URL environment variable in the .env file with your PostgreSQL connection string.

    Install Dependencies:

        The project uses psycopg2 for PostgreSQL interaction. Install it by running:
        bash
        Copy

        pip install psycopg2-binary

    Run the Application:

        Start the application by running:
        bash
        Copy

        python main.py

Usage

    Add a Brand:

        Add a new energy drink brand to the Brand table.

    Add a Drink:

        Add a new energy drink to the Drink table, linking it to a brand.

    Add a Store:

        Add a new store to the Store table.

    Log a Transaction:

        Log a purchase transaction, including the drink, store, cost, and date.

    View Data:

        View all brands, drinks, stores, and transactions.

    Exit the Application:

        Type exit to close the application.

Environment Variables 🔧

The following environment variable is used:

    DATABASE_URL: The connection string for your PostgreSQL database.

Example .env file:
env
Copy

DATABASE_URL=postgresql://username:password@host:port/database_name

Example Queries

Here are some example SQL queries you can use to interact with the database:

    Get All Brands:
    sql
    Copy

    SELECT * FROM Brand;

    Get All Drinks for a Specific Brand:
    sql
    Copy

    SELECT Drinkname, Drinkvolume, Drinkcaffeine, Drinkstrength
    FROM Drink
    WHERE Brandid = 1;

    Get All Transactions:
    sql
    Copy

    SELECT t.Transactionid, b.Brandname, d.Drinkname, s.Storename, t.Transactioncost, t.Transactiondate
    FROM Transaction t
    JOIN Drink d ON t.Drinkid = d.Drinkid
    JOIN Brand b ON d.Brandid = b.Brandid
    JOIN Store s ON t.Storeid = s.Storeid;

Contributing 🤝

Contributions are welcome! If you'd like to improve the project, feel free to open an issue or submit a pull request.
License 📄

This project is licensed under the MIT License. See the LICENSE file for details.
