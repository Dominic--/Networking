Step 1:
	# generate connected topology from data
	
	## map nodes to 0 to N-1 numbers, and generate origin topology
    ### abilene_generate_topology.py
    ### isp_generate_topology.py
    ### geant_generate_topology.py

	## filter connected topology from origin topology
    ### filter_connected_topology.py

	cd script
	sh generate_connected_topology.sh

Step 2:
	# remove some link from the connected topology using eigenvalues
	//TODO : is there need to check if the topology connected still?

	cd bin
	sh off.sh

    

