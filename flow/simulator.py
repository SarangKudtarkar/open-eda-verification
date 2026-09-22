class Simulator:
    def __init__(self, name: str):
        self.name = name

    def make_command(self):
        return ["make", f"SIM={self.name}"]


def get_simulator(name: str):
    supported = {"icarus", "verilator"}

    if name not in supported:
        raise ValueError(
            f"Unsupported simulator '{name}'. "
            f"Supported simulators: {sorted(supported)}"
        )

    return Simulator(name)
