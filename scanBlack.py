import subprocess
import os
import tkinter as tk
import tkinter.filedialog

root = tk.Tk()
root.withdraw()

def starttc(log_file):
    hh = ()
    mm = ()
    ss = ()
    ff = ()
    rate = ()
    for line in log_file:
        if line.startswith('      timecode'):
            colon = line.find(':')
            hh = line[colon+2:colon+4]
            mm = line[colon+5:colon+7]
            ss = line[colon+8:colon+10]
            ff = line[colon+11:colon+13]
        if line.startswith('    Stream #0:0'):
            fps = line.find('fps')
            rate = line[fps-6:fps-1]
    return hh, mm, ss, ff, rate

def getblackstarts(log_file):
    black_starts = []
    for line in log_file:
        if 'blackdetect' in line:
            b_s = line.find('black_start')
            b_e = line.find('black_end')
            blacktimestart = line[b_s+12:b_e-1]
            black_starts.append(blacktimestart)
    return black_starts

def tccalculations(black_start, hh, mm, ss, ff):
    bdr = float(black_start)*.999
    bdrhh = int(bdr / 3600)
    bdrmm = int(bdr / 60)
    bdrss = int(bdr - (bdrmm * 60))
    bdrff = int(((bdr - int(bdr)) * 24) + 1)
    newhh = hh + bdrhh
    newmm = mm + bdrmm
    newss = ss + bdrss
    newff = ff + bdrff
    return newhh, newmm, newss, newff

def timecode(h, m, s, f):
    if h < 10:
        h = '0'+str(h)
    if m < 10:
        m = '0'+str(m)
    if s < 10:
        s = '0'+str(s)
    if f < 10:
        f = '0'+str(f)
    return h, m, s, f

print("Choose the source directory for the MP4 files")
directory = tkinter.filedialog.askdirectory()
AllMOVTCs = 'n'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".mp4"):
            full_file = str(os.path.join(root, file))
            full_file = full_file.replace(" " , "\ ")
            path = os.path.dirname(full_file)
            logfile = os.path.join(path, str(full_file[:-4]+"_FFMPEGLOG.txt"))
            subprocess.call('ffmpeg -i '+full_file+' -vf blackdetect=d=2:pic_th=0.97:pix_th=0.1 -an -f null - 2>'+logfile, shell=True)
            subprocess.call('ffmpeg -i '+full_file+' -vf blackdetect=d=00.00:pix_th=0.01 -an -f null - 2>'+logfile, shell=True)
            logfile = logfile.replace("\ ", " ")
            with open(logfile, 'r') as log_file:
                (hh, mm, ss, ff, rate) = starttc(log_file)
            #     if hh == () and mm == () and ss == () and ff == ():
            #         if AllMOVTCs == 'n':
            #             print("No Timecode in metadata.\n")
            #            # userTC = input("Enter the start timecode of the mp4 file excluding colons (hh:mm:ss:ff) \n")
            #            # print("You entered "+userTC+" \n")
            #            # AllMOVTCs = input("Will this be the start TC for all MP4 files? [y/n]")
            #             print('User Entered Start TimeCode is '+MOVTC)
            #     else:
            #         MOVTC = str(hh)+':'+str(mm)+':'+str(ss)+':'+str(ff)
            #         print('Start TimeCode is ' + MOVTC)
            #     print('The frame rate is '+str(rate))
            #     log_file.seek(0)
            #     (black_starts) = getblackstarts(log_file)
            #     blacktc = []
            #     for i in range(len(black_starts)):
            #         hh = int(hh)
            #         mm = int(mm)
            #         ss = int(ss)
            #         ff = int(ff)
            #         (newhh, newmm, newss, newff) = tccalculations(black_starts[i], hh, mm, ss, ff)
            #         if newff >= 24:
            #             newss = newss+1
            #             newff = newff-24
            #         if newss >= 60:
            #             newmm = newmm+1
            #             newss = newss-60
            #         if newmm >= 120:
            #             newhh = newhh+1
            #             newmm = newmm-120
            #         elif newmm >= 60:
            #             newhh = newhh+1
            #             newmm = newmm-60
            #         (blackhh, blackmm, blackss, blackff) = timecode(newhh, newmm, newss, newff)
            #         blacktc.append(str(blackhh)+':'+str(blackmm)+':'+str(blackss)+':'+str(blackff))
            # f = open(logfile[:-15]+"_BLACKS.txt", 'w')
            # f.write("LIST OF BLACKS AND THEIR START TIME CODES\n\n")
            # f.write("MP4 File: "+file+"\n")
            # f.write("Start Timecode of MP4 File: "+MOVTC+"\n")
            # f.write("Frame Rate of the MP4 File: "+str(rate)+"fps\n\n")
            # f.write("BLACKS:\n")
            # for i in range(len(blacktc)):
            #     f.write("Black starts at TC "+blacktc[i]+"\n")
            # f.close()
