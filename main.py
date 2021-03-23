#!./env/bin/python
import glob, os
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.DEBUG)

os.chdir("./data")
for file in glob.glob("*.csv"):

    logging.info("Beginning parsing of {file}".format(file=file))
    with open(file) as f:
        lines = f.readlines()
    logging.debug("File read succesfully")

    logging.debug("Trimming unnecessary data")
    new_lines = []
    for l in lines:
        nl = l.replace('"', '')
        if nl != '\n':
            nl = nl.strip()
            logging.debug("{l} -> {nl}".format(l=l, nl=nl))
            new_lines.append(nl)

    # Initialize data for loop
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
            # if 7.4<float(ll[0])<8.9:
            float(ll[0]) + float(ll[1]) + float(ll[2])
            time.append(float(ll[0]))
            force.append(float(ll[1]))
            strain.append(float(ll[2]))
            logging.debug(l)
            new_lines.append(l)
        except:
            pass

    logging.debug("Writing clean data to {file}".format(
        file="../cleaned/{}".format(file)))
    with open("../cleaned/{}".format(file), 'w+') as filw:
        filw.writelines('%s\n' % l for l in new_lines)
    logging.debug("Successfully written clean data")

    # if you want 3d plot
    # fig = plt.figure()
    # fig.suptitle(file)
    # ax=fig.add_subplot(111,projection='3d')
    # ax.scatter(time,force,strain,marker='o')
    # ax.set_xlabel('time (s)')
    # ax.set_ylabel('force (kg)')
    # ax.set_zlabel('strain')
    # plt.show()

    # Create figures
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle(file.replace('.csv', ''))
    plt.subplots_adjust(hspace=.3)
    plt.subplots_adjust(top=0.85)

    if 'T1D' in file:
        stress = [
            3 * (f * 9.81) * 0.16 / (2 * 0.015 * pow(0.003, 2) * pow(10, 6))
            for f in force
        ]
    elif 'T4D' in file:
        stress = [
            (0.25 * f * 9.81 * 0.16 * 0.00385) / (0.075 * pow(10, -8) * pow(10, 6))
            for f in force
        ]
    elif 'Al' in file:
        stress = [
            3 * (f * 9.81) * 0.14/(2*.009525*pow(0.009525,2)*pow(10,6))
            for f in force
        ]
    else:
        stress = [
            3 * (f * 9.81) * 0.16 / (2 * 0.015 * pow(0.01, 2) * pow(10, 6))
            for f in force
        ]
    ax1.scatter(time, force, label='Force over time')
    # ax1.scatter(time,strain,label='stress over time')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('stress (MPa)')

    # coef_undamaged, residuals_undamged, _, _, _ = np.polyfit(strain,
    #                                                          stress,
    #                                                          1,
    #                                                          full=True)
    # undamaged_fn = np.poly1d(coef_undamaged)
    # ax2.plot(strain,
    #          undamaged_fn(strain),
    #          '--b',
    #          label='Undamaged (E={:.0f}MPa, chi^2={:.3f})'.format(
    #              coef_undamaged[0],
    #              residuals_undamged[0] / len(strain)))
    # plt.legend()
    ax2.scatter(strain, stress, c='red', label='Force over strain')
    ax2.set_xlabel('strain')
    ax2.set_ylabel('stress (MPa)')

    # To show plot in window
    # plt.show()

    logging.debug("Saving graph to {file}".format(
        file='../graphs/{}.png'.format(file.replace('.csv', ''))))
    plt.savefig('../graphs/{}.png'.format(file.replace('.csv', '')))
    logging.info("Max Stress reached: {stress}".format(stress=max(stress)))
    logging.debug("Graph making successful")
