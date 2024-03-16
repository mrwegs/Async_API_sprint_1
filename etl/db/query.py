def get_filmwork_query(modified: str):
    return f"""
                SELECT film.id,
                film.rating,
                film.title,
                film.description,
                film.file_path,
                film.type,
                ARRAY_AGG(DISTINCT genre.name) AS genre,
                ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'actor') AS actors_names,
                ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'writer') AS writers_names,
                ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film.role = 'director') AS director,
                ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE person_film.role = 'actor') AS actors,
                ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE person_film.role = 'writer') AS writers,
                GREATEST(film.modified , MAX(person.modified), MAX(genre.modified)) AS modified
                FROM content.film_work film
                LEFT JOIN content.genre_film_work AS genre_film ON film.id = genre_film.film_work_id
                LEFT JOIN content.genre AS genre ON genre_film.genre_id = genre.id
                LEFT JOIN content.person_film_work AS person_film ON film.id = person_film.film_work_id
                LEFT JOIN content.person AS person ON person_film.person_id = person.id
                WHERE
                GREATEST(film.modified , person.modified, genre.modified) >= '{modified}'
                GROUP BY film.id
                ORDER BY modified
"""


def get_persons_query(modified: str):
    return f"""
    SELECT 
            person_with_films.person_id, 
            person_with_films.full_name,
            ARRAY_AGG(distinct
                jsonb_build_object('uuid', person_with_films.film_id, 'roles', roles)) AS films,
            person_with_films.modified
    FROM (
            SELECT 
                film.id as film_id,
                person.id as person_id, 
                person.full_name as full_name,
                ARRAY_AGG(DISTINCT (person_film.role)) AS roles,
                GREATEST(film.modified, MAX(genre.modified), MAX(person.modified)) as modified
            FROM 
                content.film_work film
                LEFT JOIN content.genre_film_work AS genre_film ON film.id = genre_film.film_work_id
                LEFT JOIN content.genre AS genre ON genre_film.genre_id = genre.id
                LEFT JOIN content.person_film_work AS person_film ON film.id = person_film.film_work_id
                LEFT JOIN content.person as person on person.id = person_film.person_id
            WHERE person.id is not null and GREATEST(film.modified, genre.modified, person.modified) >= '{modified}'
            GROUP BY 
                film.id, person.id, person.full_name
        ) AS person_with_films
    GROUP BY 
        person_with_films.person_id, person_with_films.full_name, person_with_films.modified
    ORDER BY modified
"""


def get_genres_query(modified: str):
    return f"""
    SELECT 
        gr.id,
        gr.name,
        gr.modified 
    FROM 
        content.genre gr
    WHERE
        gr.modified >= '{modified}'
    ORDER BY gr.modified 
"""
