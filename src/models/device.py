from src.models.subnet import SubNet

class Device:
    def __init__(self, id, type, status, group_id):
        self.id = id
        self.type = type
        self.status = status
        self.group_id = group_id
        self.subnet = None

    def connect_to_network(self, subnet: SubNet):
        subnet.add_device(self)
        self.subnet = subnet

    def __str__(self):
        return f"{self.type} {self.id}, status: {self.status}, group_id: {self.group_id}"


class PLC(Device):
    def __init__(self, id, status = '', group_id = 0):
        super().__init__(id, "PLC", status, group_id)


class HMI(Device):
        def __init__(self, id, status = '', group_id = 0):
            super().__init__(id, "HMI", status, group_id)


class DataStore(Device):
    def __init__(self, id, status = '', group_id = 0):
        super().__init__(id, "DataStore", status, group_id)


class PC(Device):
    def __init__(self, id, status = '', group_id = 0):
        super().__init__(id, "PC", status, group_id)

    
class Router(Device):
    def __init__(self, id, status = '', group_id = 0):
        super().__init__(id, "Router", status, group_id)


class Switch(Device):
    def __init__(self, id, status = '', group_id = 0):
        super().__init__(id, "Switch", status, group_id)