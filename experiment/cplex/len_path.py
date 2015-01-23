import matplotlib.pyplot as plt

topology_x_range = {'abilene':5, 'geant':12, 'cernet2':4}
topology_line_type = {'abilene':'o', 'geant':'s', 'cernet2':'^'}
color_type = {'base':'r--', 'new':'b-'}
remove_type = {'base':'AC', 'new':'ERLU'}
result_file_template = "path_stretch_%s.txt"

line_list = []
label_list = []
for t in ['abilene', 'geant', 'cernet2']:
    f = open(result_file_template % t)
    line = f.readline()

    m_mine = []
    a_mine = []
    m_base = []
    a_base = []
    x = []

    while line:
        tokens = line.strip().split(', ')
        m_mine.append(float(tokens[1]))
        a_mine.append(float(tokens[2]))
        m_base.append(float(tokens[3]))
        a_base.append(float(tokens[4]))

        x.append(float(tokens[0]))

        line = f.readline()

    f.close()

    l1, = plt.plot(x[:topology_x_range[t]], m_mine[:topology_x_range[t]], color_type['new']+topology_line_type[t])
    l2, = plt.plot(x[:topology_x_range[t]], m_base[:topology_x_range[t]], color_type['base']+topology_line_type[t])
    l1, = plt.plot(x[:topology_x_range[t]], a_mine[:topology_x_range[t]], color_type['new']+topology_line_type[t])
    l2, = plt.plot(x[:topology_x_range[t]], a_base[:topology_x_range[t]], color_type['base']+topology_line_type[t])

    label_list.append(t + '-' + remove_type['base'])
    label_list.append(t + '-' + remove_type['new'])
    
    line_list.append(l1)
    line_list.append(l2)

#plt.legend(line_list, label_list, loc=2)

plt.show()
#plt.savefig('exp1_link.png', bbox_inches='tight')


