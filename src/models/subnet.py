
class SubNet:

    def __init__(self, id):
        self.id = id
        self.devices = set()
        self.connected_nets = set()

    def add_device(self, device):
        self.devices.add(device)

    def connect_net(self, net):
        self.connected_nets.add(net)

    def __str__(self):
        dev_str = [f"{dev}" for dev in self.devices]
        return f"SubNet {self.id}, devices connected: {dev_str}"