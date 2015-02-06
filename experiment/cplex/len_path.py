from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib import rc

font = {'size':20}
rc('font', **font)

fig1, ax1 = plt.subplots()

topology_letter = {'abilene':'a', 'geant':'b', 'cernet2':'c'}
topology_x_range = {'abilene':5, 'geant':16, 'cernet2':4}
topology_line_type = {'1.5':'o', '2.5':'s', '3.5':'^'}
color_type = {'base':'r--', 'new':'b-'}
remove_type = {'base':'DMP', 'new':'REAR'}
result_file_template = "path_stretch_%s_%s.txt"

line_list_1 = []
line_list_2 = []
label_list_1 = []
label_list_2 = []
for t in ['geant']:
    for w in ['1.5', '2.5', '3.5']:
        f = open(result_file_template % (t, w))
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

        #l1, = plt.plot(x[:topology_x_range[t]], m_mine[:topology_x_range[t]], color_type['new']+topology_line_type[t])
        #l2, = plt.plot(x[:topology_x_range[t]], m_base[:topology_x_range[t]], color_type['base']+topology_line_type[t])
        l1, = plt.plot(x[:topology_x_range[t]], a_mine[:topology_x_range[t]], color_type['new']+topology_line_type[w], ms=10)
        l2, = plt.plot(x[:topology_x_range[t]], a_base[:topology_x_range[t]], color_type['base']+topology_line_type[w], ms=10)

        label_list_1.append(r'$%s\ \omega=%s$' % (remove_type['new'], w))
        label_list_2.append(r'$%s\ \omega=%s$' % (remove_type['base'], w))
        
        line_list_1.append(l1)
        line_list_2.append(l2)

    plt.legend(line_list_2+line_list_1, label_list_2+label_list_1, loc=1, fontsize=13)
    plt.xlabel('Removing Links\n(%s)' % topology_letter[t], fontsize=22)
    plt.ylabel('Path Stretching Ratio', fontsize=22)
    
    pp = PdfPages('exp4_path_%s.pdf' % t)
    pp.savefig(fig1, bbox_inches='tight')
    pp.close()

    plt.show()


