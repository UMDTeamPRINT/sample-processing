#!./env/bin/python
import glob, os, re
import numpy as np
import matplotlib.pyplot as plt
os.chdir("./data")
fig, (ax2) = plt.subplots(1)
count = 0
max_stress = {}
#cols = ['red','green','blue','black','purple','yellow']
#marker=['x','o','H','+']
all_repaired_stress = []
all_repaired_strain = []
all_undamaged_strain = []
all_undamaged_stress = []
for file in glob.glob("*.csv"):
    with open(file) as f:
        lines = f.readlines()
    new_lines = []
    for l in lines:
        nl = l.replace('"', '')
        if nl != '\n':
            nl = nl.strip()
            new_lines.append(nl)
    new_lines.pop(1)
    header = new_lines.pop(0)
    lines = new_lines
    time = []
    force = []
    strain = []
    new_lines = [header]
    for l in lines:
        l = l.replace('-', '')
        ll = l.split(',')
        try:
            float(ll[0]) + float(ll[1]) + float(ll[2])
            if float(ll[2]) < 0.027:
                time.append(float(ll[0]))
                force.append(float(ll[1]))
                strain.append(float(ll[2]))
                new_lines.append(l)
        except:
            pass
    if 'damaged' in file and not 'undamaged' in file:
        stress = [
            3 * (f * 9.81) * 0.16 / (2 * 0.015 * pow(0.003, 2) * pow(10, 6))
            for f in force
        ]
    else:
        stress = [
            3 * (f * 9.81) * 0.16 / (2 * 0.015 * pow(0.01, 2) * pow(10, 6))
            for f in force
        ]

    max_stress[file] = (max(stress))
    if 'R' in file and not 'R6' in file and not 'R4' in file:
        # Build cumulative data to do regression on
        all_repaired_strain.extend(strain)
        all_repaired_stress.extend(stress)

        # Plot data
        ax2.scatter(
            strain, stress, c='red'
        )  #label=re.sub('\(.*\).*$','',file).strip())#,c=cols[count])
        ax2.set_xlabel('strain')
        ax2.set_ylabel('stress (MPa)')
        count += 1
    if 'U' in file and not 'U9' in file:
        # Build cumulative data to do regression on
        all_undamaged_strain.extend(strain)
        all_undamaged_stress.extend(stress)

        # Plot data
        ax2.scatter(
            strain, stress, c='blue'
        )  #label=re.sub('\(.*\).*$','',file).strip())#,c=cols[count])
        ax2.set_xlabel('strain')
        ax2.set_ylabel('stress (MPa)')
        count += 1

coef_undamaged, residuals_undamged, _, _, _ = np.polyfit(all_undamaged_strain,
                                                         all_undamaged_stress,
                                                         1,
                                                         full=True)
undamaged_fn = np.poly1d(coef_undamaged)
ax2.plot(all_undamaged_strain,
         undamaged_fn(all_undamaged_strain),
         '--b',
         label='Undamaged (E={:.0f}MPa, chi^2={:.3f})'.format(
             coef_undamaged[0],
             residuals_undamged[0] / len(all_undamaged_strain)))

coef_repaired, residuals_repaired, _, _, _ = np.polyfit(all_repaired_strain,
                                                        all_repaired_stress,
                                                        1,
                                                        full=True)
repaired_fn = np.poly1d(coef_repaired)
ax2.plot(all_repaired_strain,
         repaired_fn(all_repaired_strain),
         '--r',
         label='Repaired (E={:.0f}MPa, chi^2={:.3f})'.format(
             coef_repaired[0],
             residuals_repaired[0] / len(all_repaired_strain)))

# Sort labels alphabetically
handles, labels = ax2.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
ax2.legend(handles, labels)

# Save to file
plt.legend()
plt.title('Aggregate')
plt.savefig('../graphs/aggregate-comparison-stress-strain.png')
print(residuals_undamged)
print(len(all_undamaged_strain))
print(residuals_repaired)
