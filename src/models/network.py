from src.models import Device, SubNet, PLC, HMI, DataStore, PC, Switch, Router

class Network:
    def __init__(self, num_subnets: int, num_plcs: int):
        self.subnets = set()
        self.init_network(num_subnets, num_plcs)

    def init_network(self, num_subnets: int, num_plcs: int):

        # Create the main subnet
        main_subnet = SubNet(0)
        main_switch = Switch(0, group_id=0)
        main_pc = PC(0, group_id=0)
        main_ds = DataStore(0, group_id=0)
        main_subnet.add_device(main_switch)
        main_subnet.add_device(main_pc)
        main_subnet.add_device(main_ds)
        self.add_subnet(main_subnet)

        # Create main switch to switch connection
        subnet1 = SubNet(1)
        main_router = Router(1, group_id=1)
        subnet1.add_device(main_router)
        subnet1.add_device(main_router)
        self.add_subnet(subnet1)
        # Connect main subnet to subnet1
        main_subnet.connect_net(subnet1)
        subnet1.connect_net(main_subnet)

        # Create main router to plc connection
        for i in range(num_subnets):
            self.genrate_subnet(i + 1, main_router, subnet1, num_plcs)


    def genrate_subnet(self, id, main_router: Router, subnet_main: SubNet, num_plcs: int):
        # Subnet 1
        subnet1 = SubNet(3 * id + 2)
        self.add_subnet(subnet1)
        subnet1.add_device(main_router)
        router1 = Router(id, group_id=1)
        subnet1.add_device(router1)
        # Connect subnet to subnet1
        subnet1.connect_net(subnet_main)
        subnet_main.connect_net(subnet1)

        # Subnet 2
        subnet2 = SubNet(3 * id + 3)
        self.add_subnet(subnet2)
        subnet2.add_device(router1)
        router = Router(id, group_id=id+1)
        subnet1.add_device(router)
        # Connect subnet1 to subnet2
        subnet1.connect_net(subnet2)
        subnet2.connect_net(subnet1)

        # Subnet 3
        subnet3 = SubNet(3 * id + 4)
        self.add_subnet(subnet3)
        subnet3.add_device(router)
        hmi = HMI(id, group_id=id+1)
        subnet1.add_device(hmi)  
        ds = DataStore(id, group_id=id+1)
        subnet1.add_device(ds)    
        for i in range(num_plcs):
            # TODO: group_id needs to be set
            plc = PLC(id * num_plcs + i, group_id=id+1)
            subnet1.add_device(plc)
        # Connect subnet2 to subnet3
        subnet2.connect_net(subnet3)
        subnet3.connect_net(subnet2)

        return
    

    def add_subnet(self, subnet: SubNet):
        self.subnets.add(subnet)


