-- Tables
CREATE TABLE IF NOT EXISTS railway_station (
    station_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS train (
    train_no SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    src_station_id INT NOT NULL,
    dest_station_id INT NOT NULL,
    FOREIGN KEY(src_station_id) REFERENCES railway_station(station_id) ON DELETE CASCADE,
    FOREIGN KEY(dest_station_id) REFERENCES railway_station(station_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email_id VARCHAR(100) NOT NULL UNIQUE,
  	age INT NOT NULL CHECK(age > 0),
    mobile_no VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS ticket (
    pnr UUID DEFAULT UUID_GENERATE_V4() PRIMARY KEY,
    -- The actual cost for the passenger for its journey
    src_station_id INT NOT NULL,
    dest_station_id INT NOT NULL,
    train_no INT NOT NULL,
    user_id INT NOT NULL,
    date DATE NOT NULL CHECK(date - CURRENT_DATE >= 0),
    no_of_seats INT NOT NULL CHECK(no_of_seats > 0),
    -- booking_status BOOKING_STATUS DEFAULT 'Waiting',
    FOREIGN KEY(src_station_id) REFERENCES railway_station(station_id) ON DELETE CASCADE,
    FOREIGN KEY(dest_station_id) REFERENCES railway_station(station_id) ON DELETE CASCADE,
    FOREIGN KEY(train_no) REFERENCES train(train_no) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS schedule (
    sch_id SERIAL PRIMARY KEY,

    avail_seats INT NOT NULL CHECK(avail_seats >= 0),
    -- Train Number to which the schedule is assigned
    train_no INT NOT NULL,
    -- Station from which the train departs
    curr_station_id INT NOT NULL,
    -- Station to which the train arrives
    -- For the destination station, this value can be NULL
    next_station_id INT,
    -- (Day of Journey, Time) at which the train will arrive at the current station
    arr_time timestamp NOT NULL,
    -- (Day of Journey, Time) at which the train will depart from the current station
    dep_time timestamp NOT NULL CHECK(arr_time <= dep_time),
    -- Fare from the source station of the train till the current_station
    fare NUMERIC(7, 2) NOT NULL CHECK(fare >= 0),
    -- Time by which the train will be delayed at the current station
    date DATE NOT NULL,
    FOREIGN KEY(train_no) REFERENCES train(train_no) ON DELETE CASCADE,
    FOREIGN KEY(curr_station_id) REFERENCES railway_station(station_id) ON DELETE CASCADE,
    FOREIGN KEY(next_station_id) REFERENCES railway_station(station_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION find_trains_btw_stations(
  in_id INTEGER,
  out_id INTEGER,
  d DATE
) RETURNS TABLE (
  train_no INTEGER,
  name VARCHAR(100),
  src_station VARCHAR(100),
  dest_station VARCHAR(100)
) AS $$
BEGIN
  RETURN QUERY
    SELECT
      t.train_no,
      t.name,
      src.name AS src_station,
      dest.name AS dest_station
    FROM
      train t
      JOIN railway_station src ON t.src_station_id = src.station_id
      JOIN railway_station dest ON t.dest_station_id = dest.station_id
      JOIN schedule s1 ON t.train_no = s1.train_no
      JOIN schedule s2 ON t.train_no = s2.train_no
    WHERE
      s1.curr_station_id = in_id AND
      s2.next_station_id = out_id AND
      s1.arr_time <= s2.dep_time AND
      s1.date = d AND
      s2.date = d
    ORDER BY
      t.train_no;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_intermediate_stations(train_num INT, src_station_id INT, dest_station_id INT) 
RETURNS TABLE(station_name VARCHAR(100), arrival_time TIMESTAMP, departure_time TIMESTAMP) AS 
$$ 
DECLARE
	t1 timestamp;
	t2 timestamp;
BEGIN 
	SELECT arr_time INTO t1 FROM schedule WHERE train_no = train_num AND curr_station_id = src_station_id;
	SELECT arr_time INTO t2 FROM schedule WHERE train_no = train_num AND next_station_id = dest_station_id;
	
    RETURN QUERY 
        SELECT rs.name, s.arr_time, s.dep_time
        FROM schedule s
        JOIN railway_station rs ON s.curr_station_id = rs.station_id
        WHERE s.train_no = train_num AND s.curr_station_id != src_station_id AND s.curr_station_id != dest_station_id 
        AND s.arr_time > t1 AND s.arr_time <= t2;
END; 
$$ 
LANGUAGE PLPGSQL;





CREATE OR REPLACE FUNCTION get_min_avail_seats(train_num INT, src_id INT, dest_id INT, journey_date DATE) 
RETURNS INT AS $$
DECLARE 
    min_avail_seats INT := 9999;
    c_station_id INT := src_id;
    n_station_id INT;
	cur_avail_seats INT;
BEGIN
    WHILE c_station_id <> dest_id LOOP
        -- Get next station id and available seats
        SELECT next_station_id, avail_seats 
        INTO n_station_id, cur_avail_seats
        FROM schedule
        WHERE train_no = $1 AND curr_station_id = c_station_id AND date = journey_date;
        
        -- Update minimum available seats
        IF cur_avail_seats < min_avail_seats THEN
            min_avail_seats := cur_avail_seats;
        END IF;
        
        -- Move to next station
        c_station_id := n_station_id;
    END LOOP;
    
    RETURN min_avail_seats;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION book_seat(user_id INT, train_num INT, src_id INT, dest_id INT, journey_date DATE, num_seats INT) 
RETURNS INT
AS $$
DECLARE 
    c_station_id INT := src_id;
    n_station_id INT;
BEGIN
    WHILE c_station_id <> dest_id LOOP
        -- Get next station id and available seats
        SELECT next_station_id
        INTO n_station_id
        FROM schedule
        WHERE train_no = $2 AND curr_station_id = c_station_id AND date = journey_date;
        
        -- Update minimum available seats
		UPDATE schedule set avail_seats = avail_seats - $6
		WHERE train_no = $2 AND curr_station_id = c_station_id AND date = journey_date;
        -- Move to next station
        c_station_id := n_station_id;
    END LOOP;

	-- now create a entry in ticket table for this user 
	INSERT INTO ticket (user_id, train_no, src_station_id, dest_station_id, date, no_of_seats) 
    VALUES (user_id, train_num, src_id, dest_id, journey_date, num_seats);

    RETURN 69;
END;
$$ LANGUAGE plpgsql;

CREATE INDEX ticket_src_station_id ON ticket USING HASH(src_station_id);
CREATE INDEX ticket_dest_station_id ON ticket USING HASH(dest_station_id);
CREATE INDEX ticket_train_no ON ticket USING HASH(train_no);
CREATE INDEX ticket_user_id ON ticket USING HASH(user_id);
CREATE INDEX ticket_pid ON ticket USING HASH(pid);
CREATE INDEX ticket_seat_id ON ticket USING HASH(seat_id);
CREATE INDEX ticket_date ON ticket USING BTREE(date);
CREATE INDEX ticket_seat_type ON ticket USING HASH(seat_type);


CREATE INDEX train_src_station_id ON train USING HASH(src_station_id);
CREATE INDEX train_dest_station_id ON train USING HASH(dest_station_id);


CREATE INDEX schedule_train_no ON schedule USING HASH(train_no);
CREATE INDEX schedule_curr_station_id ON schedule USING HASH(curr_station_id);
CREATE INDEX schedule_next_station_id ON schedule USING HASH(next_station_id);


CREATE OR REPLACE FUNCTION update_avail_seats()
RETURNS TRIGGER AS $$
DECLARE 
    c_station_id INT := OLD.src_station_id;
    dest_id INT := OLD.dest_station_id;
    n_station_id INT;
    d DATE := OLD.date;
BEGIN
  WHILE c_station_id <> dest_id LOOP

    SELECT next_station_id
    INTO n_station_id
    FROM schedule
    WHERE train_no = OLD.train_no AND curr_station_id = c_station_id AND date = d;
        

    UPDATE schedule
    SET avail_seats = (avail_seats + OLD.no_of_seats)
    WHERE train_no = OLD.train_no
      AND date = d
      AND curr_station_id = c_station_id;

    c_station_id := n_station_id;

  END LOOP;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER cancel_ticket_trigger
AFTER DELETE ON ticket
FOR EACH ROW
EXECUTE FUNCTION update_avail_seats();