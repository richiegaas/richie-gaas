

# Perfect Competition Analysis 

### Tomato Allocation Cap (Bed 10) and Labor Rate Shift
Tomato production halts at 10 beds because marginal cost exceeds market price at bed 11, as visually demonstrated in the standalone tomato marginal cost chart. At bed 10, the tomato marginal cost of $8,248.60 remains below the $8,800.00 market price threshold, making the tenth bed profitable. However, at bed 11, marginal cost rises to $9,390.80, crossing above the market price line and making further expansion unprofitable. The tomato marginal cost curve also features a prominent cost dip between bed 5 ($7,660.70) and bed 6 ($4,906.30). This sharp drop occurs when cumulative labor hours pass the 720-hour farmer threshold, shifting the marginal labor rate from the farmer's $34.72/hr wage to the temporary labor rate of $17.36/hr (exactly half), thereby temporarily lowering per-bed expansion costs.

![Tomato marginal cost vs. price, standalone](figures/tomato-mc-vs-price.png)
*Figure 1: Tomato marginal cost vs. price (standalone). Shows the crossing between bed 10 and bed 11, and the bed 5→6 dip described above.*

### Reconciling Carrot Marginal Cost Across Standalone and Joint Models
Reconciling the standalone carrot marginal cost chart with the joint-context chart clarifies why carrot expansion remains economically viable under the optimal plan. The standalone carrot chart depicts marginal cost rising above the $2,094.00 market price between beds 10 and 11, peaking at bed 16 before dropping at bed 17. This standalone model assumes carrots hold an isolated allocation of 720 farmer hours.

![Carrot marginal cost vs. price, standalone](figures/carrot-mc-vs-price-standalone.png)
*Figure 2: Carrot marginal cost vs. price (standalone, private 720-hour farmer allocation). MC crosses price between bed 10 and 11, then dips again at bed 16→17.*

In the joint model, however, tomatoes consume the cheap farmer hours first, leaving carrot expansion to be priced entirely at the temporary labor rate. As shown in the joint-context chart, carrot marginal cost remains at $1,688.80 through bed 20—comfortably below the $2,094.00 market price across all beds. This joint curve directly validates the shadow price analysis, confirming that relaxing the carrot bed cap (CAR_MAXBED) to 21 beds yields an additional $352.50 in total profit.

![Carrot marginal cost vs. price, joint context](figures/carrot-mc-vs-price-joint.png)
*Figure 3: Carrot marginal cost vs. price (joint context, TOM=10 and MES=30 held at the optimum). MC stays well under price through bed 20 — the cap binds, not the economics.*

### Shadow Price Optimization and Standalone Shutdown Rule Assessment
Shadow price calculations and individual crop profitability assessments highlight strategic resource allocation and validate production under the economic shutdown rule. Re-optimizing joint production shows positive shadow prices for expanding crop caps—$352.50 for carrots (CAR_MAXBED to 21) and $246.50 for mesclun (MES_MAXBED to 31)—while confirming zero shadow values for total land (60 of 64 beds used) and labor (5,277.2 of 6,480 hours used), meaning neither slack resource justifies additional acquisition expense. Furthermore, standalone crop simulations reveal that tomatoes are profitable in isolation ($6,172.80 net profit at 10 beds), disproving the assumption that every crop loses money alone. While standalone carrots and mesclun operate at net losses, both satisfy the shutdown rule because their
market prices exceed Average Variable Cost at their caps ($2,094.00 price vs. $1,918.45 AVC for carrots; $2,700.00 price vs. $2,430.74 AVC for mesclun), contributing $175.55 and $269.26 per bed toward fixed overhead costs.
