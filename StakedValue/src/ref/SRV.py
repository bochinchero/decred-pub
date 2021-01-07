import boc_tools as boc
import pandas as pd
from datetime import date

# Set date range to fetch and grpah data
date_start  = date(int(2016),int(6),int(1))
date_end    = date(int(2021),int(1),int(15))

# get price data from CM
PriceUSD = boc.cm_getmetric('dcr','PriceUSD',date_start,date_end)
SplyCur = boc.cm_getmetric('dcr','SplyCur',date_start,date_end)
CapMrktCurUSD = boc.cm_getmetric('dcr','CapMrktCurUSD',date_start,date_end)
CapRealUSD = boc.cm_getmetric('dcr','CapRealUSD',date_start,date_end)

# get ticket data from dcrdata instance
tickets = boc.dcrdata_pgquery_utxo_tickets()
# get poolval data from dcrdata instance
poolval = boc.dcrdata_pgquery_poolval()

# calculate staked realised value
df = boc.calculate_realcap(tickets,PriceUSD.rename(columns={"date": "date", "PriceUSD": "price"}))
df = df.rename(columns={"date": "date", "realcap": "SRV"})

# merge other metrics
df = df.merge(SplyCur, left_on='date', right_on='date', how='left')
df = df.merge(poolval, left_on='date', right_on='date', how='left')
df = df.merge(CapRealUSD, left_on='date', right_on='date', how='left')
df = df.merge(CapMrktCurUSD, left_on='date', right_on='date', how='left')

# purge
del tickets,poolval

# calculate supply adjusted SRV
df['SASRV'] = df.SRV * df.SplyCur / df.poolval

# calculate the SASRVRV ratio/oscilator
df['SASRVRV'] = df.SASRV / df.CapRealUSD


df=df.set_index('date')


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

## Chart 1 - Supply Adjusted Staked Realised Value
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
axis1.set_xlim([date_start,date_end])
axis1.set_yscale('log')
# plot Market Value
axis1.plot(df.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Realised Value
axis1.plot(df.CapRealUSD, color=dcr_green,label='Realised Value',linewidth=2)
# plot Staked Realised Value
axis1.plot(df.SRV, color=dcr_orange,label='Staked Realised Value',linewidth=2)
# plot Supply Adjusted Staked Realised Value
axis1.plot(df.SASRV, color=dcr_blue,label='Sup. Adj. Staked Realised Value',linewidth=2)
axis1.set_ylim(mv_ymin,mv_ymax)
axis1.legend()

## Chart 6 - Supply Adjusted Staked Realised Value / Realised Value
fig2 = plt.figure(2)
fig2.patch.set_facecolor('white')
fig2.patch.set_alpha(1)
axis2 = plt.axes()
axis2.set_title("Supply-Adjusted Stake Realised Value / Realised Value Ratio", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis2.set_ylabel("Valuation (USD)", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis2.set_facecolor('gainsboro')
axis2.tick_params(color=dcr_darkblue, labelcolor=dcr_darkblue)
axis2.grid(color=dcr_darkblue, linestyle='--', linewidth=0.5)
axis2.set_xlim([date_start,date_end])
axis2.set_yscale('log')
# plot Market Value
axis2.plot(df.CapMrktCurUSD, color=dcr_darkblue,label='Market Value',linewidth=1)
# plot Realised Value
axis2.set_ylim(1,mv_ymax)
axis2a = axis2.twinx()
axis2a.plot(df.SASRVRV, color=dcr_darkblue,label='SASRV / RV Ratio',linewidth=1)
axis2a.set_ylabel("Ratio", fontsize=12, fontweight='bold', color=dcr_darkblue)
axis2a.fill_between(df.index,1,df.SASRVRV,where=df.SASRVRV < 1,facecolor='red', alpha=0.5)
axis2a.fill_between(df.index,1,df.SASRVRV,where=df.SASRVRV >= 1,facecolor='green', alpha=0.5)
axis2a.set_ylim(0.5,3)

plt.show()