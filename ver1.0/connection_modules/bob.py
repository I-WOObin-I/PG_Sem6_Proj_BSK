import network_manager

if __name__ == "__main__":
    network_manager = network_manager.NetworkManager("BOB  ")
    network_manager.connect('localhost', 5002)
    network_manager.send('t', "yoooo")
    network_manager.send('x')