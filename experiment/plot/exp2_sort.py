from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()

t = 'abilene'
result_file_template = "middle-compare-%s-1.5" % t
count = 1000
remove = 4

f = open(result_file_template)
line = f.readline();

base = [([0] * count) for i in range(remove)]
new = [([0] * count) for i in range(remove)]
x = [i for i in range(count)]
while line:
    tokens = line.strip().split()
    r = int(tokens[0])
    n = int(tokens[1])
    if int(r) == remove:
        break
    base[r][n] = float(tokens[2])
    new[r][n] = float(tokens[3])

    line = f.readline()

f.close()

line1 = None
for i in range(0, remove):
    for j in range(count):
        for k in range(j, count):
            if (base[i][j] > base[i][k]):
                tmp = base[i][j]
                base[i][j] = base[i][k]
                base[i][k] = tmp
    line1, = plt.plot(x, base[i], 'r--')

line2 = None
for i in range(0, remove):
    for j in range(count):
        for k in range(j, count):
            if (new[i][j] > new[i][k]):
                tmp = new[i][j]
                new[i][j] = new[i][k]
                new[i][k] = tmp
    line2, = plt.plot(x, new[i], 'b-')

#plt.axis([0, 6, 0, 20])

plt.xlabel('Random Traffic Matrix')
plt.ylabel('Oblivious Performance Ratio')
plt.legend([line1, line2], ['TMP', 'ERLU'], loc=2)

pp = PdfPages('exp2_sort_%s.pdf' % t)
pp.savefig(fig1)
pp.close()

plt.show()
#plt.savefig('exp2_sort_cernet2.png', bbox_inches='tight')

