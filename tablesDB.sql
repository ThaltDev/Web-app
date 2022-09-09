create table access(
    email varchar(255) not null,
    nameFirst varchar(255),
    nameLast varchar(255),
    employe_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table employes(
    email varchar(255) not null,
    nameFirst varchar(255) not null,
    nameLast varchar(255) not null,
    salary int,
    salaries_id int,
    works_id int,
    servies_id int,
    project_id int,
    group_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table salaries(
    perYear int,
    bonus int DEFAULT 0,
    start_salary int,
    date_hire date,
    fire_bool BOOLEAN DEFAULT False,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table works(
    done_bool BOOLEAN DEFAULT False,
    work_bool BOOLEAN DEFAULT False,
    public BOOLEAN DEFAULT False,
    group_id int,
    bonus_complet int DEFAULT 0,
    project_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table servies(
    customer_help_now int DEFAULT null,
    customers_servised int DEFAULT 0,
    employe_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table customer(
    time_used_app int DEFAULT 0,
    email varchar(255) DEFAULT "",
    name varchar(255),
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table project(
    works_id int DEFAULT 0,
    name varchar(255),
    main_employe_id int,
    summary text,
    folder_path varchar(255),
    start_date date,
    working_bool DEFAULT False,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table groupEmployes(
    work_id int,
    name varchar(255),
    id INTEGER PRIMARY KEY AUTOINCREMENT
)