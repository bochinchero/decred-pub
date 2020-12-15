
# This script calculates the realised price, aka the average buy in cost
# for every ticket in the stake pool.
# To run this a CSV file is required that contains all of the ticket data in the following format:
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
# Coinmetrics data is used to calculate the usd and btc prices of dcr on a daily basis
# Props to permabull nino for his script on transforming the CM data to something useful.

import pandas as pd
import os
import coinmetrics
import cm_tools as cmdc
import pandas as pd
from datetime import date
from datetime import datetime
import datetime

# Set date range to fetch and grpah data
date_start  = date(int(2016),int(6),int(15))
date_end    = date(int(2020),int(12),int(15))

## set it so all columns are displayed when printed
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 30)

## -----------------
## COINMETRICS DATA
## -----------------

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"

# grab data from CM - h/t permabull nino
priceUSD  = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_start, date_end))
priceBTC  = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_start, date_end))
CapRealUSD  = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_start, date_end))
CapMrktCurUSD = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_start, date_end))
SplyCur = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_start, date_end))

# remvoe timezone from Date
priceUSD['date']=priceUSD['date'].dt.tz_convert(None)
priceBTC['date']=priceBTC['date'].dt.tz_convert(None)
CapRealUSD['date']=CapRealUSD['date'].dt.tz_convert(None)
CapMrktCurUSD['date']=CapMrktCurUSD['date'].dt.tz_convert(None)
SplyCur['date']=SplyCur['date'].dt.tz_convert(None)

# rename columns to date and priceUSD
priceUSD = priceUSD.rename(columns={"date": "date", "data": "priceUSD"})
priceBTC = priceBTC.rename(columns={"date": "date", "data": "priceBTC"})
CapRealUSD = CapRealUSD.rename(columns={"date": "date", "data": "CapRealUSD"})
CapMrktCurUSD = CapMrktCurUSD.rename(columns={"date": "date", "data": "CapMrktCurUSD"})
SplyCur = SplyCur.rename(columns={"date": "date", "data": "SplyCur"})

# Print PriceUSD in console
print(priceUSD)

## -----------------
## TICKETS DATA
## -----------------

# Read Ticket Data from CSV
path= './data/dcrdata_raw_tickets.csv'
ticket_data= pd.read_csv(path,parse_dates=['v_date','p_date'])

# print read ticket data to console
print(ticket_data)

# prefix p_ to priceUSD to merge - price when purhcasing tickets
priceUSD_p = priceUSD.add_prefix('p_')
# merge purchase prices
ticket_data = ticket_data.merge(priceUSD_p,left_on='p_date',right_on='p_date',how='left')
# prefix v_ to priceUSD to merge - price when tickets vote
priceUSD_v = priceUSD.add_prefix('v_')
# merge voting prices
ticket_data = ticket_data.merge(priceUSD_v,left_on='v_date',right_on='v_date',how='left')
# calculate cost basis for every ticket
ticket_data['p_costUSD']=ticket_data.p_priceUSD*ticket_data.p_ticketprice

# purge
del priceUSD_p
del priceUSD_v

# create an array that is the additions to the stake realised cap - tickets that get purchased
SRP_adds=ticket_data[['p_date','p_costUSD','p_poolval']].copy()
# rename columns
SRP_adds=SRP_adds.rename(columns={"p_date": "date", "p_costUSD": "addUSD","p_poolval":"poolval"})
# set p_date as the index and agregate based on the day, sum for costUSD, average for the stakepool value
SRP_adds_agg = SRP_adds.set_index('date').groupby(pd.Grouper(freq='D')).agg({'addUSD':'sum','poolval':'max'})

# create an array that is the substractions to the stake realised cap - tickets that voted
SRP_subs=ticket_data[['v_date','p_costUSD']].copy()
# rename columns
SRP_subs=SRP_subs.rename(columns={"v_date": "date", "p_costUSD": "subUSD"})
# set p_date as the index and agregate based on the day, sum for costUSD, average for the stakepool value
SRP_subs_agg = SRP_subs.set_index('date').groupby(pd.Grouper(freq='D')).agg({'subUSD':'sum'})

# purge
del SRP_subs
del SRP_adds

# merge adds and subs into a single array
SRV = SRP_adds_agg.merge(SRP_subs_agg,left_on='date',right_on='date',how='left')
# compute net flows
SRV['SR_NET']=SRV.addUSD-SRV.subUSD
# get cap as the cumulative sum of net flows
SRV['CapStakeRealUSD']=SRV['SR_NET'].cumsum()
# remove temporary columns
SRV=SRV.drop(columns=['addUSD', 'subUSD','SR_NET'])

# purge
del SRP_subs_agg
del SRP_adds_agg

# Incorporate other metrics for computations
SRV = SRV.merge(CapMrktCurUSD,left_on='date',right_on='date',how='left')
SRV = SRV.merge(priceUSD,left_on='date',right_on='date',how='left')
SRV = SRV.merge(priceBTC,left_on='date',right_on='date',how='left')
SRV = SRV.merge(CapRealUSD,left_on='date',right_on='date',how='left')
SRV = SRV.merge(SplyCur,left_on='date',right_on='date',how='left')

# calculate market valuation of ticket pool value
SRV['CapStakeMrktUSD']=SRV.priceUSD*SRV.poolval

# calculate stake participation
SRV['StakePart']=100*SRV.poolval/SRV.SplyCur

# calculate supply adjusted stake realised value
SRV['CapSupAdjStRealUSD']=SRV.CapStakeRealUSD*SRV.SplyCur/SRV.poolval

# calculate the difference between the supply adjusted SRV and the RV
SRV['ASRVRV']=SRV['CapSupAdjStRealUSD']/SRV['CapRealUSD']


