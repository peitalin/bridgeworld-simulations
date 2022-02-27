

treasure_demand = crafting_for_harvesters + crafting_for_summoning_boosts
+ crafting_in_ecosystem_partners + more_utility_for_treasures

treasure_supply = legions_questing * drop_rate
- supply is a function of treasure prices, there is no supply-side scarcity
- it depends on legions questing, in tun determined by summoning rates

legions_questing = percentage_of_legions_questing * legions
legions = (n * (n - 1)) / 2
- where n is nth summoning period
- legions population accelerates over time

legions_questing = percentage_of_legions_questing * legions

Er[questing] = 0.2 * drop_rate_weighted_price of treasures
- [drop_rate * price for drop_rate, price in [t1, t2, t3, t4, t5 treasure tiers]]

Er[mining] = NFTBoost * user_wealth
- legions are more useful in the mine for richer users

Er[summoning] = -500MAGIC - opportunity_cost_of_questing_1_week + Er[questing at t+1]
- sacrifice 1 period of questing/mining and 500 MAGIC for 1x  lifetime value of a legion
- which is an income stream of questing 1 period from now = Er_t+1[questing]



treasure_demand = crafting_for_harvesters + crafting_for_summoning_boosts
+ crafting_in_ecosystem_partners + more_utility_for_treasures

treasure_supply = legions_questing * drop_rate
- supply is a function of treasure prices, there is no supply-side scarcity
- it depends on legions questing, in tun determined by summoning rates

legions_questing = percentage_of_legions_questing * legions
legions = (n * (n - 1)) / 2
- where n is nth summoning period
- legions population accelerates over time


- Atm we're seeing treasure prices dropping sharply, and rapid increase in legions:
- mainly because:
(Er[questing] or Er[summoning]) > Er[mining] > Er[crafting]
- (where Er[..] is expected returns)

And this will continue to a point where treasure prices drop enough, then we get:
Er[mining] > (Er[questing] or Er[summoning]) > Er[crafting]

at which point, legions return to the mines

An immediate reaction (not necessary the best solution) would probably be to try:
1 Reduce drop rates weekly from 20% to 10% (Taper Treasures)
* this still runs into inflation once summoning ramps up
2. Recycled treasures only
* this would sharply decrease drop rates and probably cause aux legions to dump (and to some extent gen legions will suffer price decline too)
* we actually do want some treasure inflation to supply ecosyste partners + keep crafting affordable
3. some mix of 1 and 2

I think the fundamental issue is that there are no competitive dynamics on supply in summoning and questing.
Unlike mining there is no dilution of supply as more people engage in the activity,
the only factor reducing supply is prices of treasures (legions are treasure producign factories)

IMO, a more effective long-term way to handle treasure & legion inflation is to introduce
competitive dynamics in the creation of more treasures and more legions.

Some potential solutions:
Fixed rate of treasures dropped per period.
* Implementing a fixed cap per period so that even if 10x legions quested, supply remains the same
and drop rates are dependent on supply of questors
* that way treasure production doesn't scale with legion population

Potential solutions for summoning:
* %chance of summon, based on population of legions summoning
* % chance of successful summoning goes down as more people summon
* e.g. something like baseRate + (1 - legions_summoning / total_legions)


Once we introduce competition in summoning + questing, we can introduce boost-like mechanisms
there too.
* prism shards boost your summoning rates? becomes essential to use (espeically if everyone else is using it)
* crafting mini-recipes to boost questes now becomes viable and essential

