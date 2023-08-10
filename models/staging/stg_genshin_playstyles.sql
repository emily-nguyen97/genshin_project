{{ config(materialized='view') }}

select 
-- identifiers
    cast(Character as varchar(25)) as char_name,

-- info
    cast(case when Playstyle is not null then Playstyle else null end as varchar(25)) as playstyle,
    cast(Version as float) as abyss_version

from {{ source('staging','playstyles') }}