class RaidzStats:
    def __init__(self, raidzlevel=1, mindisks=3, maxdisks=9):
        self.raidzlevel = raidzlevel
        self.prices = {
            2: 100,
            3: 130,
            4: 180
        }
        self.mindisks = mindisks
        self.maxdisks = maxdisks

    def _calcstorage(self, disks, size):
        return disks * size - (self.raidzlevel * size)

    def _calccost(self, disks, cost):
        return cost * disks

    def _calccostpertb(self, disks, size, cost):
        return self._calccost(disks, cost) / self._calcstorage(disks, size)

    def printstats(self, csv=False):
        formatstring = "{2} * {3} TB disks: {0} TB, ${1}/TB, ${4}"
        if csv:
            print("Configuration (RAIDZ{0}),Redundant Storage (in TB),$USD/TB,Total $USD".format(self.raidzlevel))
            formatstring = "{2}*{3} TB disks,{0},${1},${4}"

        for disks in xrange(self.mindisks, self.maxdisks+1):
            for size, cost in self.prices.items(): 
                print(formatstring.format(
                    self._calcstorage(disks, size),
                    self._calccostpertb(disks, size, cost),
                    disks,
                    size,
                    self._calccost(disks, cost)))

if __name__ == "__main__":
    rs = RaidzStats(raidzlevel=1, maxdisks=6)
    rs.printstats(csv=True)

