# The Sqlite3 database
The following is the SQL used to generate the Index table _(the exact command is listed in the pysec_project README.md)_

    BEGIN;
    --
    -- Create model Index
    --
    CREATE TABLE "pysec_index"
    ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "filename" text NOT NULL,
    "name" text NOT NULL,
    "date" date NULL,
    "cik" integer NOT NULL,
    "form" varchar(10) NOT NULL,
    "quarter" varchar(6) NOT NULL);

    COMMIT;

We can verify the contents of the index table with the following commands, adopted from the [Sqlite3 website](https://www.sqlite.org/cli.html).

First we run:
    sqlite3 db.sqlite3
_noting that our database is cleverly named db.sqlite3 for this project._ This opens the sqlite shell which we will work in. The following simple sql command will show the contents of our database (all 607134 rows).

    select * from pysec_index
