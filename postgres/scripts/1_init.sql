CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work(creation_date);

 CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS person_full_name_idx ON content.person (full_name);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
	person_id uuid NOT NULL REFERENCES content.person (id),
    film_work_id uuid NOT NULL REFERENCES content.film_work (id),
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE TABLE IF NOT EXISTS content.genre (
	id uuid PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT,
	created timestamp with time zone,
	modified timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS genre_name_idx ON content.genre (name);


CREATE TABLE IF NOT EXISTS content.genre_film_work (
	id uuid PRIMARY KEY,
	genre_id uuid NOT NULL REFERENCES content.genre (id),
	film_work_id uuid NOT NULL REFERENCES content.film_work (id),
	created timestamp with time zone
);

CREATE INDEX IF NOT EXISTS genre_film_work_idx ON content.genre_film_work (genre_id, film_work_id);
