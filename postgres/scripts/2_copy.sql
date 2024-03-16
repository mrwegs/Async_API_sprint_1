COPY content.film_work FROM '/data/film_work.csv' DELIMITER ',' CSV HEADER;
COPY content.genre FROM '/data/genre.csv' DELIMITER ',' CSV HEADER;
COPY content.genre_film_work FROM '/data/genre_film_work.csv' DELIMITER ',' CSV HEADER;
COPY content.person FROM '/data/person.csv' DELIMITER ',' CSV HEADER;
COPY content.person_film_work FROM '/data/person_film_work.csv' DELIMITER ',' CSV HEADER;