# financial pyramid modelling, based on known properties of chaotic maps (logistic map)
# Budnik Andrew, 2013.  Public domain.

import random
import math
import matplotlib.pyplot as plt

R_START = 2.8
R_MAX = 4.0
R = R_START
START_COEFF = 0.35
AVG_PERCENT = 0.35

R_INCR_SPEED = ( ((2.0, 3.0), 0.01), ((3.0, 1.0 + math.sqrt(6.0)), 0.02), ((1.0 + math.sqrt(6.0), 4.0), 0.03) )


def InvC(c):
    return 1.0 - c

def NextCoeff(c):
    return R * c * InvC(c)

class Player():
    def __init__(self):
        min_money_in, max_money_in = 100, 1000
        self.input_m = random.randint(min_money_in, max_money_in)
        self.buffer_m = self.input_m
        self.payoff_m = 0.0
        multiplier = [1.0/10.0, 1.0/20.0, 1.0/30.0] # 10, 20, 30 days deposits
        self.t = random.randint(0, 2) # deposit type: 0=10, 1=20, 2=30 (type=days)
        self.m = multiplier[ self.t ]
        self.coeff = START_COEFF

    def GetInputMoney(self):
        return self.input_m

    def GetBuffer(self):
        return self.buffer_m

    def MoveMoneyFromBufferToPayoffs(self):
        m = self.input_m * self.m
        self.payoff_m += m
        self.buffer_m -= m

    def GetPayoff(self):
        return self.payoff_m * self.GetPercent()

    def GetPercent(self):
        return self.coeff + AVG_PERCENT + self.t * 0.02

    def GetCoeff(self):
        return self.coeff

    def SetCoeff(self, coeff):
        self.coeff = coeff

class PayoffComputer():
    def Compute(self, player):
        buffer = player.GetBuffer()
        if buffer > 0.0:
            player.MoveMoneyFromBufferToPayoffs()
            coeff = player.GetCoeff()
            coeff = NextCoeff(coeff)
            player.SetCoeff(coeff)

