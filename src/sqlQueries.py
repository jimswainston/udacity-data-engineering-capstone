# DROP TABLES

article_table_drop = "DROP TABLE IF EXISTS articles;"
author_table_drop = "DROP TABLE IF EXISTS authors;"
affiliation_table_drop = "DROP TABLE IF EXISTS affiliations;"
affiliation_errors_table_drop = "DROP TABLE IF EXISTS affiliation_errors;"
year_table_drop = "DROP TABLE IF EXISTS dim_year"
country_table_drop = "DROP TABLE IF EXISTS dim_country"
gdp_table_drop = "DROP TABLE IF EXISTS fact_gdp"


#CREATE TABLES

article_table_create = ("""
CREATE TABLE articles (
    article_id uuid NOT NULL,
    DOI VARCHAR,
    title VARCHAR,
    published_date DATE,
    year_id INT,
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
    country_id INT,
    PRIMARY KEY (affiliation_id),
    CONSTRAINT fk_country
      FOREIGN KEY(country_id) 
	  REFERENCES dim_country(country_id)
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

year_table_create = ("""
CREATE TABLE dim_year (
    year_id INT,
    year INT,
    PRIMARY KEY (year_id)
);
""")

country_table_create = ("""
CREATE TABLE dim_country (
    country_id serial,
    country_code VARCHAR,
    country_name VARCHAR,
    PRIMARY KEY (country_id)
);
""")

fact_gdp_table_create =("""
CREATE TABLE fact_gdp (
    id uuid NOT NULL,
    country_id INT,
    year_id INT,
    gdp_amount FLOAT8,
    PRIMARY KEY (id)
);
""")

# INSERT RECORDS

article_table_insert = ("""
INSERT INTO articles (article_id,DOI,title,published_date,year_id) values (%s,%s,%s,%s,%s);
""")

author_table_insert = ("""
INSERT INTO authors (author_id,article_id,first_name,last_name) values (%s,%s,%s,%s);
""")

affiliation_table_insert = ("""
INSERT INTO author_affiliation (affiliation_id,author_id,country_id) values (%s,%s,%s);
""")

affiliation_errors_table_insert = ("""
INSERT INTO affiliation_errors (affiliation_id,author_id,affiliation_name) values (%s,%s,%s);
""")

year_table_insert = ("""
INSERT INTO dim_year (year_id,year) values (%s,%s);
""")

country_table_insert = ("""
INSERT INTO dim_country (country_code,country_name) values (%s,%s);
""")

gdp_table_insert = ("""
INSERT INTO fact_gdp (id,country_id,year_id,gdp_amount) values (%s,%s,%s,%s);
""")



# QUERY LISTS

create_table_queries = [article_table_create, author_table_create, affiliationErrors_table_create,year_table_create,country_table_create,fact_gdp_table_create,affiliation_table_create]
drop_table_queries = [article_table_drop, author_table_drop, affiliation_table_drop, affiliation_errors_table_drop,year_table_drop,country_table_drop,gdp_table_drop]