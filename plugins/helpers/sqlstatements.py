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

    airports_data_insert = ("""(icao, name, iata, latitude, longitude, country, altitude, type, municipality)
                               SELECT icao, 
                                      name,
                                      iata, 
                                      latitude, 
                                      longitude, 
                                      country, 
                                      altitude, 
                                      type, 
                                      municipality 
                               FROM staging_airports
                               ON CONFLICT (icao) DO NOTHING
    """)

    flight_data_insert = ("""(flight_id, icao24, firstSeenTime, estdepartureairport, lastSeenTime, estarrivalairport, callsign)
                              SELECT DISTINCT md5(f.icao24 || f.firstSeenTime) flight_id,
                                              f.icao24,
                                              f.firstSeenTime,
                                              f.estdepartureairport,
                                              f.lastSeenTime,
                                              f.estarrivalairport,
                                              f.callsign
                                              FROM (SELECT TIMESTAMP 'epoch' + firstseen * interval '1 second' AS firstSeenTime, 
                                                    TIMESTAMP 'epoch' + lastseen * interval '1 second' AS lastSeenTime, *
                                                    FROM staging_flights) f
                                              ON CONFLICT (flight_id) DO NOTHING
    """)

    time_firstseen_insert = ("""(seen_time, hour, day, week, month, year, weekday)
                                SELECT firstSeenTime,
                                       extract(hour from firstSeenTime), 
                                       extract(day from firstSeenTime), 
                                       extract(week from firstSeenTime), 
                                       extract(month from firstSeenTime), 
                                       extract(year from firstSeenTime), 
                                       extract(dow from firstSeenTime)
                                FROM (SELECT TIMESTAMP 'epoch' + firstseen * interval '1 second' AS firstSeenTime, *
                                FROM staging_flights) f
                                ON CONFLICT (seen_time) DO NOTHING
    """)

    time_lastseen_insert = ("""(seen_time, hour, day, week, month, year, weekday)
                                SELECT lastSeenTime,
                                       extract(hour from lastSeenTime), 
                                       extract(day from lastSeenTime), 
                                       extract(week from lastSeenTime), 
                                       extract(month from lastSeenTime), 
                                       extract(year from lastSeenTime), 
                                       extract(dow from lastSeenTime)
                                FROM (SELECT TIMESTAMP 'epoch' + lastSeen * interval '1 second' AS lastSeenTime, *
                                FROM staging_flights) f
                                ON CONFLICT (seen_time) DO NOTHING
    """)