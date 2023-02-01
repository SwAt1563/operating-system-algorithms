

class TimeByCycles:

    @classmethod
    def from_time_to_cycles(cls, t):
        return t * 1000

    @classmethod
    def from_cycles_to_time(cls, c):
        return c / 1000

