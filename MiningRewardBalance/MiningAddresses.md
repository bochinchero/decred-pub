# Having a peek at Decred's largest miners' address activity

By now everyone has probably heard about the [new proposal](https://proposals.decred.org/record/a8501bc) in Politeia to reduce PoW block reward to 1% and change the algorithm to Blake3.

Dave's [comment](https://proposals.decred.org/record/a8501bc/comments/66) on the proposal around the activity of a few particular addresses prompted me to have a look myself. I ran a query on my own dcrdata instance to get a list of the addresses that received the largest amount of mining rewards up to Dec.2022 (my dcrdata postgres db faulted then, it's currently rebuilding from scratch, which takes a few days on my hardware - I doubt the list has changed much, though). 

Below are a list of the 22 addresses that received over 100k DCR in mining rewards since launch.

| Address                             | Block Rewards Received |
|-------------------------------------|------------------------|
| DshuxHmbE8qvRu91fMQGaQV6j1oDijkpoJk | 106,428.24             |
| DsfD7KYsJtRraYXPZM61ui7779oYJCakYvH | 106,894.32             |
| DsXFWjdKKaE4ftDa1AVam35EX9wdaDeZz3q | 128,413.54             |
| DskFbReCFNUjVHDf2WQP7AUKdB27EfSPYYE | 131,126.05             |
| DshN1YKazYrnVcf9ZmudCiuvYCif72rQqUw | 143,007.68             |
| Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj | 142,614.70             |
| Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz | 148,327.54             |
| DsaczRtjC31N6XVV69qcBoyR2BEEmjRDay3 | 147,868.50             |
| DshZYJySTD4epCyoKRjPMyVmSvBpFuNYuZ4 | 179,322.32             |
| DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb | 162,229.42             |
| DsVc7oQTKhGUQ9DyCXbPEkHCoqT2cmkjgS8 | 186,746.84             |
| DseXBL6g6GxvfYAnKqdao2f7WkXDmYTYW87 | 204,571.15             |
| DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw | 268,815.20             |
| DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF | 290,226.07             |
| DsYAN3vT15rjzgoGgEEscoUpPCRtwQKL7dQ | 355,517.56             |
| DsZWrNNyKDUFPNMcjNYD7A8k9a4HCM5xgsW | 314,660.47             |
| DsfUs6UvDuvqPka1LK9JFZPiRetJ4WNycmn | 372,596.90             |
| DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu | 526,794.93             |
| Dsh5gKAtf63WuzeqxFV7vJTFkPRkE35Zaf9 | 544,752.97             |
| Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r | 601,432.37             |
| DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM | 713,482.70             |
| DshMNsvETDWpVoCe1re9NTAChiJagzsFV7J | 950,296.17             |

