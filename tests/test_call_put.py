import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from profitnloss import Call, Put

def test_call():
    c = Call(100, 1)
    assert c.strike == 100
    assert c.premium == 1
    assert c.num_shares == 100

    # TODO: test negative payoffs
    assert c.payoff(101) == 0
    assert c.payoff(100) == -100
    assert c.payoff(0) == -100
    assert c.payoff(math.inf) == math.inf

def test_put():
    p = Put(100, 1)
    assert p.strike == 100
    assert p.premium == 1
    assert p.num_shares == 100

    assert p.payoff(99) == 0
    assert p.payoff(100) == -100
    assert p.payoff(0) == 9900
    assert p.payoff(math.inf) == -100
