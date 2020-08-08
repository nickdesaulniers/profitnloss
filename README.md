# ProfitNLoss

A library to help calculate max loss, gain, net debit, credit, and break evens
for various options strategies.

## Quick Example

Build a `Strategy` by buying and selling `Call`s and `Put`s.

```python
import profitnloss as pnl

# short christmas tree spread w/ calls
s = pnl.Strategy()
s.sell(pnl.Call(95, 8.4))
s.buy(pnl.Call(105, 2.35))
s.buy(pnl.Call(105, 2.35))
s.buy(pnl.Call(105, 2.35))
s.sell(pnl.Call(110, 0.95))
s.sell(pnl.Call(110, 0.95))

assert s.break_evens() == [98.25, 108.38]
assert s.max_gain() == 325
assert s.max_loss() == -675
assert s.net_cost() == -325
assert s.payoff(0) == 325
assert s.payoff(105) == -675
assert s.payoff(115) == 325
assert s.payoff(math.inf) == 325

print(s.break_evens())
print("max loss: %f, max gain: %f" % (s.max_loss(), s.max_gain()))
print("strikes and payoffs: " + str(list(zip(s.strikes(), s.payoffs(s.strikes())))))

s.plot()
```
```
[98.25, 108.38]
max loss: -675.000000, max gain: 325.000000
strikes and payoffs: [(95.0, 325.0), (105.0, -675.0), (110.0, 325.0)]
```
![Profit and Loss Diagram](example.png?raw=true "Profit and Loss Diagram")

## API

One of the things curious about this design is that options contracts generally
have 6 traits:
1. Symbol of the underlying asset being tracked.
2. Expiration date.
3. Strike price (agreed upon future value of the underlying to potentially
   exercise the rights of the agreement at.)
4. Type (Call or Put).
5. Premium paid from buyer to seller.
6. Whether the contract is being bought or sold.

You can calculate profit and loss diagrams for most strategies given everything
but the first two. See the FAQ section at the bottom for more info.

For this library, the two contract classes (`Call` and `Put`) don't track
whether they're bought or sold, instead `buy`ing and `sell`ing are methods on a
`Strategy` class. The contract type is implied by the class, so constructing
an options contract with this library only involves explicitly supplying the
`strike` and `premium`.

### Call

A call option. Doesn't track a symbol. Doesn't track whether bought or sold;
instead strategies do.

`Call` constructor, parameters:
1. `strike`: `float` the strike price in dollars.
2. `premium`: `float` the value of the contract.
3. `num_shares`: `int` (optional; default `100`) number of shares tracked.

Methods:
`payoff` returns the profit (if positive) or loss (if negative) of the contract
from the buyers perspective as a `float`, parameters:
1. `spot`: `float` the stock price at evaluation.

`break_even` returns the break even point of the contract as `float`.

### Put

A put option. Doesn't track a symbol. Doesn't track whether bought or sold;
instead strategies do.

`Put` constructor, parameters:
1. `strike`: `float` the strike price in dollars.
2. `premium`: `float` the value of the contract.
3. `num_shares`: `int` (optional; default `100`) number of shares tracked.

Methods:
`payoff` returns the profit (if positive) or loss (if negative) of the contract
from the buyers perspective as a `float`, parameters:
1. `spot`: `float` the stock price at expiration.

`break_even` returns the break even point of the contract as `float`.

### Strategy

A set of purchased and sold `Call` and `Put` contracts.

`Strategy` constructor has no parameters.

Methods:
`buy` purchase a contract. No return value. Parameters:
1. `contract`: either a `Call` or a `Put`.

`sell` write a contract. No return value. Parameters:
1. `contract`: either a `Call` or a `Put`.

`strikes`: returns a sorted list of the unique strike prices (as `floats`) in
the `Strategy`.  No parameters.

`payoff_precise`: returns the payoff at a given `spot` without any rounding
applied, so you can get interesting IEEE754 values for non-power-of-two (NPOT)
values. Useful when numerical precision is required, such as when calculating
roots. Note that the payoff is multiplied by the number of shares controlled.
Parameters:
1. `spot`: `float` the stock price at expiration.

`payoff`: retuns the payoff at a given `spot` rounded to two decimal places.
Parameters:
1. `spot`: `float` the stock price at expiration.

`payoffs`: returns a list of the payoffs for the given `spots` rounded to two
decimal places.
1. `spots`: `[float]` the stock prices at evaluation.

`net_cost`: returns the total credits minus debits from each contract's
premiums, multiplied by the number of shares per contract (default `100`) then
rounded to two decimal places (as `float`). A net long position will have a
positive `net_cost` while a net short position will have a negative `net_cost`.
No parameters.

`break_evens`: returns the break even points of the strategy as a `[float]`
where each point has been rounded to two decimal places. No parameters.

`max_loss`: returns the largest possible deficit for the position as `float`
rounded to two decimal places. No Parameters.

`max_gain`: returns the largest possible profit for the position as `float`
rounded to two decimal places. No Parameters.

`plot`: a very simple method that uses `matplotlib` to plot the basic profit
and loss diagram. You can easily do better, using the above methods. No
parameters.

## License

Apache 2.0

## FAQ
- Q: Why no horizontal ("calendar") or diagonal spreads?
  - A: Because the break evens depend on implied volatility, which requires an
    underlying and exercise type.  I'm working on that, but not for v1.
- Q: Is that a graph with unlabeled axes? And you call yourself an engineer!
  - A: Plot it yourself then; I've given you the tools to do so here!
- Q: Did you name the library specifically for it to be `import`ed `as pnl`? Do
  you think you're funny?
  - A: Yes.
