# Definition
PRE_FOLDER_PATH := ..
DEST_PEERS := peer_0 peer_1 peer_2 peer_3 peer_4 peer_5
POST_FOLDER_PATH := metainfo_folder

# Target
.PHONY: simulation_manager

# Target to broadcast all torrent files from a peer to the others 
broadcast:
	@echo "Broadcasting all torrent files from $(peer_src)"
	@for peer in $(DEST_PEERS); do \
		if [ "$$peer" != "$(peer_src)" ]; then \
            		cp $(PRE_FOLDER_PATH)/$(peer_src)/$(POST_FOLDER_PATH)/* $(PRE_FOLDER_PATH)/$$peer/; \
        	fi \
    	done
