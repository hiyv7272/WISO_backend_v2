-- create database
-- create database WISOv2 character set utf8mb4 collate utf8mb4_general_ci;

-- delete database
-- DROP DATABASE IF EXISTS WISOv2;

-- Status table
INSERT INTO Status(status) VALUES('예약완료');

INSERT INTO Status(status) VALUES('예약취소');

INSERT INTO Status(status) VALUES('결제완료');

INSERT INTO Status(status) VALUES('결제취소');


-- ServiceStartingTimes table
INSERT INTO ServiceStartingTimes(starting_time) VALUES('오전9시');

INSERT INTO ServiceStartingTimes(starting_time) VALUES('오전10시');

INSERT INTO ServiceStartingTimes(starting_time) VALUES('오후2시');


-- ServiceDurations table
INSERT INTO ServiceDurations(service_duration) VALUES('3시간');

INSERT INTO ServiceDurations(service_duration) VALUES('4시간');

INSERT INTO ServiceDurations(service_duration) VALUES('8시간');


-- ServiceDayOfWeeks table
INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('월');

INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('화');

INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('수');

INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('목');

INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('금');

INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('토');

INSERT INTO ServiceDayOfWeeks(service_day_of_week) VALUES('일');


-- ReserveCycles table
INSERT INTO ReserveCycles(reserve_cycle) VALUES('1회');

INSERT INTO ReserveCycles(reserve_cycle) VALUES('매주');

INSERT INTO ReserveCycles(reserve_cycle) VALUES('2주');

INSERT INTO ReserveCycles(reserve_cycle) VALUES('4주');


-- ServiceDurations_ServiceStartingTimes table
INSERT INTO ServiceDurations_ServiceStartingTimes(service_durations_id, starting_times_id) VALUES('1','2');

INSERT INTO ServiceDurations_ServiceStartingTimes(service_durations_id, starting_times_id) VALUES('1','3');

INSERT INTO ServiceDurations_ServiceStartingTimes(service_durations_id, starting_times_id) VALUES('2','1');

INSERT INTO ServiceDurations_ServiceStartingTimes(service_durations_id, starting_times_id) VALUES('2','2');

INSERT INTO ServiceDurations_ServiceStartingTimes(service_durations_id, starting_times_id) VALUES('3','1');


-- Move_categories table
INSERT INTO Movecategories(name) VALUES('가정이사');

INSERT INTO Movecategories(name) VALUES('소형이사');

INSERT INTO Movecategories(name) VALUES('사무실이사');