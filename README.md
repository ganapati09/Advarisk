# ETL Pipeline for E-commerce Data

## Setup Instructions

1. **Install MySQL**:
    - Follow the instructions [here](https://dev.mysql.com/doc/mysql-getting-started/en/) to install MySQL.
    - Create a database named `ecommerce`.

2. **Install MongoDB**:
    - Follow the instructions [here](https://docs.mongodb.com/manual/installation/) to install MongoDB.
    - Create a database named `ecommerce_aggregated`.

3. **Install Python and Required Libraries**:
    ```bash
    pip install pandas  pymongo pyodbc apache-airflow
    ```

4. **Create SQL Tables and Insert Data**:
    - Execute the provided SQL commands in your MySQL database to create the necessary tables using src/tables_ddl.sql.

## Running the Pipeline

1. **Airflow Setup**:
    - Follow the Airflow installation guide [here](https://airflow.apache.org/docs/apache-airflow/stable/start.html).
    - Place the `etl_dag.py` file in the Airflow DAGs folder.

2. **Start Airflow**:
    ```bash
    airflow scheduler
    airflow webserver
    ```
    - Access the Airflow web interface at `http://localhost:8080` and trigger the `etl_pipeline` DAG.

## Data Structures and Time Complexities

- **Pandas DataFrame**: Used for data manipulation and transformation. Operations like merge and groupby have average time complexities of O(n log n) and O(n), respectively.

## Challenges and Solutions


1. **Ensuring Data Consistency**:
    - Implemented data cleaning steps to remove duplicates and handle missing values.

2. **Fault Tolerance in Airflow**:
    - Configured retries and logging to handle failures and ensure data integrity.
