WITH sorted_cities AS (
    SELECT
        c1.name AS from_city,
        c2.name AS target_city,
        conn.distance
    FROM
        connections conn
    JOIN
        cities c1 ON conn.from_city_id = c1.id
    JOIN
        cities c2 ON conn.to_city_id = c2.id
    WHERE
        c1.name = 'Factoria' -- Замените на конкретное название города
    UNION ALL
    SELECT
        c2.name AS from_city,
        c1.name AS to_city,
        conn.distance
    FROM
        connections conn
    JOIN
        cities c1 ON conn.from_city_id = c1.id
    JOIN
        cities c2 ON conn.to_city_id = c2.id
    WHERE
        c2.name = 'Factoria' -- Замените на конкретное название города
    ORDER BY
        target_city
    LIMIT 2
),
diff AS (
    SELECT 
        from_city AS departure_city,
        LAG(target_city)  OVER (ORDER BY target_city) AS first_target_city,
        target_city AS second_target_city,
        ABS(distance - LAG(distance) OVER (ORDER BY target_city)) AS distance_diff
    FROM 
        sorted_cities
)
SELECT 
    departure_city,
    first_target_city,
    second_target_city,
    distance_diff
FROM
    diff
WHERE
    distance_diff IS NOT NULL;