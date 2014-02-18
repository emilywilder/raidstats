class RaidzStats:
    def __init__(self, raidzlevel=1):
        self.raidzlevel = raidzlevel

    def _calcstorage(self, disks, size):
        return disks * size - (self.raidzlevel * size)

    def _calccost(self, disks, size, cost):
        return (cost * disks) / self._calcstorage(disks, size)

    def getstats(self, disks, size, cost):
        print("{2} * {3}TB disks: {0} TB, ${1}/TB".format(
                  self._calcstorage(disks, size),
                  self._calccost(disks, size, cost),
                  disks,
                  size))

if __name__ == "__main__":
    prices = {
        2: 100,
        3: 130,
        4: 180
    }

    rs = RaidzStats(raidzlevel=2)
    for n in xrange(3, 7):
        for s, p in prices.items(): 
            rs.getstats(n, s, p)

