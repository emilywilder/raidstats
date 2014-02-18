class RaidzStats:
    def __init__(self, raidzlevel=1):
        self.raidzlevel = raidzlevel

    def _calcstorage(self, disks, size):
        return disks * size - (self.raidzlevel * size)

    def _calccost(self, disks, cost):
        return cost * disks

    def _calccostpertb(self, disks, size, cost):
        return self._calccost(disks, cost) / self._calcstorage(disks, size)

    def getstats(self, disks, size, cost):
        print("{2} * {3} TB disks: {0} TB, ${1}/TB, ${4}".format(
                  self._calcstorage(disks, size),
                  self._calccostpertb(disks, size, cost),
                  disks,
                  size,
                  self._calccost(disks, cost)))

if __name__ == "__main__":
    prices = {
        2: 100,
        3: 130,
        4: 180
    }

    rs = RaidzStats(raidzlevel=2)
    for n in xrange(3, 10):
        for s, p in prices.items(): 
            rs.getstats(n, s, p)

