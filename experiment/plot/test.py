import matplotlib.pyplot as plt

result_file_template = "result-compare-geant"

f = open(result_file_template)
line = f.readline();
base = []
new = []
x_base = []
x_new = []
num = 0
while line:
    tokens = line.strip().split()
    base.append(float(tokens[6]))
    x_base.append(num)

    if num < 13:
        new.append(float(tokens[9]))
        x_new.append(num)

    num = num + 1
    line = f.readline()

f.close()

plt.plot(x_base, base, 'r--')
plt.plot(x_new, new, 'b--')
#plt.axis([0, 6, 0, 20])
plt.show()


