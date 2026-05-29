create table jobs (
    id serial primary key, 
    title varchar(255) not null,
    company varchar(255) not null,
    location varchar(255) not null,
    job_type varchar(255),
    salary varchar(255),
    date_posted date,
    link varchar(255) not null,
    scraped_at timestamp default current_timestamp
);