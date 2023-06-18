import network_manager



if __name__ == "__main__":
    network_manager = network_manager.NetworkManager("ALICE")
    network_manager.listen('localhost', 5002)
    network_manager.receive()
