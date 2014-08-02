import json
import argparse

class RaidzStats:
    def __init__(self, raidzlevel=1, mindisks=3, maxdisks=9):
        self.raidzlevel = raidzlevel
        self.mindisks = mindisks
        self.maxdisks = maxdisks

    def _calcstorage(self, disks, size):
        return disks * size - (self.raidzlevel * size)

    def _calccost(self, disks, cost):
        return cost * disks

    def _calccostpertb(self, disks, size, cost):
        return self._calccost(disks, cost) / self._calcstorage(disks, size)

    def printstats(self, devices, csv=False):
        devices = json.load(devices)
        formatstring = "{2} * {5} ({3} TB): {0} TB, ${1:,.2f}/TB, ${4:,.2f}"
        if csv:
            print("Configuration (RAIDZ{0}),Redundant Storage (in TB),$USD/TB,Total $USD".format(self.raidzlevel))
            formatstring = "{2}*{5} ({3} TB),{0},${1:.2f},${4:.2f}"

        for category in devices.get("raidstats"):
            for device in category.get("devices"):
                for disks in range(self.mindisks, self.maxdisks+1):
                    size = device.get("Size")
                    cost = device.get("Price")
                    print(formatstring.format(
                        self._calcstorage(disks, size),
                        self._calccostpertb(disks, size, cost),
                        disks,
                        size,
                        self._calccost(disks, cost),
                        device.get("Model")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Raid solutions")
    parser.add_argument("devicefile")
    parser.add_argument("--csv", action='store_true', default=False)

    args = parser.parse_args()

    rs = RaidzStats(raidzlevel=2, maxdisks=6)
    with open(args.devicefile, "r") as f:
        rs.printstats(f, csv=args.csv)

