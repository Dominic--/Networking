import matplotlib.pyplot as plt

topology_x_range = {'abilene':5, 'geant':12, 'cernet2':4}
remove_links = {'abilene':4, 'geant':15, 'cernet2':3}
topology_line_type = {1.5:'o', 2.0:'s'}
color_type = {'base':'r--', 'new':'b-'}
remove_type = {'base':'AC', 'new':'ERLU'}
result_file_template = "result-compare-%s-%0.1f"
topology_file_template = "../topology/connected/%s-connected-topology"
remove_file_template = "../topology/remove/%s-remove-%d-links"
remove_base_file_template = "../topology/remove/%s-remove-%d-links-base"


power_models = {155.0:60, 1240.0:100, 2480.0:140, 9920:174}
power_model = [60, 100, 140, 174]


line_list = []
label_list = []
for t in ['geant']:
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
        
        power_saving_ratio.append(saving / total)
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
        
        power_base_saving_ratio.append(saving / total)
        removes_base[num] = [s,d]
        num = num + 1

        line = f.readline()
    f.close()
    print power_base_saving_ratio


    for w in [1.5, 2.0]:
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

        l1, = plt.plot(power_saving_ratio[:topology_x_range[t]], base[:topology_x_range[t]], color_type['base']+topology_line_type[w])
        l2, = plt.plot(power_base_saving_ratio[:topology_x_range[t]], new[:topology_x_range[t]], color_type['new']+topology_line_type[w])

        label_list.append(t + '-' + remove_type['base'] + '-%0.1f' % w)  
        label_list.append(t + '-' + remove_type['new'] + '-%0.1f' % w)
        
        line_list.append(l1)
        line_list.append(l2)

plt.xlabel('Power Saving')
plt.ylabel('Oblivious Performance Ratio')
plt.legend(line_list, label_list, loc=2)

#plt.show()
plt.savefig('exp3_w.png', bbox_inches='tight')


