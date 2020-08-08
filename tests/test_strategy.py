import math
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from profitnloss import Call, Put, Strategy

@pytest.fixture
def s(): return Strategy()

def test_long_call(s):
    s.buy(Call(320, 30))
    assert s.break_evens() == [350]
    assert s.max_gain() == math.inf
    assert s.max_loss() == -3000
    assert s.net_cost() == 3000
    assert s.payoff(0) == -3000
    assert s.payoff(350) == 0
    assert s.payoff(math.inf) == math.inf

def test_short_call(s):
    s.sell(Call(100, 1))
    assert s.break_evens() == [101]
    assert s.max_gain() == 100
    assert s.max_loss() == -math.inf
    assert s.net_cost() == -100
    assert s.payoff(0) == 100
    assert s.payoff(100) == 100
    assert s.payoff(101) == 0
    assert s.payoff(99) == 100
    assert s.payoff(math.inf) == -math.inf

def test_long_put(s):
    s.buy(Put(400, 23))
    assert s.break_evens() == [377]
    assert s.max_gain() == 37700
    assert s.max_loss() == -2300
    assert s.net_cost() == 2300
    assert s.payoff(0) == 37700
    assert s.payoff(377) == 0
    assert s.payoff(math.inf) == -2300

def test_short_put(s):
    s.sell(Put(200, 2.2))
    assert s.break_evens() == [197.8]
    assert s.max_gain() == 220
    assert s.max_loss() == -19780
    assert s.net_cost() == -220
    assert s.payoff(0) == -19780
    assert s.payoff(197.8) == 0
    assert s.payoff(math.inf) == 220

# aka bull call spread
def test_debit_spread(s):
    s.buy(Call(100, 3.3))
    s.sell(Call(105, 1.5))
    assert s.break_evens() == [101.8]
    assert s.max_gain() == 320
    assert s.max_loss() == -180
    assert s.net_cost() == 180
    assert s.payoff(0) == -180
    assert s.payoff(101.8) == 0
    assert s.payoff(math.inf) == 320

# aka bear call spread
def test_credit_spread(s):
    s.sell(Call(100, 3.3))
    s.buy(Call(105, 1.5))
    assert s.break_evens() == [101.8]
    assert s.max_gain() == 180
    assert s.max_loss() == -320
    assert s.net_cost() == -180
    assert s.payoff(0) == 180
    assert s.payoff(101.8) == 0
    assert s.payoff(math.inf) == -320

def test_short_iron_condor(s):
    s.buy(Put(95, 0.7))
    s.sell(Put(100, 2.1))
    s.sell(Call(105, 2.35))
    s.buy(Call(110, 0.95))
    assert s.break_evens() == [97.2, 107.8]
    assert s.max_gain() == 280
    assert s.max_loss() == -220
    assert s.net_cost() == -280
    assert s.payoff(0) == -220
    assert s.payoff(107.8) == 0
    assert s.payoff(120) == -220
    assert s.payoff(97.2) == 0
    assert s.payoff(math.inf) == -220

def test_long_iron_butterfly(s):
    s.sell(Put(95, 1.2))
    s.buy(Put(100, 3.2))
    s.buy(Call(100, 3.3))
    s.sell(Call(105, 1.4))
    assert s.break_evens() == [96.1, 103.9]
    assert s.max_gain() == 110
    assert s.max_loss() == -390
    assert s.net_cost() == 390
    assert s.payoff(0) == 110
    assert s.payoff(100) == -390
    assert s.payoff(103.9) == 0
    assert s.payoff(110) == 110
    assert s.payoff(96.1) == 0
    assert s.payoff(math.inf) == 110

def test_short_christmas_tree_w_calls(s):
    s.sell(Call(95, 8.4))
    s.buy(Call(105, 2.35))
    s.buy(Call(105, 2.35))
    s.buy(Call(105, 2.35))
    s.sell(Call(110, 0.95))
    s.sell(Call(110, 0.95))
    assert s.break_evens() == [98.25, 108.38]
    assert s.max_gain() == 325
    assert s.max_loss() == -675
    assert s.net_cost() == -325
    assert s.payoff(0) == 325
    assert s.payoff(105) == -675
    assert s.payoff(115) == 325
    assert s.payoff(math.inf) == 325

def test_three_long_calls(s):
    s.buy(Call(100, 8))
    s.buy(Call(105, 6))
    s.buy(Call(110, 4))
    assert s.break_evens() == [111.0]

def test_bull_split_synthetic(s):
    s.buy(Call(100, 12))
    s.sell(Put(101, 11.5))
    assert s.payoff(math.inf) == math.inf

def test_long_synthetic(s):
    s.buy(Call(100, 3.53))
    s.sell(Put(100, 3.44))
    assert s.break_evens() == [100.09]
    assert s.max_gain() == math.inf
    assert s.payoff(100.09) == 0
