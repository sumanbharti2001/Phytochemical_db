CREATE DATABASE natural_products_db;
USE natural_products_db;
CREATE TABLE demo_data (
    Species_name TEXT,
    Compounds TEXT,
    Amount TEXT,
    Time_of_data_collection TEXT,
    Plant_part TEXT,
    Identification_method TEXT,
    Profile TEXT,
    Profile_base TEXT,
    DOI_number TEXT,
    Time_of_publication TEXT,
    Location TEXT,
    Country TEXT,
    Essential_oil_extraction_method TEXT,
    Development_stage TEXT,
    Season_month TEXT,
    Experimental_condition TEXT,
    Species_variety TEXT,
    Plant_Sample TEXT,
    Journals_name TEXT
);
DESCRIBE `demo data`;
SHOW COLUMNS FROM `demo data`;


