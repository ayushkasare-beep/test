# Practical 9 — Trino — Distributed SQL

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `docker-compose.yml`
- `mysql/init.sql`
- `etc/catalog/mysql.properties`

## Step-by-step execution (Windows PowerShell)

1. Open Docker Desktop and this folder in VS Code.
2. Verify `docker-compose.yml`, `mysql/init.sql` and `etc/catalog/mysql.properties` exist.
3. Run `docker compose up -d`.
4. Check containers with `docker compose ps`.
5. Query MySQL through Trino using `docker exec trino_coordinator trino --execute "SELECT * FROM mysql.university.students"`.

## Expected result

Four student records from MySQL, queried through Trino.

## Important note

The aim mentions querying two sources (such as MySQL and S3), but the supplied journal configures only MySQL.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 9

Q.1 Distributed SQL: Set up a Trino (Presto) coordinator and query data across
two different sources (e.g., MySQL and S3) simultaneously.


Step 1: Open VS Code

   1. Open VS Code.
   2. Create folder
   3. Select folder and create file
      Docker-compose.yml

      services:
        mysql:
          image: mysql:8.0
          container_name: trino_mysql
          environment:
             MYSQL_ROOT_PASSWORD: root123
             MYSQL_DATABASE: university
          ports:
             - "3307:3306"
          volumes:
             - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql:ro


        trino:
          image: trinodb/trino:latest
          container_name: trino_coordinator
          ports:
             - "8080:8080"
          volumes:
             - ./etc/catalog:/etc/trino/catalog
          depends_on:
             - mysql


Create new folder mysql


CREATE TABLE university.students (
    student_id INT PRIMARY KEY,
     student_name VARCHAR(100),
     department VARCHAR(100)
);


INSERT INTO university.students VALUES
(101, 'Aarav', 'Data Science'),
(102, 'Diya', 'Computer Science'),
(103, 'Rohan', 'Data Science'),
(104, 'Meera', 'Computer Science');


CREATE USER IF NOT EXISTS 'trino_user'@'%'
IDENTIFIED BY 'trino123';


GRANT SELECT ON university.* TO 'trino_user'@'%';




Create file init.sql write following code
Create the Trino connection file
      Right-click the catalog folder inside etc.
      Select New File.
      Name it mysql.properties.

connector.name=mysql
connection-url=jdbc:mysql://mysql:3306
connection-user=trino_user
connection-password=trino123




Output:
```
