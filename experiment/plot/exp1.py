import matplotlib.pyplot as plt

result_file_template = "result-compare-abilene"

f = open(result_file_template)
line = f.readline();
base = []
new = []
x = []
while line:
    tokens = line.strip().split()
    base.append(float(tokens[1]))
    new.append(float(tokens[2]))
    x.append(float(tokens[0]))

    line = f.readline()

f.close()

plt.plot(x, base, 'r--')
plt.plot(x, new, 'b--')
#plt.axis([0, 6, 0, 20])
plt.show()


