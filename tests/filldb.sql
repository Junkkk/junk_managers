CREATE TYPE globalroleenum AS ENUM (
	'owner',
	'employee');


CREATE TYPE projectroleenum AS ENUM (
	'admin',
	'manager');


CREATE TABLE public.companies (
	id serial NOT NULL,
	"name" varchar(50) NULL,
	CONSTRAINT companies_pkey PRIMARY KEY (id)
);


CREATE TABLE public.projects (
	id serial NOT NULL,
	"name" varchar(50) NULL,
	company_id int4 NULL,
	CONSTRAINT projects_pkey PRIMARY KEY (id),
	CONSTRAINT projects_company_id_fkey FOREIGN KEY (company_id) REFERENCES companies(id)
);


CREATE TABLE public.users (
	id serial NOT NULL,
	"name" varchar(50) NULL,
	"role" globalroleenum NULL,
	company_id int4 NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id),
	CONSTRAINT users_company_id_fkey FOREIGN KEY (company_id) REFERENCES companies(id)
);


CREATE TABLE public.memberships (
	id serial NOT NULL,
	user_id int4 NULL,
	project_id int4 NULL,
	"role" projectroleenum NULL,
	CONSTRAINT memberships_pkey PRIMARY KEY (id),
	CONSTRAINT memberships_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(id),
	CONSTRAINT memberships_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)
);



INSERT INTO public.companies ("name") VALUES
	 ('Microsoft'),
	 ('Samsung'),
	 ('VK'),
	 ('OK'),
	 ('CS');

INSERT INTO public.users ("name","role",company_id) VALUES
	 ('Anton','owner',1),
	 ('Alena','employee',1),
	 ('Alisa','employee',1),
	 ('Almeria','employee',1),
	 ('Junk','employee',1),
	 ('Epitone','employee',1),
	 ('Minami','employee',1),
	 ('Krabzr','employee',1),
	 ('Stone','owner',2),
	 ('Winter','employee',2);
INSERT INTO public.users ("name","role",company_id) VALUES
	 ('Summer','employee',2),
	 ('Chill','employee',2),
	 ('Dena','employee',2),
	 ('Freedom','employee',2),
	 ('Ferru','employee',2),
	 ('Geo','employee',2),
	 ('Hendrik','employee',2),
	 ('Meta','employee',2),
	 ('Enzore','employee',2);

INSERT INTO public.projects ("name",company_id) VALUES
	 ('Umbrella',1),
	 ('Werwolf',1),
	 ('Apple',2),
	 ('Amway',2);
	 
INSERT INTO public.memberships (user_id,project_id,"role") VALUES
	 (2,1,'admin'),
	 (3,1,'manager'),
	 (4,1,'manager'),
	 (5,1,'manager'),
	 (6,2,'admin'),
	 (7,2,'manager'),
	 (8,2,'manager'),
	 (2,2,'manager'),
	 (10,3,'admin'),
	 (11,3,'manager');
INSERT INTO public.memberships (user_id,project_id,"role") VALUES
	 (12,3,'manager'),
	 (13,3,'manager'),
	 (14,3,'manager'),
	 (15,4,'admin'),
	 (16,4,'manager'),
	 (17,4,'manager'),
	 (18,4,'manager'),
	 (19,4,'manager');