I then created a script to pull the daily activity for these 22 addresses for charting from dcrdata.org's api, and included the approximate key dates below to see if there was anything in particular that stood out. Some of these dates are taken from Checkmate's [Mining Market Mechanics ](https://medium.com/decred/decred-mining-market-mechanics-fd26b921dc46)piece, along with Politeia, dcrdata and other sources.

| ID | Date    | Event(s)                                                                        |
|----|---------|---------------------------------------------------------------------------------|
| 1  | 2018-01 | Baikal BK-B                                                                     |
| 2  | 2018-04 | Innosilicon D9                                                                  |
| 3  | 2018-06 |  Baikal BK-D, FFMiner D18, Obelisk DCR-1 - Huobi & OkEX Listings, DEX blog post |
| 4  | 2018-08 | Innosilion D9+, FFMiner DS19, Ibelink DSM7T                                     |
| 5  | 2018-09 | Bitmain DR-9                                                                    |
| 6  | 2018-10 | StrongU STU-U1 & STU-U1+ - Binance Listing                                      |
| 7  | 2018-11 | MicroBT Whatsminer D1                                                           |
| 8  | 2018-12 | Bitmain DR-5                                                                    |
| 9  | 2019-07 | StrongU STU-U1++                                                                |
| 10 | 2020-10 | DCR DEX Launch                                                                  |
| 11 | 2021-09 | Bitmain DR-5 - New batch shipped.                                               |
| 12 | 2021-11 | Subsidy Change (10/80) Proposal Posted                                          |
| 13 | 2022-05 | Subsidy Change (10/80) Activates                                                |
| 14 | 2022-09 | Huobi Delisting                                                                 |

I don't intend to do a huge amount of analysis or commentary here, just share the data so whoever has a look at this can draw their own conclusions. 

## The Bigger Picture
Once I had the events and charting, I plotted the sum balance of the addresses above, price data is taken from coinmetrics community API.

![Combined Full History ](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/Combined%20100k+%20PoW%20Block%20Reward%20Address%20Balance.png?raw=true)

While there is some obvious correlation in the selloff from 2022 onwards, things really get a bit more interesting if you break it down and have a look at the balance of each address - do keep in mind that the y-axis scale is different for each chart.

![DshMNsvETDWpVoCe1re9NTAChiJagzsFV7J](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DshMNsvETDWpVoCe1re9NTAChiJagzsFV7J%20Balance.png?raw=true)
![DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM%20Balance.png?raw=true)
![Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r%20Balance.png?raw=true)
![Dsh5gKAtf63WuzeqxFV7vJTFkPRkE35Zaf9](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/Dsh5gKAtf63WuzeqxFV7vJTFkPRkE35Zaf9%20Balance.png?raw=true)
![DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu%20Balance.png?raw=true)
![DsfUs6UvDuvqPka1LK9JFZPiRetJ4WNycmn](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsfUs6UvDuvqPka1LK9JFZPiRetJ4WNycmn%20Balance.png?raw=true)
![DsZWrNNyKDUFPNMcjNYD7A8k9a4HCM5xgsW](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsZWrNNyKDUFPNMcjNYD7A8k9a4HCM5xgsW%20Balance.png?raw=true)
![DsYAN3vT15rjzgoGgEEscoUpPCRtwQKL7dQ](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsYAN3vT15rjzgoGgEEscoUpPCRtwQKL7dQ%20Balance.png?raw=true)
![DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF%20Balance.png?raw=true)
![DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw%20Balance.png?raw=true)
![DseXBL6g6GxvfYAnKqdao2f7WkXDmYTYW87](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DseXBL6g6GxvfYAnKqdao2f7WkXDmYTYW87%20Balance.png?raw=true)
![DsVc7oQTKhGUQ9DyCXbPEkHCoqT2cmkjgS8](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsVc7oQTKhGUQ9DyCXbPEkHCoqT2cmkjgS8%20Balance.png?raw=true)
![DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb%20Balance.png?raw=true)
![DshZYJySTD4epCyoKRjPMyVmSvBpFuNYuZ4](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DshZYJySTD4epCyoKRjPMyVmSvBpFuNYuZ4%20Balance.png?raw=true)
![DsaczRtjC31N6XVV69qcBoyR2BEEmjRDay3](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsaczRtjC31N6XVV69qcBoyR2BEEmjRDay3%20Balance.png?raw=true)
![Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz%20Balance.png?raw=true)
![Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj%20Balance.png?raw=true)
![DshN1YKazYrnVcf9ZmudCiuvYCif72rQqUw](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DshN1YKazYrnVcf9ZmudCiuvYCif72rQqUw%20Balance.png?raw=true)
![DskFbReCFNUjVHDf2WQP7AUKdB27EfSPYYE](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DskFbReCFNUjVHDf2WQP7AUKdB27EfSPYYE%20Balance.png?raw=true)
![DsXFWjdKKaE4ftDa1AVam35EX9wdaDeZz3q](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsXFWjdKKaE4ftDa1AVam35EX9wdaDeZz3q%20Balance.png?raw=true)
![DsfD7KYsJtRraYXPZM61ui7779oYJCakYvH](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DsfD7KYsJtRraYXPZM61ui7779oYJCakYvH%20Balance.png?raw=true)
![DshuxHmbE8qvRu91fMQGaQV6j1oDijkpoJk](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/all/DshuxHmbE8qvRu91fMQGaQV6j1oDijkpoJk%20Balance.png?raw=true)

## Zooming in: 2018-2020 Bear Market

![Combined](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/Combined%20100k+%20PoW%20Block%20Reward%20Address%20Balance.png?raw=true "Combined")

Note that I have only added images for the addresses with activity in this date range.

![DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM%20Balance.png?raw=true)
![Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r%20Balance.png?raw=true)
![DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu%20Balance.png?raw=true)
![DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF%20Balance.png?raw=true)
![DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw%20Balance.png?raw=true)
![DseXBL6g6GxvfYAnKqdao2f7WkXDmYTYW87](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DseXBL6g6GxvfYAnKqdao2f7WkXDmYTYW87%20Balance.png?raw=true)
![DsVc7oQTKhGUQ9DyCXbPEkHCoqT2cmkjgS8](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsVc7oQTKhGUQ9DyCXbPEkHCoqT2cmkjgS8%20Balance.png?raw=true)
![DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb%20Balance.png?raw=true)
![Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz%20Balance.png?raw=true)
![Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj%20Balance.png?raw=true)
![DskFbReCFNUjVHDf2WQP7AUKdB27EfSPYYE](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DskFbReCFNUjVHDf2WQP7AUKdB27EfSPYYE%20Balance.png?raw=true)
![DsXFWjdKKaE4ftDa1AVam35EX9wdaDeZz3q](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsXFWjdKKaE4ftDa1AVam35EX9wdaDeZz3q%20Balance.png?raw=true)
![DsfD7KYsJtRraYXPZM61ui7779oYJCakYvH](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DsfD7KYsJtRraYXPZM61ui7779oYJCakYvH%20Balance.png?raw=true)
![DshuxHmbE8qvRu91fMQGaQV6j1oDijkpoJk](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear1/DshuxHmbE8qvRu91fMQGaQV6j1oDijkpoJk%20Balance.png?raw=true)


## Zooming in: 2021-2023 Bear Market

![Combined](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/Combined%20100k+%20PoW%20Block%20Reward%20Address%20Balance.png?raw=true)

Note that I have only added images for the addresses with activity in this date range.

![DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DsSWTHFrsXV77SwAcMe451kJTwWjwPYjWTM%20Balance.png?raw=true)
![Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/Dsh3RaFqAgnfnGqY9cQiJUde5cR7qwdQP8r%20Balance.png?raw=true)

![DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DsiDegkW7HxidcUCNpRqpgskc9JFCkqwWeu%20Balance.png?raw=true)
![DsfUs6UvDuvqPka1LK9JFZPiRetJ4WNycmn](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DsfUs6UvDuvqPka1LK9JFZPiRetJ4WNycmn%20Balance.png?raw=true)
![DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DsnxqhJX2tjyjbfb9y4yPdpJ744G9fLhbbF%20Balance.png?raw=true)
![DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DsjukEpaBShycR6GW3gMX5t8j8kSCLKLTUw%20Balance.png?raw=true)
![DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DscMACUgLBhyDhVcg8YgaX68JJVrbdNndrb%20Balance.png?raw=true)
![DsaczRtjC31N6XVV69qcBoyR2BEEmjRDay3](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/DsaczRtjC31N6XVV69qcBoyR2BEEmjRDay3%20Balance.png?raw=true)
![Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/Dsa3yVGJK9XFx6L5cC8YzcW3M5Q85wdEXcz%20Balance.png?raw=true)
![Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj](https://github.com/bochinchero/decred-pub/blob/main/MiningRewardBalance/bear2/Dso9uYBoEfvka4L7zLw9YoS5N7d6wmHu3sj%20Balance.png?raw=true)
