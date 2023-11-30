In Datenbank musst ihr genau eine Tabele erstellen:

mysql> SELECT * FROM todos;
+----+-----------+--------+---------+
| No | Todo item | Status | Actions |
+----+-----------+--------+---------+

--

mysql Commands:
Create Table :
CREATE TABLE todos (
    No INT AUTO_INCREMENT PRIMARY KEY,
    `Todo item` VARCHAR(255) NOT NULL,
    `Status` VARCHAR(255) NOT NULL,
    `Actions` VARCHAR(255) NOT NULL
);

------------
Das braucht ihr nicht :
das ist nur für info.
ALTER TABLE todos MODIFY COLUMN No INT DEFAULT 0;
ALTER TABLE todos MODIFY COLUMN No INT AUTO_INCREMENT PRIMARY KEY;
