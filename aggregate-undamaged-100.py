#!./env/bin/python
import glob, os, re
import numpy as np
import matplotlib.pyplot as plt
os.chdir("./data")
fig, (ax2) = plt.subplots(1)
count = 0
max_stress={}
#cols = ['red','green','blue','black','purple','yellow']
#marker=['x','o','H','+']
all_stress = []
all_strain = []
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

    max_stress[file]=(max(stress))
    if 'U' in file and not 'U9' in file:
        # Build cumulative data to do regression on
        all_strain.extend(strain)
        all_stress.extend(stress)

        # Plot data
        ax2.scatter(strain, stress, label=re.sub('\(.*\).*$','',file).strip())#,c=cols[count])
        ax2.set_xlabel('strain')
        ax2.set_ylabel('stress (MPa)')
        count+=1
        plt.legend()
        plt.title('Undamaged Stress-Strain')
        #plt.legend()
        #plt.show()

coef = np.polyfit(all_strain,all_stress,1)
print(coef)
poly1d_fn = np.poly1d(coef) 

ax2.plot(all_strain, poly1d_fn(all_strain), '--k')

# Sort labels alphabetically
handles, labels = ax2.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
ax2.legend(handles, labels)

# Save to file
print(max_stress)
plt.savefig('../graphs/aggregate-undamaged-stress-strain.png')
