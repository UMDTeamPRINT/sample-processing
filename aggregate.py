import glob, os
import matplotlib.pyplot as plt
os.chdir("./data")
fig, (ax2) = plt.subplots(1)
count = 0
cols = ['red','green','blue','black']
marker=['x','o','H','+']
for file in glob.glob("*.csv"):
    if 'repair' in file:
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
                if float(ll[2])<0.03:
                    time.append(float(ll[0]))
                    force.append(float(ll[1]))
                    strain.append(float(ll[2]))
                    new_lines.append(l)
            except:
                pass
        if 'damaged' in file and not 'undamaged' in file:
            stress = [3*(f*9.81)*0.16/(2*0.015*pow(0.003,2)*pow(10,6)) for f in force]
        else:
            stress = [3*(f*9.81)*0.16/(2*0.015*pow(0.01,2)*pow(10,6)) for f in force]
        ax2.scatter(strain, stress, label=file.replace('(',' ').replace(')','')[0:10].strip()+'%',c=cols[count],marker=marker[count])
        ax2.set_xlabel('strain')
        ax2.set_ylabel('stress (MPa)')
        count+=1
plt.legend()
plt.show()