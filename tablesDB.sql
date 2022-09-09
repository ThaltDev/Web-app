/*DROP TABLE access;
DROP TABLE employes;
DROP TABLE bank;
DROP TABLE salary;
DROP TABLE servies;
DROP TABLE customer;
DROP TABLE project;
DROP TABLE groupEmployes;
DROP TABLE chain_projects;
DROP TABLE chain_employes;*/

create table access(
    employe_id int
);
create table employes(
    email varchar(255) not null,
    FirstName varchar(255) not null,
    LastName varchar(255) not null,
    bank_id int,
    servies_id int,
    main_project_id int,
    group_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table bank(
    bonus int DEFAULT 0,
    salary_id int,
    date_hire date,
    fire_bool BOOLEAN DEFAULT False,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employe_id int
);
create table salary(
    perYear int,
    previous_salary_id int,
    id integer primary key autoincrement
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
    servies_help_now Default null,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table project(
    name varchar(255),
    main_employe_id int,
    summary text,
    folder_path varchar(255),
    start_date date,
    version int,
    working_bool DEFAULT False,
    group_id int,
    bonus int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table groupEmployes(
    projects_id int,
    name varchar(255),
    emlpoyes_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table chain_projects(
    project_id int,
    previous_chain_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
create table chain_employes(
    employe_id int,
    previous_chain_id int,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);