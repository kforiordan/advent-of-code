#!/usr/bin/env python

import sys
import re

def y_distance(a, b):
    return abs(a["y"] - b["y"])

def x_distance(a, b):
    return abs(a["x"] - b["x"])

# Manhattan distance, or taxicab distance.
def manhattan_distance(a, b):
    return y_distance(a, b) + x_distance(a, b)

# Not sure we'll need this function
def manhattan_area(d):
    # Four times the triangular number series sum
    return int(4 * ((d * (d+1)) / 2))


# Not sure we'll need this either, so leaving it as is.
def exclusion_zone(sensor):
    # Start with the positions at the same or less manhattan distance
    # from the sensor as its nearest becon.
    dist = manhattan(sensor, beacons[sensor["beacon"]])
    area = manhattan_area(dist)

    # Now subtract 1: the beacon itself
    area -= 1

    # Now subtract any sensors that are within this area:

    # And what remains is the exclusion area size .. oh wait, we were
    # not asked to calculate this.
    return area


def get_sensors_and_beacons(fh):
    sensors = []
    beacons = []

    idx = 0
    for line in fh:
        line = line.rstrip('\n')
        sensor_re = re.compile('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)')
        m = sensor_re.match(line)
        if m:
            sx, sy, bx, by = map(int, [m.group(1), m.group(2), m.group(3), m.group(4)])
            sensor = {"x":sx, "y":sy, "beacon":idx}
            # This is a bit broken.  Many sensors may detect the same
            # beacon, so the same beacon may appear multiple times in
            # the beacons list.  It's ok for now though.
            beacon = {"x":bx, "y":by, "sensor":idx}
            sensor["beacon_distance"] = manhattan_distance(sensor, beacon)
            sensors.append(sensor)
            beacons.append(beacon)
            idx += 1

    return (sensors, beacons)


def linear_exclusions_y(y):
    exclusion_ranges = []

    for sensor in sensors:
        # Distance from sensor to y-line
        ydiff = sensor["y"] - y

        # If y-line is further away then our nearest beacon, move on.
        if abs(ydiff) > sensor["beacon_distance"]:
            continue

        # This is the range, from x1 to x2, of squares at that yline
        # which we can exclude.
        x1 = sensor["x"] - (sensor["beacon_distance"] - abs(ydiff))
        x2 = sensor["x"] + (sensor["beacon_distance"] - abs(ydiff))

        # If the a beacon is present in our possible exclusion range,
        # shorten the range (such a beacon will always be at an edge)
        beacon = beacons[sensor["beacon"]]
        if beacon["y"] == y:
            if beacon["x"] == x1:
                x1 += 1
            elif beacon["x"] == x2:
                x2 -= 1
            else:
                print("oh no")
                exit(0)
            if x1 > x2:
                continue

        exclusion_ranges.append((x1,x2))

    # Ok, so now we have a bunch of overlapping exclusion ranges
    n_changes = 0
    while True:
        for i in range(len(exclusion_ranges)):
            if exclusion_ranges[i] == None:
                continue
            x1,x2 = exclusion_ranges[i]
            for j in range(len(exclusion_ranges)):
                if i == j or exclusion_ranges[j] == None:
                    continue
                x3,x4 = exclusion_ranges[j]
                if x1 <= x3:
                    if x2 >= x4:
                        exclusion_ranges[j] = None
                        n_changes += 1
                    elif x2 >= x3:
                        exclusion_ranges[i] = (x1,x4)
                        exclusion_ranges[j] = None
                        n_changes += 1
                elif x3 <= x1:
                    if x4 >= x2:
                        exclusion_ranges[i] = None
                        n_changes += 1
                    elif x4 >= x1:
                        exclusion_ranges[i] = None
                        exclusion_ranges[j] = (x3,x2)
                        n_changes += 1

        if n_changes == 0:
            break
        n_changes = 0

    return [r for r in exclusion_ranges if r != None]


if __name__ == "__main__":
    (sensors, beacons) = get_sensors_and_beacons(sys.stdin)

    t = 0
    for r in linear_exclusions_y(2000000):
        x1,x2 = r
        t += (x2 - x1) + 1
    print("Silver: {}".format(t))
