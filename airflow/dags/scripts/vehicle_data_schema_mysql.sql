use traffic_data;
CREATE TABLE IF NOT EXISTS vehicles (
    uid varchar(25) PRIMARY KEY NOT NULL,
    veh_type varchar(25) NOT NULL,
    traveled_distance DOUBLE DEFAULT NULL,
    avg_speed DOUBLE DEFAULT NULL,
    track_id INT DEFAULT NULL,
);