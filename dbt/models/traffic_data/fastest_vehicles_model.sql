{{ config(materialzied='view')}}

with 
    vehicles as (select * from {{source('traffic_data', 'vehicles')}}),
    trajectories as (select * from {{source('traffic_data', 'trajectories')}}),

    fast_vehicles as (
        select 
            vehicles.type,
            vehicles.traveled_d,
            vehicles.avg_speed,
            trajectories.*

        from
            trajectories
                inner join vehicles on trajectories.uid = vehicles.uid
        where
            vehicles.avg_speed > 40
        
    )
    select * from fast_vehicles