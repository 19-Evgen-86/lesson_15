import sqlite3


def get_db_data(db_name, sql):
    with sqlite3.connect(db_name) as db:
        db.row_factory = sqlite3.Row
        return db.execute(sql).fetchall()


def set_db_data(db_name, sql):
    with sqlite3.connect(db_name) as db:
        db.execute(sql)


def create_table_shelter_db():
    sql_animals_breed = """ CREATE TABLE  `animals_breed` (
                        `id` INTEGER  PRIMARY KEY AUTOINCREMENT,
                        `breed` NVARCHAR(30)             
                     )"""

    set_db_data("shelter.db", sql_animals_breed)

    ql_animals_type = """ CREATE TABLE  `animals_type` (
                            `id` INTEGER  PRIMARY KEY AUTOINCREMENT,
                            `animal_type` NVARCHAR(30)                
                         )"""
    set_db_data("shelter.db", ql_animals_type)

    sql_animals_color = """ CREATE TABLE  `animals_color` (
                                `id` INTEGER  PRIMARY KEY AUTOINCREMENT,
                                `color_1` NVARCHAR(30),
                                `color_2` NVARCHAR(30)                
                             )"""
    set_db_data("shelter.db", sql_animals_color)

    sql_animals = """ CREATE TABLE  `animals` (
                `id` varchar(30) PRIMARY KEY,
                `name` NVARCHAR(50),
                `animal_type_id` INTEGER,
                `breed_id` INTEGER,
                `date_of_birth` date,
                `color_id` INTEGER, 
                 FOREIGN KEY (breed_id) REFERENCES animals_breed(id),
                 FOREIGN KEY (animal_type_id) REFERENCES animals_type(id),
                 FOREIGN KEY (color_id) REFERENCES animals_color(id)
             )"""
    set_db_data("shelter.db", sql_animals)

    sql_animals_programs = """ CREATE TABLE  `animals_programs` (
                        `id` integer PRIMARY KEY AUTOINCREMENT,
                        `animal_program` NVARCHAR(30)                   
                     )"""
    set_db_data("shelter.db", sql_animals_programs)

    sql_animals_status = """ CREATE TABLE  `animals_status` (
                           `id` integer PRIMARY KEY AUTOINCREMENT,
                           `animal_status` NVARCHAR(30)                   
                        )"""
    set_db_data("shelter.db", sql_animals_status)

    sql_shelter = """ CREATE TABLE `shelter` (
                    `id` integer PRIMARY KEY AUTOINCREMENT,
                    `animal_id` VARCHAR(30),
                    `outcome_subtype` INTEGER ,
                    `outcome_type` INTEGER,
                    `outcome_month` INTEGER,
                    `outcome_year` INTEGER,
                    `age_upon_outcome` INTEGER,
                    FOREIGN KEY (outcome_subtype) REFERENCES animals_programs(id),
                    FOREIGN KEY (outcome_type) REFERENCES sql_animals_status(id),
                    FOREIGN KEY (animal_id) REFERENCES animals(id)
                 )"""
    set_db_data("shelter.db", sql_shelter)


def copy_animals_breed():
    with sqlite3.connect("animal.db") as animals:
        animals_breed = animals.execute("select distinct breed from animals")

    with sqlite3.connect("shelter.db") as shelter:
        shelter.executemany(" insert into animals_breed (breed) values (?)", animals_breed)


def copy_animals_status():
    with sqlite3.connect("animal.db") as animals:
        animals_status = animals.execute("select distinct outcome_type from animals")

    with sqlite3.connect("shelter.db") as shelter:
        shelter.executemany(" insert into animals_status (animal_status) values (?)", animals_status)


def copy_animals_programs():
    with sqlite3.connect("animal.db") as animals:
        animals_programs = animals.execute("select distinct outcome_subtype from animals")

    with sqlite3.connect("shelter.db") as shelter:
        shelter.executemany(" insert into animals_programs (animal_program) values (?)", animals_programs)


def copy_animals_type():
    with sqlite3.connect("animal.db") as animals:
        animals_type = animals.execute("select distinct animal_type from animals")

    with sqlite3.connect("shelter.db") as shelter:
        shelter.executemany(" insert into animals_type (animal_type) values (?)", animals_type)

def copy_animals_color():
    with sqlite3.connect("animal.db") as animals:
        animals_color = animals.execute("select distinct `color1`,`color2` from animals")

    with sqlite3.connect("shelter.db") as shelter:
        shelter.executemany(" insert into animals_color (color_1,color_2) values (?,?)", animals_color)

def insert_to_animals():
    sql_query = "insert into animals (id,name,animal_type_id,breed_id,date_of_birth,color_id) " \
                "values ('A686497','Chester',1,2,date('2014-03-22'),1)," \
                "('A617061','Pumpkin',1,4,date('2011-08-02'),6)"
    set_db_data("shelter.db", sql_query)


def insert_to_shelter():
    sql_query = "insert into shelter (animal_id,outcome_subtype,outcome_type,outcome_month,outcome_year,age_upon_outcome) " \
                "values ('A686497',3,5,4,2015,'3 months')," \
                "('A617061',5,7,8,2017,'6 months')"
    set_db_data("shelter.db", sql_query)


def get_animal_by_id(id: int):
    sql_query = f"SELECT `name`,`animal_type`,`breed`,`animal_program`,`animal_status` " \
                f"FROM `animals` LEFT JOIN `shelter` ON shelter.animal_id = animals.id " \
                f"LEFT JOIN animals_type ON animals.animal_type_id = animals_type.id " \
                f"LEFT JOIN animals_status ON shelter.outcome_type = animals_status.id " \
                f"LEFT JOIN animals_programs ON shelter.outcome_subtype = animals_programs.id " \
                f"LEFT JOIN animals_breed ON animals.breed_id = animals_breed.id " \
                f"WHERE shelter.id = '{id}'"

    result = get_db_data("shelter.db", sql_query)
    if result:
        for item in result:
            return dict(item)
    else:
        return {"error": f" NOT FOUND ID = {id}"}

