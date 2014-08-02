import json
import argparse
import logging

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

        logger = logging.getLogger("printstats")
        logger.setLevel(logging.INFO)
        log_formatter = logging.Formatter("%(message)s")
        formatstring = "{2} * {5} ({3} TB): {0} TB, ${1:,.2f}/TB, ${4:,.2f}"

        if csv:
            csvlog = logging.FileHandler("raidstats.csv", mode='w')
            csvlog.setFormatter(log_formatter)
            logger.addHandler(csvlog)

            logger.info("Configuration (RAIDZ{0}),Redundant Storage (in TB),$USD/TB,Total $USD".format(self.raidzlevel))
            formatstring = "{2}*{5} ({3} TB),{0},${1:.2f},${4:.2f}"
        else:
            console_log = logging.StreamHandler()
            console_log.setFormatter(log_formatter)
            logger.addHandler(console_log)

        for category in devices.get("raidstats"):
            for device in category.get("devices"):
                for disks in range(self.mindisks, self.maxdisks+1):
                    size = device.get("Size")
                    cost = device.get("Price")
                    logger.info(formatstring.format(
                        self._calcstorage(disks, size),
                        self._calccostpertb(disks, size, cost),
                        disks,
                        size,
                        self._calccost(disks, cost),
                        device.get("Model")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Raid solutions")
    parser.add_argument("devicefile", nargs="+")
    parser.add_argument("--csv", action='store_true', default=False)

    args = parser.parse_args()

    rs = RaidzStats(raidzlevel=2, maxdisks=6)
    for devicefile in args.devicefile:
        with open(devicefile, "r") as f:
            rs.printstats(f, csv=args.csv)

