{{ config(mateialzied='view')}}

-- with source_data as (
--     select type, count(*) as total, sum(avg_speed) as total_avg_speed, avg(avg_speed) as avg_speed_per_type, (sum(traveled_d) / 1000) as total_traveled_d_km from vehicles group by "type"
-- )

-- select * from source_data


with 
    vehicles as (select * from {{source('traffic_data', 'vehicles')}}),

    vehicle_distribution as (
        select 
            vehicles.type,
            count(*) as total,
            sum(vehicles.avg_speed) as total_avg_speed,
            avg(vehicles.avg_speed) as avg_speed_per_type,
            (sum(vehicles.traveled_d) / 1000 ) as total_traveled_d_km

        from
            vehicles
        
        group by vehicles.type
        
    )
    select * from vehicle_distribution