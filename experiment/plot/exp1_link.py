import matplotlib.pyplot as plt

topology_x_range = {'abilene':5, 'geant':12, 'cernet2':4}
topology_line_type = {'abilene':'o', 'geant':'s', 'cernet2':'^'}
color_type = {'base':'r--', 'new':'b-'}
remove_type = {'base':'AC', 'new':'ERLU'}
result_file_template = "result-compare-%s-1.5"

line_list = []
label_list = []
for t in ['abilene', 'geant', 'cernet2']:
    f = open(result_file_template % t)
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

    l1, = plt.plot(x[:topology_x_range[t]], base[:topology_x_range[t]], color_type['base']+topology_line_type[t])
    l2, = plt.plot(x[:topology_x_range[t]], new[:topology_x_range[t]], color_type['new']+topology_line_type[t])

    label_list.append(t + '-' + remove_type['base'])
    label_list.append(t + '-' + remove_type['new'])
    
    line_list.append(l1)
    line_list.append(l2)

plt.xlabel('Remove Links')
plt.ylabel('oblivious performance ratio')
plt.title('OPR with Power Saving')
plt.legend(line_list, label_list, loc=2)

plt.show()
#plt.savefig('exp1.png', bbox_inches='tight')


