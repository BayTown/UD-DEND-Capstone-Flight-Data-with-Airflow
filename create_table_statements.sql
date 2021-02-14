CREATE TABLE staging_aircraft_types(
    aircraftdescription varchar(256),
    description varchar(256),
    designator varchar(256),
    enginecount varchar(256),
    enginetype varchar(256),
    manufacturercode varchar(256),
    modelfullname varchar(256),
    wtc varchar(256)
);

CREATE TABLE staging_manufacturers(
    code varchar(256),
    name varchar(256)
);

CREATE TABLE staging_aircraft_database(
    icao24 varchar(256),
    registration varchar(256),
    manufacturericao varchar(256),
    manufacturername varchar(256),
    model varchar(256),
    typecode varchar(256),
    serialnumber varchar(256),
    linenumber varchar(256),
    icaoaircrafttype varchar(256),
    operator varchar(256),
    operatorcallsign varchar(256),
    operatoricao varchar(256),
    operatoriata varchar(256),
    owner varchar(256),
    testreg varchar(256),
    registered varchar(256),
    reguntil varchar(256),
    status varchar(256),
    built varchar(256),
    firstflightdate varchar(256),
    seatconfiguration varchar(256),
    engines varchar(256),
    modes boolean,
    adsb boolean,
    acars boolean,
    notes varchar(256),
    categoryDescription varchar(256)
);

CREATE TABLE staging_airports(
    name varchar(256),
    iata varchar(256),
    icao varchar(256),
    latitude numeric(18,0),
    longitude numeric(18,0),
    country varchar(256),
    altitude numeric(18,0),
    type varchar(256),
    municipality varchar(256)
);

CREATE TABLE staging_flights(
    icao24 varchar(256),
    firstSeen integer,
    estDepartureAirport varchar(256),
    lastSeen integer,
    estArrivalAirport varchar(256),
    callsign varchar(256)
);