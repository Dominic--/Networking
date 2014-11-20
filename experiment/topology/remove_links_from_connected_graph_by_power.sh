#for topo in abilene geant 1221 1239 1755 3257 3967 6461; do
for topo in abilene geant; do
	for threhold in 80 85 90 95; do
		../bin/off_by_power 1 ${threhold} \
			../topology/connected/${topo}-connected-topology \
			../topology/final/${topo}-final-1-${threhold}-topology-power \
			../topology/remove/${topo}-remove-1-${threhold}-links-power 
	done
done
