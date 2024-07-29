WITH sorted_cities AS (
    SELECT 
        c1.name as city,
        c2.name as target_city,
        d.distance
    FROM 
        connections d
    JOIN 
        cities c1 ON d.from_city_id = c1.id
    JOIN 
        cities c2 ON d.to_city_id = c2.id
    WHERE 
        c1.name = 'CITY NAME'
    ORDER BY c2.name
    LIMIT 2
),
diff AS (
    SELECT 
        city AS departure_city,
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