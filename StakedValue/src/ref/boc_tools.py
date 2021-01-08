# bochinchero on chain tools

import pandas as pd
import coinmetrics
import cm_data_converter as cmdc # h/t Permabull Nino
import sqlalchemy as sql

# Coinmetrics data manipulation

def cm_getmetric(asset,metric,date_start,date_end):
    # this function grabs the metric for asset within the specified date range,
    # removes the timezone, sets the date as an index and changes the column name to
    # the name of the metric

    # Initialize a reference object, in this case `cm` for the Community API
    cm = coinmetrics.Community()

    # grab data from CM - h/t permabull nino
    data = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, metric, date_start, date_end))

    # remove timezone from date
    data['date'] = data['date'].dt.tz_convert(None)
    # rename columns to date and metric
    output = data.rename(columns={"date": "date", "data": metric})

    # purge
    del data
    # return output data
    return output

# Realised Cap Calculation

def calculate_realcap(utxo_set,price):
    # This function calculates realised value based on 2 data frames that need the following structure
    # utxo_set: fund_date, spend_date, value
    # price: date, price
    # the function output will be as date, realcap

    # merge price into utxo set based on fund_date
    utxo_set = utxo_set.merge(price,left_on='fund_date',right_on='date',how='left')

    # calculate value on utox fund date in fiat/btc
    utxo_set['fund_value']=utxo_set.value*utxo_set.price

    # split out utxo_set into additions and subtractions arrays
    adds = utxo_set[['fund_date','fund_value']].copy()
    subs = utxo_set[['spend_date', 'fund_value']].copy()

    # rename date columns
    adds = adds.rename(columns={"fund_date": "date", "fund_value": "adds_value"})
    subs = subs.rename(columns={"spend_date": "date", "fund_value": "subs_value"})

    # create aggregate version of both arrays based on the daily sums.
    adds_agg = adds.set_index('date').groupby(pd.Grouper(freq='D')).agg({'adds_value': 'sum'})
    subs_agg = subs.set_index('date').groupby(pd.Grouper(freq='D')).agg({'subs_value': 'sum'})

    # merge adds and subs into a single array
    realcap = adds_agg.merge(subs_agg,left_on='date',right_on='date',how='left')

    # purge
    del adds_agg, subs_agg, adds, subs, utxo_set

    # calculate net flows
    realcap['net'] = realcap.adds_value - realcap.subs_value

    # calculate realised cap
    realcap['realcap'] = realcap.net.cumsum()

    # drop temp calculation columns
    realcap = realcap.drop(columns=['adds_value', 'subs_value', 'net'])

    # return RV as the output of the function
    return realcap

# dcrdata query functions

def dcrdata_query(query):
    # this function queries data from a remote dcrdata instance
    # the connection string has been defined as the server I use
    # input argument is a query as a text string, other functions
    # are defined below for specific queries
    # Create an engine instance
    engine = sql.create_engine('postgresql://-redacted-@45.63.41.247:5432/dcrdata')
    # Connect to PostgreSQL server
    pg_connection = engine.connect()
    # Read data from PostgreSQL database query and load into a DataFrame instance
    output = pd.read_sql(query, pg_connection)
    # close pg connection
    pg_connection.close();

    return output

def dcrdata_pgquery_utxo_tickets():
    # this function uses the dcrdata_query func to obtain all of the ticket data for realised value
    #   - Fund Date
    #   - Spend Date
    #   - Value

    query = """
    Select 
    	date(bdb1.time) as fund_date,
    	date(bdb2.time) as spend_date,
    	tdb.price as value
    	
    from public.tickets as tdb
    left join public.blocks as bdb1 
    	on tdb.block_height = bdb1.height 
    left join public.blocks as bdb2 
    	on tdb.spend_height = bdb2.height

    order by tdb.id asc
    """
    # execute query on dcrdata pgdb
    output = dcrdata_query(query)
    # fix date formats
    output['fund_date']=pd.to_datetime(output.fund_date)
    output['spend_date']=pd.to_datetime(output.spend_date)
    return output


def dcrdata_pgquery_poolval():
    # this function uses the dcrdata_query func to obtain ticket pool value
    #   - date
    #   - poolval

    query = """
    Select 
    	date(bdb.time) as date,
    	avg(sdb.pool_val/100000000) as poolval
    	
    from public.stats as sdb
    left join public.blocks as bdb
    	on sdb.height = bdb.height 
	group by date
    order by date asc
    """
    # execute query on dcrdata pgdb
    output = dcrdata_query(query)
    # fix date formats
    output['date'] = pd.to_datetime(output.date)
    return output
