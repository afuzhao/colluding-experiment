# Mathematical foundations and verification

These calculations describe the implemented payoff functions. They do not assert that language-model agents optimize them or play equilibrium strategies. The reproducible checker in [tools/build_evidence.py](tools/build_evidence.py) imports the actual economics and saves [all numerical checks](data/mathematical_checks.json), including exhaustive pure-strategy equilibrium searches on the configured grids. It makes no model calls.

## 1 Quantity market E1

Three firms choose integers $q_i\in\{0,\ldots,40\}$. With $Q=\sum_iq_i$,

$$P(Q)=\max(0,100-Q),\qquad \pi_i=(P(Q)-4)q_i.$$

The truncation matters for very large output: producing when price is below cost can lose money. In the positive-price region, holding rival output $S_i=\sum_{j\ne i}q_j$ fixed,

$$\pi_i=(96-S_i-q_i)q_i,\quad \frac{\partial\pi_i}{\partial q_i}=96-S_i-2q_i.$$

The continuous best response is $(96-S_i)/2$, projected onto the allowed range; the integer solution must compare adjacent grid values and retain ties. At the symmetric interior solution, $q=(96-2q)/2$, giving $q=24$, $P=28$, and profit576 each.

**Integer qualification:** exhaustive checking finds seven pure-strategy stage equilibria: $(24,24,24)$ and the six permutations of $(23,24,25)$. All have total output72 and price28, but individual profits differ. The familiar symmetric Cournot benchmark is therefore not the unique pure equilibrium of the implemented integer game. This distinction matters for claims about finite repeated games.

Joint industry profit in the relevant region is

$$\Pi(Q)=(96-Q)Q=2304-(Q-48)^2.$$

It is maximized at $Q=48$. The symmetric joint-output allocation is $(16,16,16)$, with price52 and profit768 each. Total-profit maximization does not select a unique split of that total: $(8,8,32)$ also totals48 and yields profits384,384,1536. Thus E1's unequal offer redistributes the same total profit2304 while favoring C.

If the other two firms remain at16, a unilateral best response is32, earning1024 rather than768. A verbal cartel agreement therefore has a one-period deviation incentive; a cooperative prompt does not remove it from the payoff function.

### Competitive C and the observed zero-profit window

| Quantities A B C | Price | Profits A B C | Meaning |
|---|---:|---|---|
|16 16 16|52|768 768 768|Symmetric joint-output benchmark|
|16 16 32|36|512 512 1024|Only C expands; A/B can still earn positive profit|
|32 32 32|4|0 0 0|Observed suppression endpoint in Sumin's action-only rounds 10–13|
|16 32 32|20|256 512 512|A has a profitable deviation from the zero-profit profile|

When B=C=32, A's best response is16, not32. When B=16 and C=32, A's best response is24, earning576. Consequently C's expansion mechanically lowers price for given A/B quantities, but A/B escalation to32 is an empirical response, not a theorem of profit maximization.

With C fixed32 and A/B combined output $s$, their joint profit is $(64-s)s$, maximized at $s=32$. Splitting that as16 each gives512 each. A profitable A/B partial agreement remains mathematically possible in E1; C's competition does not create a structural impossibility of coordination.

For a linear inverse demand curve, recorded consumer surplus is $CS=Q^2/2$ in these positive-price examples. At total96, price equals cost4 and $CS=4608$, while profits are zero. This is the aggregate efficient-output quantity for identical constant costs, even though each firm choosing32 is not an individual Cournot equilibrium. Economic welfare and individual strategic optimality are distinct.

## 2 Differentiated-price market E2

Prices are integers $p_i\in\{4,\ldots,84\}$, with unit cost4. Consumers choose nonnegative quantities to maximize utility less expenditure:

$$U(\mathbf q)=124Q-\frac{0.75}{2}\sum_iq_i^2-\frac{0.75}{2}Q^2,\qquad Q=\sum_iq_i.$$

For an active product, the first-order condition is

$$p_i=124-0.75q_i-0.75Q.$$

When all three products sell positive quantities, solving gives

$$q_i=40-(p_i-4)+\frac{(p_j-4)+(p_k-4)}{3}.$$

Demand is not independently clipped at zero. The implemented active-set solver removes products whose prices exceed the active demand threshold and resolves the remaining system. All best-response and unequal-offer numbers below use that solver, including grid boundaries.

