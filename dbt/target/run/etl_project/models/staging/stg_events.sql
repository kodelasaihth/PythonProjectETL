
  create or replace   view ANALYTICS_DB.PUBLIC.stg_events
  
  
  
  
  as (
    SELECT
      $1:id::int                AS user_id,
    $1:first_name::string     AS first_name,
    $1:last_name::string      AS last_name,
    $1:email::string          AS email,
    $1:gender::string         AS gender,
    $1:country::string        AS country,
    $1:title::string          AS job_title,

    TRY_TO_DATE($1:birthdate::string, 'MM/DD/YYYY') AS birth_date,

    TRY_TO_TIMESTAMP($1:registration_dttm::string) AS registration_ts,

    $1:salary::float          AS salary

FROM userdata
  );

