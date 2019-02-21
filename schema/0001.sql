create table if not exists concert_master (
    conc_id     SERIAL PRIMARY KEY,
    venue       TEXT,
    event_name  TEXT,
    band_name   TEXT,
    conc_date   TEXT,
    conc_price  TEXT,
    genra       TEXT,
    subgenra    TEXT,
    postcode    TEXT
);

