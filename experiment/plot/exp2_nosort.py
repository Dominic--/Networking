import matplotlib.pyplot as plt

result_file_template = "middle-compare-abilene-1.5"
count = 1000
remove = 5

f = open(result_file_template)
line = f.readline();

base = [([0] * count) for i in range(remove)]
new = [([0] * count) for i in range(remove)]
x = [i for i in range(count)]
while line:
    tokens = line.strip().split()
    r = int(tokens[0])
    if int(r) >= 5:
        break
    n = int(tokens[1])
    base[r][n] = float(tokens[2])
    new[r][n] = float(tokens[3])

    line = f.readline()

f.close()

line1 = None
for i in range(remove):
    line1, = plt.plot(x, base[i], 'r--')

line2 = None
for i in range(remove):
    line2, = plt.plot(x, new[i], 'b-')

#plt.axis([0, 6, 0, 20])
plt.xlabel('Random Traffic Matrix')
plt.ylabel('Oblivious Performance Ratio')
plt.title('OPR with Random TMs')
plt.legend([line1, line2], ['AC', 'ERLU'], loc=2)

#plt.show()
plt.savefig('exp2_nosort_abilene.png', bbox_inches='tight')


