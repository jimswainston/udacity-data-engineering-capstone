# DROP TABLES

article_table_drop = "DROP TABLE IF EXISTS articles;"
author_table_drop = "DROP TABLE IF EXISTS authors;"
affiliation_table_drop = "DROP TABLE IF EXISTS affiliations;"
affiliation_errors_table_drop = "DROP TABLE IF EXISTS affiliation_errors;"



#CREATE TABLES

article_table_create = ("""
CREATE TABLE articles (
    article_id uuid NOT NULL,
    DOI VARCHAR,
    title VARCHAR,
    published_date DATE,
    PRIMARY KEY (article_id)
);
""")

author_table_create = ("""
CREATE TABLE authors (
    author_id uuid NOT NULL,
    article_id uuid NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    PRIMARY KEY (author_id)
);
""")

affiliation_table_create = ("""
CREATE TABLE author_affiliation (
    affiliation_id uuid NOT NULL,
    author_id uuid NOT NULL,
    country_name VARCHAR,
    PRIMARY KEY (affiliation_id)
);
""")

affiliationErrors_table_create =("""
CREATE TABLE affiliation_errors (
    affiliation_id uuid NOT NULL,
    author_id uuid NOT NULL,
    affiliation_name VARCHAR,
    PRIMARY KEY (affiliation_id)
);
""")

# INSERT RECORDS

article_table_insert = ("""
INSERT INTO articles (article_id,DOI,title,published_date) values (%s,%s,%s,%s);
""")



# QUERY LISTS

create_table_queries = [article_table_create, author_table_create, affiliation_table_create, affiliationErrors_table_create]
drop_table_queries = [article_table_drop, author_table_drop, affiliation_table_drop, affiliation_errors_table_drop]