# set date as the index for the data frame.
SRV=SRV.set_index('date')
# drop NAs, theres some weird thing going on with pool val
SRV = SRV.dropna()

## -----------------
##  CHARTING
## -----------------

from matplotlib import pyplot as plt



# set colours
dcr_turq='#41BF53'
dcr_blue='#2970FF'
dcr_darkblue='#091440'
dcr_orange='#ED6D47'
dcr_green='#41BF53'

# set ylims for market value
mv_ymin=500000
mv_ymax=10000000000

## Chart 1 - Realised Value and Market Value
fig1 = plt.figure(1)
fig1.patch.set_facecolor('white')
fig1.patch.set_alpha(1)
axis1 = plt.axes()
axis1.set_title("Decred Market Valuations (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis1.set_ylabel("Valuation (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis1.set_facecolor('gainsboro')
axis1.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis1.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis1.set_xlim([date_start,date_end])
axis1.set_yscale('log')
# plot Market Value
axis1.plot(SRV.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Realised Value
axis1.plot(SRV.CapRealUSD, color=dcr_green,label='Realised Value',linewidth=2)
axis1.set_ylim(mv_ymin,mv_ymax)
axis1.legend()

## Chart 2 Stake Participation
fig2 = plt.figure(2)
fig2.patch.set_facecolor('white')
fig2.patch.set_alpha(1)
axis2 = plt.axes()
axis2.set_title("Decred Stake Participation (%)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis2.set_ylabel("Participation (%)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis2.set_facecolor('gainsboro')
axis2.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis2.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis2.set_xlim([date_start,date_end])
axis2.set_yscale('linear')
# plot Market Value
axis2.plot(SRV.StakePart, color=dcr_blue,label='Stake Participation (%)',linewidth=1)
axis2.legend()

## Chart 3 - Staked Market Value
fig3 = plt.figure(3)
fig3.patch.set_facecolor('white')
fig3.patch.set_alpha(1)
axis3 = plt.axes()
axis3.set_title("Decred Market Valuations (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis3.set_ylabel("Valuation (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis3.set_facecolor('gainsboro')
axis3.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis3.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis3.set_xlim([date_start,date_end])
axis3.set_yscale('log')
# plot Market Value
axis3.plot(SRV.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Staked Market Value
axis3.plot(SRV.CapStakeMrktUSD, color=dcr_blue,label='Staked Market Value',linewidth=2)
axis3.set_ylim(mv_ymin,mv_ymax)
axis3.legend()

## Chart 4 - Staked Realised Value
fig4 = plt.figure(4)
fig4.patch.set_facecolor('white')
fig4.patch.set_alpha(1)
axis4 = plt.axes()
axis4.set_title("Decred Market Valuations (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis4.set_ylabel("Valuation (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis4.set_facecolor('gainsboro')
axis4.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis4.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis4.set_xlim([date_start,date_end])
axis4.set_yscale('log')
# plot Market Value
axis4.plot(SRV.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Realised Value
axis4.plot(SRV.CapRealUSD, color=dcr_green,label='Realised Value',linewidth=2)
# plot Staked Realised Value
axis4.plot(SRV.CapStakeRealUSD, color=dcr_orange,label='Staked Realised Value',linewidth=2)
axis4.set_ylim(mv_ymin,mv_ymax)
axis4.legend()

## Chart 5 - Supply Adjusted Staked Realised Value
fig5 = plt.figure(5)
fig5.patch.set_facecolor('white')
fig5.patch.set_alpha(1)
axis5 = plt.axes()
axis5.set_title("Decred Market Valuations (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis5.set_ylabel("Valuation (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis5.set_facecolor('gainsboro')
axis5.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis5.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis5.set_xlim([date_start,date_end])
axis5.set_xlim([date_start,date_end])
axis5.set_yscale('log')
# plot Market Value
axis5.plot(SRV.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Realised Value
axis5.plot(SRV.CapRealUSD, color=dcr_green,label='Realised Value',linewidth=2)
# plot Staked Realised Value
axis5.plot(SRV.CapStakeRealUSD, color=dcr_orange,label='Staked Realised Value',linewidth=2)
# plot Supply Adjusted Staked Realised Value
axis5.plot(SRV.CapSupAdjStRealUSD, color=dcr_blue,label='Sup. Adj. Staked Realised Value',linewidth=2)
axis5.set_ylim(mv_ymin,mv_ymax)
axis5.legend()

## Chart 6 - Supply Adjusted Staked Realised Value / Realised Value
fig6 = plt.figure(6)
fig6.patch.set_facecolor('white')
fig6.patch.set_alpha(1)
axis6 = plt.axes()
axis6.set_title("Supply-Adjusted Stake Realised Value / Realised Value Ratio", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis6.set_ylabel("Valuation (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis6.set_facecolor('gainsboro')
axis6.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis6.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis6.set_xlim([date_start,date_end])
axis6.set_yscale('log')
# plot Market Value
axis6.plot(SRV.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Realised Value
axis6.set_ylim(1,mv_ymax)
axis6a = axis6.twinx()
axis6a.plot(SRV.ASRVRV, color=dcr_darkblue,label='SASRV / RV Ratio',linewidth=1)
axis6a.set_ylabel("Ratio", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis6a.fill_between(SRV.index,1,SRV.ASRVRV,where=SRV.ASRVRV < 1,facecolor='red', alpha=0.5)
axis6a.fill_between(SRV.index,1,SRV.ASRVRV,where=SRV.ASRVRV >= 1,facecolor='green', alpha=0.5)
axis6a.set_ylim(0.5,3)

plt.show()