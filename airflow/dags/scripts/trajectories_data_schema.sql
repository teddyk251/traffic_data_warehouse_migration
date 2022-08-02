CREATE TABLE IF NOT EXISTS trajectories
(
    "id" SERIAL NOT NULL,
    "uid" TEXT NOT NULL,
    "lat" FLOAT NOT NULL,
    "lon" FLOAT DEFAULT NULL,
    "speed" FLOAT DEFAULT NULL,
    "lon_acc" FLOAT DEFAULT NULL,
    "lat_acc" FLOAT DEFAULT NULL,
    "time" FLOAT DEFAULT NULL,
    PRIMARY KEY ("id"),
    CONSTRAINT fk_vehicles
        FOREIGN KEY("uid") 
            REFERENCES vehicles(unique_id)
            ON DELETE CASCADE
    
);