

# Perfect Competition Analysis 

### Operational Hypothesis Framework
“I expect 20 carrot beds, 30 mesclun beds, and 14 tomato beds, because this would maximize efficiency in terms of optimizing cost and wages.”

### Deep-Dive Executive Analysis & Visual Graph Diagnostics
The hypothesis correctly identifies that labor complexity closes the revenue gap at 10 tomato beds, but it incorrectly proposes planting 14 tomato beds. As visually demonstrated, at bed 10, the tomato marginal cost remains below the flat $8,800.00 market price and earning a net margin of $551.40 for that bed. Every bed beyond 10 costs significantly more to produce than it earns. The chart also illustrates a notable labor threshold dip between bed 5 ($7,660.70) and bed 6 ($4,906.30), occurring when cumulative farm labor crosses 720 hours, dropping the marginal wage rate from the farmer's implied $34.72/hr to the temporary worker rate of $17.36/hr. While this wage drop creates a temporary cost reduction, compounding complexity quickly dominates, establishing 10 beds as the strict profit-maximizing cutoff.

![Tomato marginal cost vs. price, standalone](figures/tomato-mc-vs-price.png)
*tomato-mc-vs-price.png — the bed 10/11 crossing and the bed 5→6 dip described above.*

The hypothesis correctly predicts 20 carrot beds, but understanding why requires reconciling two seemingly conflicting charts. The standalone chart shows carrot MC crossing above the $2,094.00 market price between beds 10 and 16, peaking at $2,551.80 before dropping at bed 17. This standalone model assumes carrots receive a private allocation of cheap farmer hours.

![Carrot marginal cost vs. price, standalone](figures/carrot-mc-vs-price-standalone.png)
*carrot-mc-vs-price-standalone.png — MC crosses price between bed 10 and 16, dips again at bed 17.*

In the actual joint plan, higher-value tomatoes claim the cheap farmer hours first, so all carrot expansion is priced at the temporary worker rate ($17.36/hr) from bed 1 onward. Joint carrot MC remains constant at $1,688.80 at bed 20—comfortably below the $2,094.00 price across all beds. Carrots are constrained strictly by their policy cap (20), generating a shadow price of $352.50 if relaxed to 21 beds.

![Carrot marginal cost vs. price, joint context](figures/carrot-mc-vs-price-joint.png)
*carrot-mc-vs-price-joint.png — TOM=10 and MES=30 held at the optimum; MC stays well under price through bed 20.*

The hypothesis correctly allocates 30 mesclun beds. A naive stopping rule would halt mesclun at 6 beds. However, between beds 13 and 15, pooled labor hours pass the 720-hour farmer threshold, causing MC to plummet to ~$1,980.00 at bed 15. From bed 15 through bed 30, MC stays well below market price. Mesclun expands to its policy cap (30), yielding a shadow price of $246.50 for the 31st bed.

![Mesclun marginal cost vs. price, standalone](figures/mesclun-mc-vs-price.png)
*mesclun-mc-vs-price.png — the bed 6/7 crossing and the bed 13→15 dip described above.*

Shadow price calculations and individual crop profitability assessments highlight strategic resource allocation and validate production under the economic shutdown rule. While standalone carrots and mesclun operate at net losses, both satisfy the shutdown rule because their market prices exceed Average Variable Cost at their caps.

### Conclusion & Hypothesis Verdict
In conclusion, the hypothesis is PARTIALLY CORRECT in its economic intuition but INCORRECT in its proposed final allocation. Expanding tomatoes to 14 beds to force full 64-bed land utilization destroys farm profit because beds 11 through 14 generate severe marginal losses. Land capacity is a slack resource. Forcing 100% land occupancy reduces net farm returns. The true profit-maximizing plan is exactly 20 carrots, 30 mesclun, and 10 tomatoes, leaving 4 beds unplanted.
