from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rc
import matplotlib.pyplot as plt

t = 'cernet2'

font = {'size':20}
rc('font', **font)

fig1, ax1 = plt.subplots()

result_file_template = "middle-compare-%s-%s"
count = 1001

topology_letter = {'abilene':'a', 'geant':'b', 'cernet2':'c'}
remove_ = {'abilene':4, 'geant':6, 'cernet2':2}
remove = remove_[t]


label = {'1.5':'o', '2.5':'s', '3.5':'^'}
base = {'1.5':[0] * count, '2.5':[0] * count, '3.5':[0] * count}
new = {'1.5':[0] * count, '2.5':[0] * count, '3.5':[0] * count}
x = [i/10 for i in range(count)]
xx = [0, 5, 10, 15] + [i*20 for i in range(1,5)]+[80, 85, 90, 95, 98, 99, 100]
print xx

for w in ['1.5', '2.5', '3.5']:
    f = open(result_file_template % (t, w))
    line = f.readline();
    while line:
        tokens = line.strip().split()
        r = int(tokens[0])
        n = int(tokens[1])
        if int(r) != remove:
            line = f.readline()
            continue
        base[w][n] = float(tokens[2])
        new[w][n] = float(tokens[3])

        line = f.readline()

    f.close()

line_list = []
line_label = []
line1 = None
for i in ['1.5', '2.5', '3.5']:
    base[i][1000] = 1000
    for j in range(count):
        for k in range(j, count):
            if (base[i][j] > base[i][k]):
                tmp = base[i][j]
                base[i][j] = base[i][k]
                base[i][k] = tmp
    base[i][1000] = base[i][999]
    l1, = plt.plot([base[i][ii*10] for ii in xx], xx, 'r--'+label[i], ms=10)

    line_list.append(l1)
    line_label.append(r'$DMP\ \omega=%s$' % i)

line2 = None
for i in ['1.5', '2.5', '3.5']:
    new[i][1000] = 1000
    for j in range(count):
        for k in range(j, count):
            if (new[i][j] > new[i][k]):
                tmp = new[i][j]
                new[i][j] = new[i][k]
                new[i][k] = tmp
    new[i][1000] = new[i][999]
    l1, = plt.plot([new[i][ii*10] for ii in xx], xx, 'b-'+label[i], ms=10)

    line_list.append(l1)
    line_label.append(r'$REAR\ \omega=%s$' % i)

#plt.axis([0, 6, 0, 20])

print (base['3.5'][500] - base['2.5'][500]) / (new['3.5'][1000] - new['2.5'][0])

plt.ylabel('CDF (%)', fontsize=22)
plt.xlabel("Performance Ratio\n(%s)" % topology_letter[t], fontsize=22)
plt.legend(line_list, line_label, loc=4, fontsize=15)

pp = PdfPages('exp2_sort_%s.pdf' % t)
pp.savefig(fig1, bbox_inches='tight')
pp.close()

plt.show()
#plt.savefig('exp2_sort_cernet2.png', bbox_inches='tight')

