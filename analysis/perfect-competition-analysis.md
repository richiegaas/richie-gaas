

# Perfect Competition Analysis 

### Operational Hypothesis Framework
The operational hypothesis under evaluation states: “I expect 20 carrot beds, 30 mesclun beds, and 14 tomato beds, because this would maximize efficiency in terms of optimizing cost and wages, and because tomatoes earn about four times more per bed compared to carrots and mesclun, I believe the labor penalty closes that gap at 10 tomato beds.”
This hypothesis embeds three explicit analytical assertions: (1) full land utilization across all 64 total beds (20 carrots + 30 mesclun + 14 tomatoes) maximizes operational efficiency; (2) tomatoes warrant maximum land allocation because their market price ($8,800.00/bed) is roughly four times higher than carrots ($2,094.00/bed) and mesclun ($2,700.00/bed); and (3) compounding labor penalties alter the marginal cost structure, creating a critical economic threshold around 10 tomato beds. Evaluating this hypothesis requires synthesizing all case data, diagnostic workbooks, and four marginal cost vs. price chart sources.

### Deep-Dive Executive Analysis & Visual Graph Diagnostics
Tomato Cost Dynamics & The 10-Bed Hard Limit: The hypothesis correctly identifies that labor complexity closes the revenue gap at 10 tomato beds, but it incorrectly proposes planting 14 tomato beds. As visually demonstrated in tomato-mc-vs-price.png, tomatoes experience a steep 10% compounding labor penalty per bed due to pest pressure, harvest bottlenecks, and walking time. At bed 10, the tomato marginal cost (MC) is $8,248.60, remaining below the flat $8,800.00 market price and earning a net margin of $551.40 for that bed. However, at bed 11, compounding labor costs push MC up to $9,390.80—exceeding the market price by $590.80 per bed. Planting beds 11 through 14 generates severe cumulative losses because every bed beyond 10 costs significantly more to produce than it earns. The chart also illustrates a notable labor threshold dip between bed 5 ($7,660.70) and bed 6 ($4,906.30), occurring when cumulative farm labor crosses 720 hours, dropping the marginal wage rate from the farmer's implied $34.72/hr to the temporary worker rate of $17.36/hr. While this wage drop creates a temporary cost reduction, compounding complexity quickly dominates, establishing 10 beds as the strict profit-maximizing cutoff.

![Tomato marginal cost vs. price, standalone](figures/tomato-mc-vs-price.png)
*tomato-mc-vs-price.png — the bed 10/11 crossing and the bed 5→6 dip described above.*

Carrot Allocation & Graph Reconciliation (20 Beds): The hypothesis correctly predicts 20 carrot beds, but understanding why requires reconciling two seemingly conflicting charts: carrot-mc-vs-price.png (standalone) and carrot-mc-vs-price-joint.png (joint context). The standalone chart shows carrot MC crossing above the $2,094.00 market price between beds 10 and 16, peaking at $2,551.80 before dropping at bed 17. This standalone model assumes carrots receive a private allocation of cheap farmer hours.

![Carrot marginal cost vs. price, standalone](figures/carrot-mc-vs-price-standalone.png)
*carrot-mc-vs-price-standalone.png — MC crosses price between bed 10 and 16, dips again at bed 17.*

In the actual joint plan, higher-value tomatoes claim the cheap farmer hours first, so all carrot expansion is priced at the temporary worker rate ($17.36/hr) from bed 1 onward. As proven in carrot-mc-vs-price-joint.png, joint carrot MC remains constant at $1,688.80 at bed 20—comfortably below the $2,094.00 price across all beds. Carrots are constrained strictly by their policy cap (CAR_MAXBED = 20), generating a positive shadow price of $352.50 if relaxed to 21 beds.

![Carrot marginal cost vs. price, joint context](figures/carrot-mc-vs-price-joint.png)
*carrot-mc-vs-price-joint.png — TOM=10 and MES=30 held at the optimum; MC stays well under price through bed 20.*

Mesclun Optimization & Premature Stopping Signals (30 Beds): The hypothesis correctly allocates 30 mesclun beds. As illustrated in mesclun-mc-vs-price.png, mesclun MC initially crosses above the $2,700.00 market price between beds 6 and 13 (peaking at ~$2,980.00). A naive stopping rule would halt mesclun at 6 beds. However, between beds 13 and 15, pooled labor hours pass the 720-hour farmer threshold, causing MC to plummet to ~$1,980.00 at bed 15. From bed 15 through bed 30, MC stays well below market price (reaching ~$2,420.00 at bed 30). Mesclun expands to its policy cap (MES_MAXBED = 30), yielding a shadow price of $246.50 for the 31st bed.

![Mesclun marginal cost vs. price, standalone](figures/mesclun-mc-vs-price.png)
*mesclun-mc-vs-price.png — the bed 6/7 crossing and the bed 13→15 dip described above.*

### Conclusion & Hypothesis Verdict
In conclusion, the hypothesis is PARTIALLY CORRECT in its economic intuition but INCORRECT in its proposed final allocation. The hypothesis accurately identifies 20 carrot beds and 30 mesclun beds as crop optima, and correctly pinpoints that labor penalties close the tomato profitability gap at 10 beds. However, proposing 14 tomato beds contradicts the P = MC stopping rule. Expanding tomatoes to 14 beds to force full 64-bed land utilization destroys farm profit because beds 11 through 14 generate severe marginal losses. Because land capacity is a slack resource (60 of 64 beds used; shadow price = $0.00), forcing 100% land occupancy reduces net farm returns. The true profit-maximizing plan is exactly 20 carrots, 30 mesclun, and 10 tomatoes (60 beds total), leaving 4 beds unplanted.
