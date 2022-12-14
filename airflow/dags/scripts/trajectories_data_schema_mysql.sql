use traffic_data;

CREATE TABLE IF NOT EXISTS(
    id SERIAL INT PRIMARY KEY,
    uid varchar(25) NOT NULL,
    lat DOUBLE DEFAULT NULL,
    lon DOUBLE DEFAULT NULL,
    speed DOUBLE DEFAULT NULL,
    lon_acc DOUBLE DEFAULT NULL,
    lat_acc DOUBLE DEFAULT NULL,
    time DOUBLE DEFAULT NULL,
    FOREIGN KEY (uid) REFERENCES vehicles (uid) ON DELETE CASCADE
);