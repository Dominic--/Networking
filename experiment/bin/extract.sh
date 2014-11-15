for file in X{01..24}; do
	#mkdir ../demand/abilene/X${file}
	for line in {1..2016}; do
		sed "${line}q;d" ../data/abilene/${file} > ../demand/abilene/X${file}/${line}.txt
	done
done
