#! /usr/bin/env python3
from profitnloss import Call, Put, Strategy

# short christmas tree spread w/ calls
s = Strategy()
s.sell(Call(95, 8.4))
s.buy(Call(105, 2.35))
s.buy(Call(105, 2.35))
s.buy(Call(105, 2.35))
s.sell(Call(110, 0.95))
s.sell(Call(110, 0.95))

print(s.break_evens())
print("max loss: %f, max gain: %f" % (s.max_loss(), s.max_gain()))
print("strikes and payoffs: " + str(list(zip(s.strikes(), s.payoffs(s.strikes())))))
s.plot()
