for topo in abilene geant 1221 1239 1755 3257 3967 6461; do
	for with_weigth in 0 1; do
		./off ${with_weigth} 0.8 \
			../topology/connected/${topo}-connected-topology \
			../topology/final/${topo}-final-${with_weigth}-topology \
			../topology/remove/${topo}-remove-${with_weigth}-links 
	done
done
