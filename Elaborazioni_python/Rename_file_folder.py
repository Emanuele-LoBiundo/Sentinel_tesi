# Pythono3 code to rename multiple
# files in a directory or folder

# importing os module
import os
import pandas as pd

folder = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\Merge_VV\\"

a = os.listdir(folder)
b = a[len(a)-3]
# Function to rename multiple files
def main():
    i = 0

    for filename in os.listdir(folder):
        z = pd.to_datetime(filename[2:11])
        stringa = str(z)
        month = stringa[5:7]
        if ".aux" in filename:
            dst = filename[0:2] + "2018" + str(month) + str(filename[2:4]) + filename[-8:-4]
            src = folder + filename
            dst = folder + dst
            os.rename(src, dst)
        else:
            dst = filename[0:2] + "2018" + str(month) + str(filename[2:4]) + filename[-4:]
            print(dst)
            src = folder + filename
            dst = folder + dst
            os.rename(src, dst)
    i += 1


# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()

#
# # rename() function will
# # rename all the files
if ".ovr" in filename:
    os.rename(src, dst)
if ".aux" in filename:
    os.rename(src, dst)
elif ".xml" in filename:
    os.rename(src, dst)
else:
    pass


# Function to rename multiple files
def main():
    i = 0

    for filename in os.listdir(folder):
        if "ovr" in filename:
            if len(filename) == 19:
                z = pd.to_datetime(filename[2:11])
                stringa = str(z)
                month = stringa[5:7]
                dst = filename[0:2] + "2018" + str(month) + str(filename[2:4]) + filename[-4:]
                print(dst)
                src = folder + filename
                dst = folder + dst
                if dst not in os.listdir(folder):
                    os.rename(src, dst)
                    i += 1
        else:
            i += 1
            pass

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()