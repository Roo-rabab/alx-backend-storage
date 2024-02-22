-- Create a temporary table to store the split and formed attributes
CREATE TEMPORARY TABLE IF NOT EXISTS temp_band_info AS (
    SELECT
        band_name,
        SUBSTRING_INDEX(SUBSTRING_INDEX(attributes, 'formed:', -1), ',', 1) AS formed,
        SUBSTRING_INDEX(SUBSTRING_INDEX(attributes, 'split:', -1), ',', 1) AS split
    FROM
        bands
);

-- Calculate the lifespan in years until 2022
SELECT
    band_name,
    IF(split = 0, 0, IF(split = -1, 2022 - formed, split - formed)) AS lifespan
FROM
    temp_band_info
WHERE
    style = 'Glam rock'
ORDER BY
    lifespan DESC;
