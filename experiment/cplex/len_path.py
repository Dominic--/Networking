from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()

topology_x_range = {'abilene':5, 'geant':16, 'cernet2':4}
topology_line_type = {'1.5':'o', '2.5':'s', '3.5':'^'}
color_type = {'base':'r--', 'new':'b-'}
remove_type = {'base':'TMP', 'new':'ERLU'}
result_file_template = "path_stretch_%s_%s.txt"

line_list = []
label_list = []
#for t in ['geant']:
#for t in ['abilene']:
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
        l1, = plt.plot(x[:topology_x_range[t]], a_mine[:topology_x_range[t]], color_type['new']+topology_line_type[w])
        l2, = plt.plot(x[:topology_x_range[t]], a_base[:topology_x_range[t]], color_type['base']+topology_line_type[w])

        label_list.append(w + '-' + remove_type['base'])
        label_list.append(w + '-' + remove_type['new'])
        
        line_list.append(l1)
        line_list.append(l2)

    plt.legend(line_list, label_list, loc=1)
    plt.xlabel('Removing Links', fontsize=22)
    plt.ylabel('Path Stretching Ratio', fontsize=22)
    
    pp = PdfPages('exp4_path_%s.pdf' % t)
    pp.savefig(fig1)
    pp.close()

    plt.show()


