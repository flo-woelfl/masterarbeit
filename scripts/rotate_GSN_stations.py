
''' Rotates the BH1 and BH2 miniseeds to BHE and BHZ'''
from obspy import read
from obspy.signal.rotate import rotate2ZNE

filename = input('Please enter the filename with all miniseeds: ')

# the files with BH1 will be read in and it will be assumed that the BH2 files
# are from the same event
# therefore just the BH1 will be read in and the 1 will be replaced by 2 and Z 

with open(filename) as f:
    data = f.read().splitlines()
    for line in data:
        # print line
        st1 = read(line)
        data1 = st1[0].data

        line2 = list(line)
        line2[-7] = '2'
        # print ''.join(line2)
        st2 = read(''.join(line2))
        data2 = st2[0].data 

        lineZ = list(line)
        lineZ[-7] = 'Z'
        # print ''.join(lineZ)
        stZ = read(''.join(lineZ))
        dataZ = stZ[0].data 

        # rotations
        [new1, new2, newZ] = rotate2ZNE(data1, 30, 40, data2, 30, 40, dataZ, 30, 40)

        st_new1 = read()
        st_new1.write(''.join(line), format="MSEED")
        st_new1[0].data = new1       
        st_new2 = read()
        st_new2.write(''.join(line2), format="MSEED")
        st_new1[0].data = new2
        st_newZ = read()
        st_newZ.write(''.join(lineZ), format="MSEED")
        st_new1[0].data = newZ