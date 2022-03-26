import heapq

WALL = 1

class PriorityQueue:
    """
    This is a priority queue where we will store our matrix positions to be checked.
    """
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Path:
    def __init__(self, pos, removed_wall):
        self.pos = pos
        self.removed_wall = removed_wall

    def get_neighbours(self, map):
        x, y = self.pos
        neighbours = []

        # Verify move left
        if x - 1 >= 0:
            if map[x - 1][y] != WALL:
                neighbours.append(Path((x-1,y), self.removed_wall))
            elif not self.removed_wall:
                neighbours.append(Path((x-1,y), True))

        # Verify move right
        if x + 1 < len(map):
            if map[x + 1][y] != WALL:
                neighbours.append(Path((x+1,y), self.removed_wall))
            elif not self.removed_wall:
                neighbours.append(Path((x+1,y), True))

        # Verify move down
        if y - 1 >= 0:
            if map[x][y - 1] != WALL:
                neighbours.append(Path((x,y-1), self.removed_wall))
            elif not self.removed_wall:
                neighbours.append(Path((x,y-1), True))

        # Verify move up
        if y + 1 < len(map[0]):
            if map[x][y + 1] != WALL:
                neighbours.append(Path((x,y+1), self.removed_wall))
            elif not self.removed_wall:
                neighbours.append(Path((x,y+1), True))

        return neighbours

    def __str__(self):
        return str(self.pos) + str(self.removed_wall)

    def __lt__(self, _):
        # We give priority to paths without the wall removed
        return not self.removed_wall


def heuristic(current_pos, end_pos):
    """
    Calculate an heuristics based on the current positions and the end position
    """
    x_start, y_start = current_pos
    x_end, y_end = end_pos

    # The closer the distance, the smaller the heuristic value
    return (x_end - x_start) + (y_end - y_start)


def solution(map):
    """
    This is basically the implementation of an A* algorithm where we allow
    removing a wall once per each possible path.
    """
    end_pos = (len(map) - 1, len(map[0])- 1)
    map_heuristic = lambda current_pos: heuristic(
        current_pos, end_pos
    )
    queue = PriorityQueue()
    begin = Path((0,0), False)
    queue.put(begin, 0)

    # Stores the costs to get to each map position, while considering having
    # removed a wall or not
    cost = dict()
    cost[str(begin)] = 1

    while not queue.empty():

        current = queue.get()

        if current.pos == end_pos:
            break

        for path in current.get_neighbours(map):
            new_cost = cost[str(current)] + 1

            if str(path) not in cost or new_cost < cost[str(path)]:
                cost[str(path)] = new_cost
                queue.put(path, new_cost + map_heuristic(path.pos))

    # Get the minimum between getting there by destroying a wall or not
    return min(
        cost.get(str(Path(end_pos, True)), float("inf")),
        cost.get(str(Path(end_pos, False)), float("inf"))
    )

if __name__ == "__main__":
    assert solution([
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
            [1, 1, 1, 0]
        ]) == 7

    assert solution([
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0]
        ]) == 11

    print("All tests passed")
