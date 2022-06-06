create table candidates_status_transitions (
    candidate_id serial PRIMARY KEY,
    hired_timestamp TIMESTAMPTZ DEFAULT NULL,
    invited_timestamp TIMESTAMPTZ DEFAULT NULL,
    shortlisted_timestamp TIMESTAMPTZ DEFAULT NULL,
    first_response_timestamp TIMESTAMPTZ DEFAULT NULL
);

insert into candidates_status_transitions (candidate_id, hired_timestamp) 
select generate_series(1, 10e6) as id,
    timestamp '2020-01-01 00:00:00' + random() * (timestamp '2020-05-01 00:00:00' - timestamp '2020-01-01 00:00:00') as hire_date;

update candidates_status_transitions SET invited_timestamp = (timestamp '2020-05-01 00:00:00' + random() * (timestamp '2020-10-01 00:00:00' - timestamp '2020-05-01 00:00:00'))
    WHERE MOD(candidate_id, 2) = 0;

update candidates_status_transitions SET shortlisted_timestamp = (timestamp '2020-06-01 00:00:00' + random() * (timestamp '2020-11-01 00:00:00' - timestamp '2020-06-01 00:00:00'))
    WHERE MOD(candidate_id, 3) = 0;