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