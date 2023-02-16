--Data Showcase 1: Count of launches by mission
SELECT mission_name, COUNT(launch_id) AS launch_count;
FROM Launches;
JOIN Missions ON Launches.mission_id = Missions.mission_id;
GROUP BY mission_name;

--Data Showcase 2: Count of launches by rocket
SELECT rocket_name, COUNT(launch_id) AS launch_count;
FROM Launches;
JOIN Rockets ON Launches.rocket_id = Rockets.rocket_id;
GROUP BY rocket_name;

--Data Showcase 3: Count of launches by name
SELECT launch_name, COUNT(launch_id) AS launch_count;
FROM Launches;
GROUP BY launch_name;