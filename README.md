# ETL and Data Warehouse Project

This project is the final project for a database course completed in Spring 2021 at Amirkabir University of Tehran. It involves designing and implementing a relational database, ETL processes, and a data warehouse. The repository contains the following main components:

- **ETL**: Scripts for extracting, transforming, and loading data between databases.
- **Database**: Schema and model for the relational database.
- **Data Warehouse**: Additional data and scripts for the data warehouse.

More information about the details of the project definition is available in Two Languages: English and Persian.

- **English**: `simple etl project/Project Description (EN).pdf`
- **Persian**: `simple etl project/Project Description (FA).pdf`

## Repository Structure

- `ETL`:
  - **ETL.py**: Main script for ETL operations.
  - **create_library.py**: Script for creating the database schema.
  - **create_warehouse.py**: Script for creating the data warehouse schema.
- `Database`:
  - **schema.sql**: SQL script for creating the database schema.
  - **data_model.pdf**: Diagram of the database model.
- `Data_Warehouse`:
  - **warehouse_schema.sql**: SQL script for creating the data warehouse schema.
  - **warehouse_data_model.pdf**: Diagram of the data warehouse model.
  - **answer.pdf**: Additional data for answering project questions.

## How to Run the Project

### Prerequisites

- Python 3.x
- PostgreSQL
- psycopg2 library

### Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ashkanvg/ETL-Data-Warehouse.git
    cd ETL-Data-Warehouse
    ```

2. **Install Python Dependencies**:
    ```bash
    pip install psycopg2
    ```

3. **Database Setup**:
    - Ensure you have PostgreSQL installed and running.
    - Create two PostgreSQL databases: one for the source data and one for the data warehouse.

4. **Run the Database Schema Scripts**:
    - Execute the `schema.sql` script to create the database schema:
      ```bash
      psql -U <username> -d <source_database> -f DATABASE/schema.sql
      ```
    - Execute the `warehouse_schema.sql` script to create the data warehouse schema:
      ```bash
      psql -U <username> -d <warehouse_database> -f Data_Warehouse/warehouse_schema.sql
      ```

5. **Run the ETL Script**:
    - Ensure the `ETL.py` script is properly configured with your database connection details.
    - Run the ETL script to transfer data from the source database to the data warehouse:
      ```bash
      python ETL/ETL.py
      ```

## Project Components

### Relational Database Design
The relational database is designed to store library data, including books, authors, genres, and member information. The database is normalized to 5NF to ensure minimal redundancy and dependency.

### ETL Process
The ETL process involves extracting data from the source database, transforming it as needed, and loading it into the data warehouse. The `ETL.py` script handles this process, ensuring data consistency and handling changes in the source data (inserts, updates, deletes).

### Data Warehouse Design
The data warehouse is designed to store historical data for analytical purposes. It supports "time travel" queries to view the state of the database at any point in time. The warehouse schema includes tables for historical records and maintains a log of data changes.

## Additional Information

For more detailed instructions on running the project and the specifics of each script, refer to the `ETL_File_Description (EN).pdf` or `ETL_File_Description (FA).pdf` files included in the `simple etl project/ETL`.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