Firm profit is $\pi_i=(p_i-4)q_i$. Holding rival prices fixed in the three-active region, $dq_i/dp_i=-1$, so the interior best-response condition is $q_i=p_i-4$. With equal prices $p$, demand is $(124-p)/3$; solving $(124-p)/3=p-4$ gives $p=34$, quantity30 and profit900 each. Exhaustive checking of all integer profiles finds exactly one **pure-strategy** stage equilibrium, $(34,34,34)$; this is not a separate claim that mixed equilibria have been enumerated.

### Joint pricing

Using inverse demand, total producer profit can be written in quantities as

$$\Pi=120Q-0.75\sum_iq_i^2-0.75Q^2.$$

Since $\sum_iq_i^2\ge Q^2/3$,

$$\Pi\le120Q-Q^2=3600-(Q-60)^2.$$

The bound is attained at equal quantities20, hence prices64 and profits1200 each. The configured price grid includes that solution. This verifies a global joint-profit benchmark, not a Nash equilibrium: against rival prices64, own price44 yields quantity40 and profit1600.

### Partial coalition and unequal package

Against C fixed at37, a symmetric A/B price $x$ gives

$$q_A=q_B=\frac{161}{3}-\frac{2x}{3}.$$

Maximizing the A/B joint profit gives continuous $x=42.25$; exhaustive two-dimensional grid optimization gives the equal integer pair42/42. C's continuous best response against42/42 is $110/3$, with grid best response37. The resulting profits are approximately975.333,975.333,1067. Conditional independent A/B pricing against C=37 has the checked grid equilibrium35/35. Thus A/B joint pricing can be profitable even with independently pricing C; whether agents actually sustain it requires empirical qualification.

The elicitation offer76/76/52 gives quantities8,8,40 and profits576,576,1920. Its total3072 is **lower** than3600 at equal joint pricing. It is not E1's fixed-total redistribution and cannot be treated as a purely linguistic translation.

The transaction price is sales weighted:

$$\bar p=\frac{\sum_i p_iq_i}{\sum_iq_i}.$$

If A/B stay64 and C changes to52, sales become16,16,32, so the transaction price falls to58 while A/B prices do not change. This is why a lower price index alone cannot identify A/B coordination breakdown. Consumer surplus is $0.375\sum_iq_i^2+0.375Q^2$; it is1800 at64each and2112 at64/64/52.

## 3 Repeated incentives and limits of equilibrium language

A Nash equilibrium is a mutual best-response profile, rather than any price profile described as cooperative or competitive. See the original definition in [Nash's dissertation](https://library.princeton.edu/sites/g/files/toruqf6021/files/documents/Non-Cooperative_Games_Nash.pdf), particularly its equilibrium definition.

An instructive **infinite-horizon** grim-trigger calculation uses cooperative payoff $\pi^C$, one-period deviation payoff $\pi^D$ and subsequent symmetric stage-equilibrium payoff $\pi^N$:

$$\frac{\pi^C}{1-\delta}\ge\pi^D+\frac{\delta\pi^N}{1-\delta}
\quad\Longleftrightarrow\quad
\delta\ge\frac{\pi^D-\pi^C}{\pi^D-\pi^N}.$$

E1 has $(\pi^C,\pi^D,\pi^N)=(768,1024,576)$; E2 has $(1200,1600,900)$. Both yield $\delta\ge4/7$. Their symmetric benchmark incentive ratios therefore match, despite different quantities, prices and coalition structures.

This is an explanatory comparison, not an equilibrium proof for our known 15-round studies. Standard finite-horizon unraveling arguments require assumptions about continuation equilibrium and rationality; multiple stage equilibria can change the argument. [MIT's repeated-games notes](https://ocw.mit.edu/courses/14-12-economic-applications-of-game-theory-fall-2025/mit14_12f12_chapter12_f12.pdf) explicitly separate finite and infinite repetition and discuss the role of equilibrium multiplicity. The actual E1 grid has multiple pure equilibria. The agents also receive cooperative-owner guidance and are not verified optimizers. We therefore do not label their finite-horizon cartel play an equilibrium merely because it persists or invoke an infinite-horizon theorem to justify it.
