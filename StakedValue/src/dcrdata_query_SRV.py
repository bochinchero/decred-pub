
# This script gets data from a local dcrdata instance's postgresql database
# and pulls it back into a csv file. it brings back the following information
# for every ticket - the query ignores tickets that have expired or
# have been missed but haven't been spent.
#   - Purchase Height
#   - Purchase Date/Time
#   - Purchase Price
#   - Purchase Height Ticket Pool Size
#   - Purchase Height Ticket Pool Value
#   - Voting Height
#   - Voting Date/Time
#   - Voting Reward
#   - Voting Height Ticket Pool Size
#   - Voting Height Ticket Pool Value
#   - Ticket Status in the Pool (0: live, 1: voted, 2: expired 3: missed)

import pandas as pd
import sqlalchemy as sql
import requests
import io


# Create an engine instance
engine = sql.create_engine('postgresql://dcrdata:dcrdata@192.168.56.1:5432/dcrdata')
# Connect to PostgreSQL server
pg_connection = engine.connect()

# Read data from PostgreSQL database query and load into a DataFrame instance

query = """
Select 
	tdb.block_height as p_height,
	date(bdb1.time) as p_date,
	tdb.price as p_ticketprice, 
	sdb1.pool_size as p_poolsize,
	sdb1.pool_val/100000000 as p_poolval,
	tdb.spend_height as v_height,
	date(bdb2.time) as v_date,
	vdb.vote_reward as v_reward,
	sdb2.pool_size as v_poolsize,
	sdb2.pool_val/10000000 as v_poolval,
	tdb.pool_status

from public.tickets as tdb
left join public.blocks as bdb1 
	on tdb.block_height = bdb1.height 
left join public.stats as sdb1 
	on tdb.block_height = sdb1.height
left join public.blocks as bdb2 
	on tdb.spend_height = bdb2.height
left join public.stats as sdb2 
	on tdb.spend_height = sdb2.height
left join public.votes as vdb 
	on tdb.id = vdb.ticket_tx_db_id

where (((pool_status < 2) OR ((pool_status > 1) AND (spend_height is not null))) AND tdb.block_height > 2966)
order by tdb.block_height asc
"""
# execute the query and read the data into a pandas data frame
raw_ticket_data = pd.read_sql(query, pg_connection)

# close pg connection
pg_connection.close();

# this prints the latest data in the console, we can verify that the blocks are updated, etc.
print('Ticket Data Latest:')
print(raw_ticket_data)
print(raw_ticket_data.dtypes)

# Save CSVs

raw_ticket_data.to_csv('data/dcrdata_raw_tickets.csv')
