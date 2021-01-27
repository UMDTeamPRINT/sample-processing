import glob, os
import matplotlib.pyplot as plt
os.chdir("./data")
for file in glob.glob("*.csv"):
    with open(file) as f:
        lines = f.readlines()
    new_lines = []
    for l in lines:
        nl = l.replace('"','')
        if nl!='\n':
            nl=nl.strip()
            new_lines.append(nl)
    new_lines.pop(1)
    header=new_lines.pop(0)
    lines = new_lines
    time =[]
    force=[]
    strain=[]
    new_lines = [header]
    for l in lines:
        l = l.replace('-','')
        ll = l.split(',')
        try:
            float(ll[0])+float(ll[1])+float(ll[2])
            time.append(float(ll[0]))
            force.append(float(ll[1]))
            strain.append(float(ll[2]))
            new_lines.append(l)
        except:
            pass
    with open('cleaned/{}'.format(file), 'w+') as filw:
        filw.writelines('%s\n' % l for l in new_lines)
    # if you want 3d plot
    # fig = plt.figure()
    # fig.suptitle(file)
    # ax=fig.add_subplot(111,projection='3d')
    # ax.scatter(time,force,strain,marker='o')
    # ax.set_xlabel('time (s)')
    # ax.set_ylabel('force (kg)')
    # ax.set_zlabel('strain')
    # plt.show()
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle(file.replace('.csv',''))
    plt.subplots_adjust(hspace=.3)
    plt.subplots_adjust(top=0.85)
    if 'damaged' in file and not 'undamaged' in file:
        stress = [3*(f*9.81)*0.16/(2*0.015*pow(0.003,2)*pow(10,6)) for f in force]
    else:
        stress = [3*(f*9.81)*0.16/(2*0.015*pow(0.01,2)*pow(10,6)) for f in force]
    ax1.scatter(time, stress, label='Force over time')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('stress (MPa)')
    ax2.scatter(strain, stress, c='red', label='Force over strain')
    ax2.set_xlabel('strain')
    ax2.set_ylabel('stress (MPa)')
    # plt.show()
    plt.savefig('graphs/{}.png'.format(file.replace('.csv','')))
    print(file)
    print(max(stress))
