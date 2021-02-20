CREATE TABLE staging_aircraft_types(
    aircraftdescription VARCHAR(256),
    description         VARCHAR(256),
    designator          VARCHAR(256),
    enginecount         VARCHAR(256),
    enginetype          VARCHAR(256),
    manufacturercode    VARCHAR(256),
    modelfullname       VARCHAR(256),
    wtc                 VARCHAR(256)
);

CREATE TABLE staging_aircraft_database(
    icao24              VARCHAR(256),
    registration        VARCHAR(256),
    manufacturericao    VARCHAR(256),
    manufacturername    VARCHAR(256),
    model               VARCHAR(256),
    typecode            VARCHAR(256),
    serialnumber        VARCHAR(256),
    linenumber          VARCHAR(256),
    icaoaircrafttype    VARCHAR(256),
    operator            VARCHAR(256),
    operatorcallsign    VARCHAR(256),
    operatoricao        VARCHAR(256),
    operatoriata        VARCHAR(256),
    owner               VARCHAR(256),
    testreg             VARCHAR(256),
    registered          VARCHAR(256),
    reguntil            VARCHAR(256),
    status              VARCHAR(256),
    built               VARCHAR(256),
    firstflightdate     VARCHAR(256),
    seatconfiguration   VARCHAR(256),
    engines             VARCHAR(256),
    modes               BOOLEAN,
    adsb                BOOLEAN,
    acars               BOOLEAN,
    notes               VARCHAR(256),
    categoryDescription VARCHAR(256)
);

CREATE TABLE staging_airports(
    name            VARCHAR(256),
    iata            VARCHAR(256),
    icao            VARCHAR(256),
    latitude        NUMERIC(18,0),
    longitude       NUMERIC(18,0),
    country         VARCHAR(256),
    altitude        NUMERIC(18,0),
    type            VARCHAR(256),
    municipality    VARCHAR(256)
);

CREATE TABLE staging_flights(
    icao24              VARCHAR(256),
    firstSeen           INT,
    estDepartureAirport VARCHAR(256),
    lastSeen            INT,
    estArrivalAirport   VARCHAR(256),
    callsign            VARCHAR(256)
);

CREATE TABLE dim_aircrafts(
    icao24              VARCHAR(256) PRIMARY KEY,
    registration        VARCHAR(256),
    operator            VARCHAR(256),
    operatoricao        VARCHAR(256),
    owner               VARCHAR(256),
    manufacturericao    VARCHAR(256),
    manufacturername    VARCHAR(256),
    typecode            VARCHAR(256),
    model               VARCHAR(256),
    serialnumber        VARCHAR(256),
    aircraftdescription VARCHAR(256),
    wtc                 VARCHAR(256),
    enginetype          VARCHAR(256),
    enginecount         INT
);

CREATE TABLE dim_time (
    seen_time   TIMESTAMP    NOT NULL   PRIMARY KEY,
    hour         INT         NOT NULL,
    day          INT         NOT NULL,
    week         INT         NOT NULL,
    month        INT         NOT NULL,
    year         INT         NOT NULL,
    weekday      INT         NOT NULL
);

CREATE TABLE dim_airports (
    icao            VARCHAR(256)    NOT NULL   PRIMARY KEY,
    name            VARCHAR(256),
    iata            VARCHAR(256),
    latitude        NUMERIC(18,0),
    longitude       NUMERIC(18,0),
    country         VARCHAR(256),
    altitude        NUMERIC(18,0),
    type            VARCHAR(256),
    municipality    VARCHAR(256)
);

CREATE TABLE fact_flights(
    flight_id           VARCHAR(32)     NOT NULL    PRIMARY KEY,
    icao24              VARCHAR(256)    NOT NULL,
    firstSeenTime       TIMESTAMP,
    estDepartureAirport VARCHAR(256),
    lastSeenTime        TIMESTAMP,
    estArrivalAirport   VARCHAR(256),
    callsign            VARCHAR(256)
);