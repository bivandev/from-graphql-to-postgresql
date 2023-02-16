CREATE TABLE missions (
  mission_id VARCHAR(255) PRIMARY KEY,
  mission_name VARCHAR(255) NOT NULL,
  launch_date_utc VARCHAR(255),
  rocket_id VARCHAR(255),
  CONSTRAINT fk_rocket_id
    FOREIGN KEY (rocket_id)
    REFERENCES rockets(rocket_id)
);

CREATE TABLE launches (
  launch_id VARCHAR(255) PRIMARY KEY,
  mission_id VARCHAR(255) NOT NULL,
  launch_date_utc VARCHAR(255),
  launch_success BOOLEAN,
  details TEXT,
  CONSTRAINT fk_mission_id
    FOREIGN KEY (mission_id)
    REFERENCES missions(mission_id)
);

CREATE TABLE rockets (
  rocket_id VARCHAR(255) PRIMARY KEY,
  rocket_name VARCHAR(255) NOT NULL,
  rocket_type VARCHAR(255)
);