class System():
    def __init__(self):
        print '================'
        self.players = []
        self.total_input_money = 0.0
        self.InitStats()

    def InitStats(self):
        self.avg_buffers = []
        self.avg_payoffs = []
        self.profit_m = []
        self.lose_m = []
        self.max_profit = []
        self.max_lose = []
        self.avg_percent = []
        self.num_players = []
        self.num_profit_players = []
        self.num_lose_players = []

    def CanIncreaseR(self):
        return R < R_MAX

    def NonEmptyBufferExists(self):
        for p in self.players:
            if p.GetBuffer() > 0.0:
                return True
        return False

    def AddPlayers(self, players):
        for p in players: self.total_input_money += p.input_m
        self.players.extend(players)

    def ComputePayoffs(self):
        comp = PayoffComputer()
        for p in self.players:
            comp.Compute(p)

    def GetTotalInputMoney(self):
        return self.total_input_money

    def GetTotalPayoffs(self):
        payoffs = 0.0
        for p in self.players: payoffs += p.GetPayoff()
        return payoffs

    def UpdateStats(self, day):
        avg_buffers = avg_payoffs = avg_percent = 0.0
        profit_m = lose_m = 0.0
        max_profit = max_lose = 0.0
        num_profit_players = num_lose_players = 0
        for p in self.players:
            avg_buffers += p.GetBuffer()
            avg_payoffs += p.GetPayoff()
            avg_percent += p.GetPercent()

            if p.GetBuffer() <= 0.0:
                if p.GetPercent() > 1.0:
                    num_profit_players += 1
                else:
                    num_lose_players += 1
                
                delta = p.GetPayoff() - p.GetInputMoney()
                if delta > 0.0:
                    if delta > max_profit: max_profit = delta
                    profit_m += delta
                else:
                    if -delta > max_lose: max_lose = -delta
                    lose_m -= delta

        num = len( self.players )
        self.avg_buffers.append( avg_buffers / num )
        self.avg_payoffs.append( avg_payoffs / num )
        self.profit_m.append( profit_m )
        self.lose_m.append( lose_m )
        self.max_profit.append( max_profit )
        self.max_lose.append( max_lose )

        self.avg_percent.append( avg_percent / num )

        self.num_players.append( len(self.players) )
        self.num_profit_players.append( num_profit_players )
        self.num_lose_players.append( num_lose_players )

    def GetDelta(self):
        return self.GetTotalInputMoney() - self.GetTotalPayoffs()

    def GetMinPercentDay(self):
        best_day = day = 0
        percent = self.avg_percent[0]
        for p in self.avg_percent:
            if p > percent:
                percent = p
                best_day = day

            day += 1
        return best_day

    def ShowStatsGraph(self, days):
        p1, = plt.plot(days, self.avg_buffers, 'ko', markersize=1)
        p2, = plt.plot(days, self.avg_payoffs, 'ro', markersize=5)
        plt.legend([p2, p1], ["average payoff", "average buffer"], loc=2)
        plt.show()

        p1, = plt.plot(days, self.profit_m, 'ko', markersize=1)
        p2, = plt.plot(days, self.lose_m, 'ro', markersize=5)
        plt.legend([p2, p1], ["player lose", "player profit"], loc=2)
        plt.show()

        p1, = plt.plot(days, self.max_profit, 'ko', markersize=1)
        p2, = plt.plot(days, self.max_lose, 'ro', markersize=5)
        plt.legend([p2, p1], ["max player lose", "max player profit"], loc=2)
        plt.show()

        day = 0
        for p in self.avg_percent:
            if p < 1.0: break
            day += 1
        print 'first day of negative percent is', day

        day = max_avg_percent_day = 0
        percent = self.avg_percent[0]
        for p in self.avg_percent:
            if p > percent: percent = p; max_avg_percent_day = day
            day += 1
        print 'max avg percent day is', max_avg_percent_day, '(', percent, ')'

        print 'start percent =', self.avg_percent[0]
        print 'end percent   =', self.avg_percent[len(self.avg_percent)-1]

        p1, = plt.plot(days, self.avg_percent, 'mo', markersize=3)
        plt.legend([p1], ["average percent"])
        plt.show()

        print 'num players =', len(self.players)
        p1, = plt.plot(days, self.num_players, 'ko', markersize=1)
        p2, = plt.plot(days, self.num_lose_players, 'ro', markersize=3)
        p3, = plt.plot(days, self.num_profit_players, 'go', markersize=3)
        plt.legend([p3, p2, p1], ["profit players", "lose players", "total players"], loc=2)
        plt.show()

    def PrintStats(self):
        delta = self.GetDelta()
        print 'Total Input   :', self.GetTotalInputMoney()
        print 'Total Payoffs :', self.GetTotalPayoffs()
        print '--------'
        print 'delta =', delta, '(', delta / self.GetTotalInputMoney(), ')'
        print '--------'

def GetNewPlayersStat(day):
    #return 30, 10  # simplification: no functional dependency
    if 0  <= day < 15: return 10, 5
    if 15 <= day < 30: return 20, 10
    if 30 <= day < 50: return 25, 5
    if 50 <= day < 60: return 30, 5
    if 60 <= day < 75: return 15, 5
    return 10, 5

def AddNewPlayers(sys, day):
    avg_new_players_per_day, dispersion_new_players_per_day = GetNewPlayersStat(day)

    num_new_players = random.randint(avg_new_players_per_day - dispersion_new_players_per_day,
                                     avg_new_players_per_day + dispersion_new_players_per_day)
    
    sys.AddPlayers( [Player() for i in range(0, num_new_players)] )

def GetRStep():
    global R
    for pair in R_INCR_SPEED:
        r = pair[0]
        if r[0] <= R < r[1]:
            return pair[1]
    print 'warning: using default r step'
    return 0.01

def TestSystem(sys):
    day = 0
    global R
    R = R_START

    # phase 1. New deposits are available, num of players increasing
    while sys.CanIncreaseR():
        AddNewPlayers(sys, day)
        sys.ComputePayoffs()
        sys.UpdateStats(day)
        R += GetRStep()
        day += 1
        #print 'day', day
        #sys.PrintStats()

    if R > 4.0: R = 4.0

    phase1_days = day
    print 'phase 1 =', phase1_days, 'days'

    # phase 2. New deposits are not available, num of players can be less or equal than current players
    while sys.NonEmptyBufferExists():
        sys.ComputePayoffs()
        sys.UpdateStats(day)
        day += 1

    print 'phase 2 =', day - phase1_days, 'days'
    return day

def Main():
    sys = System()
    day = TestSystem(sys)
    sys.PrintStats()
    sys.ShowStatsGraph(range(0,day))

Main()
