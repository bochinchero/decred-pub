# Decred On-Chain: Stake-based Valuation Models

### Background

The following works are the basis for the research below, consider it prior recommended reading:
* [Realised Capitalisation](https://coinmetrics.io/realized-capitalization/) by Nic Carter and Antoine Le Calvez
* [Realised Cap, MVRV ratio and Gradient Oscillators](https://medium.com/decred/decred-on-chain-realised-cap-mvrv-ratio-and-gradient-oscillators-a36ed2cc8182) by Checkmate.
*  [Ticket Pool Volume Weighted Average (TVWAP)](https://medium.com/@permabullnino/decred-on-chain-the-ticket-pool-vwap-d0a3d1c42a3) by Permabull Niño.

Defining some of the terms that are referred to throughout the rest of this post:

* **Market Value** or market capitalisation the traditional means of valuation in legacy finance, widely used as a metric for cryptocurrencies, it's calculated as `circulating supply * latest market price`.
* **Realised Value** is a valuation metric based on the cumulative sum of the price of each UTXO when it last moved.
 * **Ticket Pool Size** is the total number of Proof-of-Stake tickets in the Decred network, this size oscillates around 40,960 - which is the a target ticket pool size, a predefined network parameter.
* **Ticket Pool Value** is the total amount of DCR locked in on tickets. at a given time.

Decred's Proof-of-Stake and ticket-based governance system is the heartbeat of the protocol, it generates a constant flow of coins that, when analysed through already established on-chain metrics, creates a differentiating imprint that makes Decred stand out when compared to other UTXO chains.  


Checkmate's article above delves deep into the Realised Value and its very unique behaviour when it comes to Decred, it acts as a kind of moving average to the Market Value, acting as support during upward trends and resistance on downward trends.


![Realised Value](./1_RealisedCap.PNG)


### The Ticket Pool: A Map For Stakeholder Sentiment

Given that the Decred stakeholders lock up coins for up to 142 days to stake, the ticket pool and some of the metrics that can be derived from it can provide clear signals of stakeholder commitment to participate in the governance and security of the network. A good proportion of these metrics are unique to Decred's hybrid consensus and ticketing system, as such cannot be compared on equal footing to any other chain out there.

The **Stake Participation** is the simplest form of these metrics, it is calculated as `Ticket Pool Value / Circulating Supply` at any given time. It's easily available as a chart on the [dcrdata.org block explorer](https://explorer.dcrdata.org/charts?chart=stake-participation&zoom=ikd7pc00-khmn2tc0&bin=day&axis=time&visibility=true-false). In simple terms, it's the percentage of supply has been locked in tickets.

![Stake Participation](./3_StakedSupply.PNG)

Since the launch of the network, the stake participation has seen a nearly consistent uptrend, with every higher high and subsequent retracement establishing a new, higher low. The demand to participate in the governance and security of the protocol has not been fazed at all by the bear market over the past two years.


| Peak Date | Peak Stake Participation (%) | Bottom Date | Bottom Stake Participation (%) |
|--|--|--|--|
|2017-03-29|41.82%|2017-06-30|35.28%|
|2018-01-17|47.63%|2018-04-03|45.43%|
|2018-06-28|47.85%|2018-09-10|45.84%|
|2020-01-20|51.85%|2020-02-22|48.60%|

Going a step further, we can take a first stab at establishing a metric that measures valuation from the stakeholder sentiment point of view via the **Staked Market Value**, which is calculated as the `Ticket Pool Value * Latest Market Price`.

![Staked Market Value](./4_StakeValue.PNG)

This metric gives us the current valuation of all the DCR in the ticket pool at a given time. It's an analogy to the Total Value Locked (TVL) in the decentralised finance space, a concise indicator of the current value of the capital that's been put at stake to participate in the network while earning yield.

The main disadvantage of this metric is that it weighs all of the stake at the current price, implicitly making the assumption that stakeholders are choosing to continue staking at the current valuation. In reality, stakeholders have agreed to engage in a contract, locking their coins at a specific market valuation and ticket price, expecting a yield within a certain range. Since the tickets are pseudo-randomly selected to vote, stakeholders do not have the option of withdrawing from the contract until their ticket is either called to vote or expires.


### Introducing the Staked Realised Value

The Staked Realised Value is an attempt at a more accurate valuation based on stakeholder sentiment, it's defined as the valuation of the ticket pool, measured by cost of every ticket on the day it was purchased and added to the pool.

Assuming a hypothetical case where there are no tickets live on the network and three are purchased in consecutive days, voting a few days later in the same order:

| Ticket ID |Date Purchased  | Ticket Price (DCR)  |   Date Voted |
|--|--|--|--|
|1 |Day 1| 100 DCR | Day 11
|2 |Day 2 | 100 DCR | Day 12
|3 |Day 3 | 100 DCR | Day 13

The stake realised value would be calculated as:

 Date | DCR Price | Ticket Pool Value (DCR) | Staked Realised Value  | Net Change |  Comment
--|--|--|--|--|--|
Day 0 | 1 USD| 0 DCR |0 USD | 0 | No Change
Day 1 | 1 USD| 100 DCR |100 USD | + 100 USD| Ticket 1 Purchased
Day 2 | 2 USD| 200 DCR | 300 USD | + 200 USD | Ticket 2 Purchased
Day 3| 3 USD| 300 DCR | 600 USD | + 300 USD | Ticket 3 Purchased
Day 4| 10 USD| 300 DCR | 600 USD | 0 | No Change 
Day 11| 10 USD | 200 DCR | 500 USD | - 100 USD |  Ticket 1 Voted
Day 12| 10 USD | 100 DCR| 300 USD | - 200 USD | Ticket 2 Voted
Day 13 | 10 USD | 0 DCR | 0 USD | - 300 USD | Ticket 3 Voted
Day 14 | 10 USD | 0 DCR | 0 USD | 0 | No change

Even as the DCR/USD price rises tenfold between Day 1 and Day 4, the Staked Realised Value is still calculated on the initial capital that was locked with every ticket.

The chart below includes the Staked Realised Value alongside the Market Value and Realised Value.

![Staked Realised Value](./5_StakeRealisedValue.PNG)

The Staked Realised value behaves very much like the lower band for the Market Value. In sharp sell-offs, the value locked into governance and security of the network acts as the psychological bottom for stakeholders. 

The downside of this metric as a valuation model is that it only accounts for the coins that are in the ticket pool value at a given time, so by definition it will always be considerably below the Market and Realised Value. 

In order to estimate the collective average DCR price for all of the coins currently locked in the ticket pool, we can calculate the  **Supply-Adjusted Staked Realised Value** (this needs a better name) as`Staked Realised Value * (Circulating Supply / Ticket Pool Value)`. 
 
![Supply Adjusted Staked Realised Value](./6_SupAdjStakeReal.PNG)

The Supply Adjusted Staked Realised Value is an approximation of the Realised Value but focused exclusively on stakeholders. It behaves as a faster moving average to the market value, acting as support in uptrends and resistance in downtrends and sideways action.

Since Decred has only gone through a single market cycle, we lack enough data points to make conclusive statements regarding the relationship between these metrics and how they behave during bull and bear markets. That being said, given the early indications of a new market cycle beginning, these are definitely something to keep an eye on for the next few months.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzMjY1MTQ4NywtNTMzOTAxMzM1LC0xND
U2OTM3OTYxLC0yNzE5Njg1OTBdfQ==
-->
