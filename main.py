from src.models import Network

def main():
    network = Network(3, 3)
    for subnet in network.subnets:
        print(subnet)


if __name__ == "__main__":
    main()
