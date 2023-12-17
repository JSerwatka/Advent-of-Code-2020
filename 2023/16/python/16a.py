import numpy as np

beams = {}
energized_places = set()

class Beam:
    directions = {
        "top": (0, -1),
        "right": (1, 0),
        "bottom": (0, 1),
        "left": (-1, 0),
    }
    debug = False

    @classmethod
    def set_space_and_boundary(cls, space, boundary):
        cls.space = space
        cls.space_result = np.copy(space)
        cls.boundary = boundary
    
    def __init__(self, x, y, direction):
        # to prevent beams we already now route of
        self.beam_hash = f"{x}_{y}_{direction}"
        if self.beam_hash in beams:
            return

        self.x = x
        self.y = y
        self.direction = direction
        self.dead = False

        if self._is_in_boundaries():
            self._energize()
            beams[self.beam_hash] = self
            self._test_position()
        else:
            self.dead = True

    def __repr__(self):
        return self.beam_hash

    def _is_in_boundaries(self):
        return 0 <= self.x < Beam.boundary and 0 <= self.y < Beam.boundary

    def _energize(self):
        if (Beam.debug):
            Beam.space_result[self.y][self.x] = b"#"
        energized_places.add(self.x * 10 + self.y)

    def _test_position(self):
        match (self.direction, Beam.space[self.y][self.x]):
            case ("top", b"/"):
                self.direction = "right"
            case ("right", b"/"):
                self.direction = "top"
            case ("bottom", b"/"):
                self.direction = "left"
            case ("left", b"/"):
                self.direction = "bottom"
            case ("top", b"\\"):
                self.direction = "left"
            case ("right", b"\\"):
                self.direction = "bottom"
            case ("bottom", b"\\"):
                self.direction = "right"
            case ("left", b"\\"):
                self.direction = "top"
            case ("left", b"|") | ("right", b"|"):
                dx_top, dy_top = Beam.directions["top"]
                dx_bottom, dy_bottom = Beam.directions["bottom"]
                Beam(self.x + dx_top, self.y + dy_top, "top")
                Beam(self.x + dx_bottom, self.y + dy_bottom, "bottom")
                self.dead = True
            case ("top", b"-") | ("bottom", b"-"):
                dx_left, dy_left = Beam.directions["left"]
                dx_right, dy_right = Beam.directions["right"]
                Beam(self.x + dx_left, self.y + dy_left, "left")
                Beam(self.x + dx_right, self.y + dy_right, "right")
                self.dead = True

    def step(self):
        dx, dy = Beam.directions[self.direction]
        self.x += dx
        self.y += dy
        
        if self._is_in_boundaries():
            self._energize()
            self._test_position()
        else:
            self.dead = True

def main():
    # with open("../input.txt") as f:
    with open("../input_example.txt") as f:
        space = np.array([list(line.strip()) for line in f], dtype="S1")
        Beam.set_space_and_boundary(space, space.shape[0])
        Beam(0, 0, "right")
        while beams:
                _, beam = beams.popitem()
                while not beam.dead:
                    beam.step()
                    pass
        
        if Beam.debug:
            for line in Beam.space_result:
                print(line.tobytes().decode())


        return len(energized_places)

print(main())
