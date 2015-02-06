from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
from matplotlib import rc

t = 'geant'


font = {'size':20}
rc('font', **font)
fig1, ax1 = plt.subplots()

topology_letter = {'abilene':'a', 'geant':'b', 'cernet2':'c'}
topology_x_range = {'abilene':5, 'geant':13, 'cernet2':4}
remove_links = {'abilene':4, 'geant':15, 'cernet2':3}
w_line_type = {'1.5':'o', '2.5':'s', '3.5':'^'}
color_type = {'base':'r--', 'new':'b-'}
remove_type = {'base':'DMP', 'new':'REAR'}
result_file_template = "result-compare-%s-%s"
topology_file_template = "../topology/connected/%s-connected-topology"
remove_file_template = "../topology/remove/%s-remove-%d-links"
remove_base_file_template = "../topology/remove/%s-remove-%d-links-power"

y_lim = {'abilene':9, 'geant':200, 'cernet2':4}


power_models = {155.0:60, 1240.0:100, 2480.0:140, 9920:174}
power_model = [60, 100, 140, 174]


line_list_1 = []
line_list_2 = []
label_list_1 = []
label_list_2 = []
#for t in ['abilene', 'geant', 'cernet2']:
for w in ['1.5', '2.5', '3.5']:
    # compute the total power of topology
    f = open(topology_file_template % t)
    line = f.readline()
    line = f.readline()
    topo = dict()
    total = 0
    while line:
        tokens = line.strip().split()
        s = int(tokens[0])
        d = int(tokens[1])
        c = float(tokens[2])
        
        topo[s,d] = c
        if c <= 155.0:
            total = total + power_model[0]
        elif c <= 1240.0:
            total = total + power_model[1]
        elif c <= 2480.0:
            total = total + power_model[2]
        elif c <= 9920.0:
            total = total + power_model[3]

        line = f.readline()
    f.close()
    #print total

    # compute the power removed link array
    removes = dict()
    power_saving_ratio = [0]
    saving = 0.0
    f = open(remove_file_template % (t, remove_links[t]))
    line = f.readline()
    num = 1
    while line:
        tokens = line.strip().split()
        s = int(tokens[0])
        d = int(tokens[1])

        if topo[s,d] <= 155.0:
            saving = saving + power_model[0]
        elif topo[s,d] <= 1240.0:
            saving = saving + power_model[1]
        elif topo[s,d] <= 2480.0:
            saving = saving + power_model[2]
        elif topo[s,d] <= 9920.0:
            saving = saving + power_model[3]
        
        power_saving_ratio.append(saving / total * 100)
        removes[num] = [s,d]
        num = num + 1

        line = f.readline()
    f.close()
    print power_saving_ratio


    removes_base = dict()
    f = open(remove_base_file_template % (t, remove_links[t]))
    line = f.readline()
    power_base_saving_ratio = [0]
    saving = 0.0
    num = 1
    while line:
        tokens = line.strip().split()
        s = int(tokens[0])
        d = int(tokens[1])

        if topo[s,d] <= 155.0:
            saving = saving + power_model[0]
        elif topo[s,d] <= 1240.0:
            saving = saving + power_model[1]
        elif topo[s,d] <= 2480.0:
            saving = saving + power_model[2]
        elif topo[s,d] <= 9920.0:
            saving = saving + power_model[3]
        
        power_base_saving_ratio.append(saving / total * 100)
        removes_base[num] = [s,d]
        num = num + 1

        line = f.readline()
    f.close()
    print power_base_saving_ratio


    f = open(result_file_template % (t, w))
    line = f.readline()

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

    l1, = ax1.plot(power_base_saving_ratio[:topology_x_range[t]], base[:topology_x_range[t]], color_type['base']+w_line_type[w], ms=10)
    l2, = ax1.plot(power_saving_ratio[:topology_x_range[t]], new[:topology_x_range[t]], color_type['new']+w_line_type[w], ms=10)

    label_list_1.append(r'$%s\ \omega=%s$' % (remove_type['base'], w))
    label_list_2.append(r'$%s\ \omega=%s$' % (remove_type['new'], w))
    
    line_list_1.append(l1)
    line_list_2.append(l2)

plt.xlabel('Power Saving Ratio (%) \n '+'(%s)' % topology_letter[t], fontsize=22)
plt.ylabel('OPRE', fontsize=22)
#plt.legend([l1, l2], ['TMP, w=1.5, 2.0, 2.5...', 'ERLU, w=1.5, 2.0, 2.5...'], loc=2)
plt.legend(line_list_1+line_list_2, label_list_1+label_list_2, loc=2, fontsize=15)

ax1.set_yscale('log')
ax1.set_ylim([1,y_lim[t]])
ax1.get_yaxis().set_major_formatter(tic.ScalarFormatter())
#ax1.yaxis.set_minor_formatter(FormatStrFormatter("%0.1f"))


pp = PdfPages('opr_with_power_%s.pdf' % t)
pp.savefig(fig1, bbox_inches='tight')
pp.close()

plt.show()
#plt.savefig('opr_with_power_%s.png' % t, bbox_inches='tight')


