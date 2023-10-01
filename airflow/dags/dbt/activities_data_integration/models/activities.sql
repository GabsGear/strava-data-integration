
SELECT 

    NAME                                                     AS activity_name,
    DISTANCE/1000                                            AS distance_km,
    MOVING_TIME                                              AS moving_time,
    ELAPSED_TIME                                             AS total_activity_time,
    TOTAL_ELEVATION_GAIN                                     AS accumulated_elevation,
    TYPE                                                     AS activity_type,
    CAST(START_DATE_LOCAL AS DATE)                       AS activity_started_at,
    LOCATION_COUNTRY                                         AS country,
    ACHIEVEMENT_COUNT                                        AS strava_achievements,
    KUDOS_COUNT                                              AS strava_kudos,
    CASE WHEN GEAR_ID = 'b12622486'  THEN 'Gravel - Gaia'
         WHEN GEAR_ID = 'b9940418'   THEN 'MTB - Chica'
         WHEN GEAR_ID = 'b8585841'   THEN 'ROAD - Caloi 10'
         WHEN GEAR_ID = 'b8532069'   THEN 'MTB - Jolene'
        ELSE 'Mizzuno Wave Verdin'
        END                                                   AS equipement,
    AVERAGE_SPEED                                             AS average_speed,
    MAX_SPEED                                                 AS max_speed,
    AVERAGE_CADENCE                                           AS average_cadence,
    AVERAGE_HEARTRATE                                         AS average_heartrate,
    MAX_HEARTRATE                                             AS max_heartrate,
    ELEV_HIGH                                                 AS high_elevation,
    ELEV_LOW                                                  AS elev_low,
    PR_COUNT                                                  AS personal_records,
    AVERAGE_TEMP                                              AS average_temperature,
    AVERAGE_WATTS                                             AS average_watts

FROM {{ ref('stg_strava_activities') }}
