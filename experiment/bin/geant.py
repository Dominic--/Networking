import xml.etree.ElementTree as ET


nodes = {}
f = open("../topology/final/geant-map-number", "r")
line = f.readline()
line = f.readline()
while line:
    s = line.strip().split(' ')
    nodes[s[0]] = int(s[1])

    line = f.readline()
f.close()

n = 0
for month in range(5, 9):
    for day in range(1, 32):
        if month == 5 and day < 4:
            continue
        if month == 6 and day == 31:
            continue

        for hour in range(0, 24):
            if month == 5 and day == 4 and hour < 15:
                continue

            for minute in range(0, 60, 15):
                dom = ET.parse(open("../data/geant/demands/geant-IntraTM-2005-%02d-%02d-%02d-%02d.xml" % (month, day, hour, minute), "r"))
                root = dom.getroot()

                demands = {}
                for src in root.iter('src'):
                    for dst in src.findall('dst'):
                        demands[nodes[src.get('id')],nodes[dst.get('id')]] = dst.text

                f = open("../demand/geant/%d.txt" % n, "w")
                f.write("%d\n" % len(demands))
                for s,d in demands:
                    f.write("%d %d %s\n" % (s, d, demands[s,d]))
                f.close()

                n = n + 1

