aircraft_data_insert = ("""INSERT INTO dim_aircrafts (icao24, 
                                                      registration, 
                                                      operator, 
                                                      operatoricao, 
                                                      owner, 
                                                      manufacturericao, 
                                                      manufacturername, 
                                                      typecode, 
                                                      model, 
                                                      serialnumber, 
                                                      aircraftdescription, 
                                                      wtc, 
                                                      enginetype, 
                                                      enginecount) 
                           SELECT DISTINCT sad.icao24, 
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
                                           sat.enginecount 
                           FROM staging_aircraft_database AS sad 
                           LEFT JOIN staging_aircraft_types AS sat 
                           ON sad.typecode=sat.designator
;""")