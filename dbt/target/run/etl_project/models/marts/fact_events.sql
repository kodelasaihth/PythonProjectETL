
  
    

create or replace transient table ANALYTICS_DB.PUBLIC.fact_events
    
    
    
    as (SELECT
    user_id,
    first_name,
    last_name,
    email,
    country,
    job_title,

    DATEDIFF(year, birth_date, CURRENT_DATE) AS age,

    salary,

    CASE
        WHEN salary > 50000 THEN 'HIGH'
        WHEN salary > 20000 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS salary_band,

    registration_ts

FROM ANALYTICS_DB.PUBLIC.stg_events
    )
;


  