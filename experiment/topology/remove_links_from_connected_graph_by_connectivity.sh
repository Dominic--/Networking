#for topo in abilene geant 1221 1239 1755 3257 3967 6461; do
for topo in abilene geant; do
	for with_weigth in 0 1; do
		../bin/off ${with_weigth} 0.95 \
			../topology/connected/${topo}-connected-topology \
			../topology/final/${topo}-final-${with_weigth}-95-topology \
			../topology/remove/${topo}-remove-${with_weigth}-95-links 
	done
done
