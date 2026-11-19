-- Practical 9: Trino SQL reading MySQL student data.
-- Requires Trino and MySQL Docker Compose + mysql.properties from the journal.
-- The journal configures MySQL; querying S3 also needs a separate S3 connector.
SHOW CATALOGS;
SHOW SCHEMAS FROM mysql;
SELECT * FROM mysql.university.students;
SELECT department, COUNT(*) AS total
FROM mysql.university.students
GROUP BY department;
