class SqlQueries:
    aircraft_data_insert = ("""SELECT DISTINCT sad.icao24, 
                                               sad.registration, 
                                               sad.operator, 
                                               sad.operatoricao, 
                                               sad.owner, 
                                               sad.manufacturericao, 
                                               sad.manufacturername, 
                                               sad.typecode, 
                                               sad.model, 
                                               sad.serialnumber, 
                                               sat.aircraftdescription, 
                                               sat.wtc, 
                                               sat.enginetype, 
                                               CAST(sat.enginecount AS INTEGER) 
                               FROM staging_aircraft_database AS sad 
                               LEFT JOIN staging_aircraft_types AS sat 
                               ON sad.typecode=sat.designator
                               ON CONFLICT (icao24) DO NOTHING""")

    flight_data_insert = ("""(icao24, firstSeenTime, estdepartureairport, lastSeenTime, estarrivalairport, callsign)
                             SELECT DISTINCT f.icao24,
                                             f.firstSeenTime,
                                             f.estdepartureairport,
                                             f.lastSeenTime,
                                             f.estarrivalairport,
                                             f.callsign
                                             FROM (SELECT TIMESTAMP 'epoch' + firstseen * interval '1 second' AS firstSeenTime, 
                                                          TIMESTAMP 'epoch' + lastseen * interval '1 second' AS lastSeenTime, *
                                                   FROM staging_flights) f
    ;""")