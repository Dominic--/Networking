#for topo in abilene geant 1221 1239 1755 3257 3967 6461; do
for topo in cernet2; do
	#for with_weigth in 0 1; do
	for remove_n in {1..3}; do
		../bin/off_by_connectivity 0 ${remove_n}\
			../topology/connected/${topo}-connected-topology \
			../topology/final/${topo}-final-topology-${remove_n}-base \
			../topology/remove/${topo}-remove-${remove_n}-links-base 
	done
done

for topo in geant; do
	#for with_weigth in 0 1; do
	for remove_n in {1..15}; do
		../bin/off_by_connectivity 0 ${remove_n}\
			../topology/connected/${topo}-connected-topology \
			../topology/final/${topo}-final-topology-${remove_n}-base \
			../topology/remove/${topo}-remove-${remove_n}-links-base 
	done
done
