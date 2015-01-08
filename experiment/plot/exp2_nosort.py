import matplotlib.pyplot as plt

result_file_template = "middle-compare-abilene"
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
    n = int(tokens[1])
    base[r][n] = float(tokens[2])
    new[r][n] = float(tokens[3])

    line = f.readline()

f.close()

for i in range(remove):
    plt.plot(x, base[i], 'r--')

for i in range(remove):
    plt.plot(x, new[i], 'b--')

#plt.axis([0, 6, 0, 20])
plt.show()


