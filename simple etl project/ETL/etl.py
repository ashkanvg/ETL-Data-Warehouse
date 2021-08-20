import psycopg2 as pg
import datetime

#connect to databases
    # library
libraryConnection = pg.connect("host=127.0.0.1 dbname=library user=postgres password=postgres")
libraryCursor = libraryConnection.cursor()

    # warehouse
warehouseLibraryConnection = pg.connect("host=127.0.0.1 dbname=warehouse user=postgres password=postgres")
warehouseLibraryCursor = warehouseLibraryConnection.cursor()

#get source database tables and their primery keys (hit by github(link in pdf))
libraryCursor.execute("""
    SELECT c.table_name, c.column_name
    FROM information_schema.table_constraints tc 
        JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
        JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
        AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = c.table_name
    ORDER BY c.table_name, c.ordinal_position ASC
    """)

src_tables = libraryCursor.fetchall()
# for x in src_tables : x[0] = table_name  x[1] = primary_key


names = []
tables = []
for x in src_tables:
    if not x[0] in names:
        tables.append(x)    #tables
        names.append(x[0])  #tables_name

#refactor record
def refactor(record):
    for y in record:
        if y is None: #if value none
            i = record.index(y)
            record = list(record)
            record[i] = ''
            record = tuple(record)
        if isinstance(y, datetime.date): #if value date
            i = record.index(y)
            record = list(record)
            record[i] = '%s' % (str(y))
            record = tuple(record)
    return record
    

#tables -->list of table(table name,primary key)
for table in tables:
 
    table_name = table[0] #copy of table_name
    primary_key = table[1] #copy of primary_key

    #update old records
    if table_name[0:7] == "UPDATED" :
        libraryCursor.execute("SELECT * FROM %s" % (table_name))
        libraryQuery = libraryCursor.fetchall()

        updated = []

        #libraryQuery--> records in table
        for record in libraryQuery:
            record = refactor(record) 

            # want insert in updated if not in
            if not record[0] in updated: 
                warehouseLibraryCursor.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name[8:], primary_key, record[0]))
                libraryCursor.execute("SELECT * FROM %s WHERE %s = %s ;" % (table_name[8:], primary_key, record[0]))
                query = libraryCursor.fetchall()
                refactor(query)

                # insert refactored select 
                warehouseLibraryCursor.execute("INSERT INTO %s VALUES %s;" % (table_name[8:], query))
                updated.append(record[0])

            warehouseLibraryCursor.execute("INSERT INTO %s VALUES %s;" % (table_name, record))
            warehouseLibraryConnection.commit()

            #clear updated table from sourse database
            libraryCursor.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name, primary_key, record[0]))
            libraryConnection.commit()
            
    #delete records
    elif table_name[0:7] == "DELETED":
        libraryCursor.execute("SELECT * FROM %s" % (table_name))
        libraryQuery = libraryCursor.fetchall()

        # no need to check because we have delete not update
        # so we get all records from libraryQuery which table_name is DELETED
        for record in libraryQuery:

            record = refactor(record)

            warehouseLibraryCursor.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name[8:], primary_key, record[0]))
            warehouseLibraryCursor.execute("INSERT INTO %s VALUES %s;" % (table_name, record))
            warehouseLibraryConnection.commit()

            #clear DELETE table from sourse database
            libraryCursor.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name, primary_key, record[0]))
            libraryConnection.commit()
        
    #insert new records
    else :
        warehouseLibraryCursor.execute("SELECT MAX(TRANSFER) FROM %s" % (table_name))
        last_transfer = warehouseLibraryCursor.fetchone()
        last_transfer = str(last_transfer[0])
        if last_transfer == 'None':
            last_transfer = str(datetime.datetime.now())


        # select every things after etl run 
        libraryCursor.execute("SELECT * FROM %s WHERE CREATE > '%s' " % (table_name, last_transfer))
        libraryQuery = libraryCursor.fetchall()

        for record in libraryQuery:
            record = refactor(record)

            warehouseLibraryCursor.execute("INSERT INTO %s VALUES %s;" % (table_name, record))
            warehouseLibraryConnection.commit()


#close connections
warehouseLibraryConnection.close()
libraryConnection.close()
