import pprint

class Parser:
    def __init__(self, f):
        self.config = None
        self.passengers = []
        self.timeline_latest_finish = []
        self.timeline_earliest_start = []

        self.parse(f)

    def parse(self, f):
        with open(f, 'r') as infile:
            self.config = parseConfigLine(next(infile))

            self.timeline_earliest_start = [[] for i in range(0, self.config['steps'])]
            self.timeline_latest_finish = [[] for i in range(0, self.config['steps'])]

            id = 0
            for l in infile:
                passenger = parsePassengerLine(l, id)
                if passenger['distance'] > (passenger['latest_finish'] - passenger['earliest_start']):
                    print('Skipping undeliverable passenger %s' %passenger)
                    continue

                self.passengers.append(passenger)
                self.timelineAdd(id)
                id += 1

    def timelineAdd(self, pid):
        passenger = self.passengers[pid]
        self.timeline_earliest_start[passenger['earliest_start']].append(pid)
        self.timeline_latest_finish[passenger['latest_finish']].append(pid)

    def __repr__(self):
        s = 'config: %s\npassengers: %s\ntimeline_latest_finish: %s\ntimeline_earliest_start: %s' % (
                str(self.config),
                pprint.pformat(self.passengers),
                str(self.timeline_latest_finish),
                str(self.timeline_earliest_start)
            )
        return s

def parseConfigLine(line):
    splitted_line = splitLineToInts(line)
    return {
        'grid_size': parseCoordinate(splitted_line[0], splitted_line[1]),
        'num_vehicles': splitted_line[2],
        'num_rides': splitted_line[3],
        'bonus': splitted_line[4],
        'steps': splitted_line[5]
    }


def parsePassengerLine(line, id):
    splitted_line = splitLineToInts(line)
    start_point = parseCoordinate(splitted_line[0], splitted_line[1])
    end_point = parseCoordinate(splitted_line[2], splitted_line[3])
    return {
        'id': id,
        'start_point': start_point,
        'end_point': end_point,
        'earliest_start': splitted_line[4],
        'latest_finish': splitted_line[5],
        'distance': calcDistance(start_point, end_point)
    }

def calcDistance(a, b):
    """
    Calculate a distance between two coordinates

    Tests:
        >>> calcDistance((1, 3), (4, 6))
        6
        >>> calcDistance((-1, -1), (-4, -6))
        8
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def parseCoordinate(x, y):
    return (x, y)

def splitLineToInts(l):
    return list(map(lambda s: int(s), l.strip().split(" ")))

if __name__ == '__main__':
    parser = Parser('data/a_example.in')
    print(parser)
    all_fetched_pids = []
    for carId in range(0, 1):
        fetched_pids = []
        step = 0
        position = (0, 0)
        print("a")
        while step < parser.config['steps']:
            possible_pids = []

            for pids in parser.timeline_earliest_start[step:]:
                print(pids)
                for pid in pids:
                    if pid in fetched_pids:
                        continue
                    passenger = parser.passengers[pid]
                    distance_to_cur_pos = calcDistance(
                        position,
                        passenger['start_point'])

                    print(carId, position, pid, distance_to_cur_pos)
                    #all_fetched_pids.append(pid)
                    #fetched_pids.append(pid)
            step += 1

