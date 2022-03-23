import sqlite3


def get_db_data(db_name, sql):
    with sqlite3.connect(db_name) as db:
        db.row_factory = sqlite3.Row
        return db.execute(sql).fetchall()


def set_db_data(db_name, sql):
    with sqlite3.connect(db_name) as db:
        db.execute(sql)


def create_table():
    sql_animals = """ create table `animals` (
                `id` varchar(30) UNIQUE,
                `name` NVARCHAR(50),
                `animal_type` NVARCHAR(30),
                `breed` NVARCHAR(30),
                `date_of_birth` DATE,
                `color_1` NVARCHAR(10),
                `color_2` NVARCHAR(10)  
             )"""
    set_db_data("shelter.db", sql_animals)

    sql_shelter = """ create table `shelter` (
                    `id` integer PRIMARY KEY AUTOINCREMENT,
                    `animal_id` VARCHAR(30) UNIQUE,
                    `outcome_subtype` NVARCHAR(30),
                    `outcome_type` NVARCHAR(30),
                    `outcome_month` INTEGER,
                    `outcome_year` INTEGER,
                    `age_upon_outcome` NVARCHAR(10),

                    FOREIGN KEY (animal_id) REFERENCES animals(id)
                 )"""
    set_db_data("shelter.db", sql_shelter)


if __name__ == '__main__':
    pass