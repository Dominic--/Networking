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
    n = int(tokens[1])
    base[r][n] = float(tokens[2])
    new[r][n] = float(tokens[3])

    line = f.readline()

f.close()

for i in range(remove):
    for j in range(count):
        for k in range(j, count):
            if (base[i][j] > base[i][k]):
                tmp = base[i][j]
                base[i][j] = base[i][k]
                base[i][k] = tmp
    plt.plot(base[i], x, 'r--')
#plt.plot(base[4], x, 'r--')

for i in range(remove):
    for j in range(count):
        for k in range(j, count):
            if (new[i][j] > new[i][k]):
                tmp = new[i][j]
                new[i][j] = new[i][k]
                new[i][k] = tmp
    plt.plot(new[i], x, 'b--')
#plt.axis([0, 6, 0, 20])
plt.show()


