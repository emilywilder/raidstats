import os
import json
import argparse
import logging

class RaidStats:
    def __init__(self, raidzlevel=1, mindisks=3, maxdisks=9):
        self.raidzlevel = raidzlevel
        self.mindisks = mindisks
        self.maxdisks = maxdisks
        self.logger = logging.getLogger("RaidStats")
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(message)s")
        console_log = logging.StreamHandler()
        console_log.setFormatter(self.formatter)
        self.logger.addHandler(console_log)

    def _calcstorage(self, disks, size):
        return disks * size - (self.raidzlevel * size)

    def _calccost(self, disks, cost):
        return cost * disks

    def _calccostpertb(self, disks, size, cost):
        return self._calccost(disks, cost) / self._calcstorage(disks, size)

    def printstats(self, devices, csv=False):
        category = json.load(devices)

        logger = self.logger

        formatstring = "{6}, {2} * {5} ({3} TB), {0}, ${1:.2f}, ${4:.2f}"

        if csv:
            devices_filename = os.path.splitext(os.path.basename(devices.name))[0]
            csvfilename = "{0}.csv".format(devices_filename)
            csvlogger = logging.getLogger(csvfilename)
            csvlogger.setLevel(logging.INFO)
            handler = logging.FileHandler(csvfilename, mode='w')
            handler.setFormatter(self.formatter)
            csvlogger.addHandler(handler)
            logger = csvlogger

#        logger.info(category.get("name"))
        logger.info("Category, Configuration (RAIDZ{0}), Redundant Storage (in TB), $USD/TB, Total $USD".format(self.raidzlevel))

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
                    device.get("Model"),
                    category.get("name")))

        if csv:
            written_filename = os.path.basename(logger.handlers[0].stream.name)
            self.logger.info("Wrote {0}".format(written_filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Raid solutions")
    parser.add_argument("devicefile", nargs="+")
    parser.add_argument("--csv", action='store_true', default=False)

    args = parser.parse_args()

    rs = RaidStats(raidzlevel=2, maxdisks=6)
    for devicefile in args.devicefile:
        with open(devicefile, "r") as f:
            rs.printstats(f, csv=args.csv)

