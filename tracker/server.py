from bittorrent_tracker import Tracker

# Create a new tracker
tracker = Tracker()

# Start the tracker
tracker.start()

print('Tracker is running on {}:{}'.format(*tracker.server.server_address))