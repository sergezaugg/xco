# --------------
# Author : Serge Zaugg
# Description : For devel only : assess code in interactive mode 
# --------------




import os
# import xeno_canto_organizer.xco as xco
import src.xeno_canto_organizer.xco as xco

# make a projects dir, if it does not already exist
if not os.path.isdir('./temp_xc_project'):
    os.makedirs('./temp_xc_project')
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = './temp_xc_project')

# success 
xc.download_summary(gen = "Corvus" , sp = "corone", cnt = "France", verbose=False)
xc.download_summary(gen = "Corvus" , sp = "corone", cnt = "Germany", verbose=True)
xc.download_summary(gen = "Corvus" , sp = "corone", cnt = "Germany",  q = ">C", len_min = None, len_max = None , verbose=True)
xc.download_summary(gen = "Corvus" , cnt = "Germany", q = "A", len_min = 10, len_max = 12 , verbose=True)
xc.download_summary(cnt = "Germany", q = "B", len_min = 10, len_max = 20 , verbose=True)
xc.download_summary(gen = "Corvus", sp = "corone", verbose=True)
# fail
xc.download_summary(verbose=True)
xc.download_summary(gen = "Corvus" , sp = "ddddddd", verbose=False)
xc.download_summary(gen = "afvafas" , verbose=False)
xc.download_summary(cnt = "afvafas" ,verbose=False)


xc.df_recs.shape
print(xc.df_recs['gen'].value_counts())
print(xc.df_recs['q'].value_counts())
print(xc.df_recs['lic'].value_counts())



xc.__apikey
print(xc._XCO__apikey)

# Download the files 
xc.download_audio_files(verbose=True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(
    fs_tag = 24000, 
    segm_duration = 1.0, 
    segm_step = 0.5, 
    win_siz = 512, 
    win_olap = 192, 
    max_segm_per_file = 12, 
    specsub = True, 
    log_f_min = 0.005,
    colormap='viridis',
    verbose=True
    )






#---------------------------
# v3

import requests
import getpass
import gc
import os

apikey = 'demo'
apikey = 'adfbadfbsrfdb'

apikey = getpass.getpass("Password: ")

XC_API_URL = 'https://xeno-canto.org/api/3/recordings'

full_query_string = XC_API_URL +  '?query=sp:"larus fuscus"' + '&key=' + apikey + '&page=4'
full_query_string = XC_API_URL +  '?query=gen:larus+sp:fuscus' + '&key=' + apikey + '&page=4'

full_query_string = XC_API_URL +  '?query=gen:larus' + '&key=' + apikey + '&page=4'
full_query_string = XC_API_URL +  '?query=' + 'gen:larus' + '+' + 'cnt:France' + '&key=' + apikey
 
full_query_string = XC_API_URL +  '?query=' + 'gen:larus' + '+' + 'cnt:Spain'  + '&key=' + apikey 
full_query_string = XC_API_URL +  '?query=' + 'gen:larus' + '&key=' + apikey 
full_query_string = XC_API_URL +  '?query=' + 'gen:larus' + '+' + 'q:">B"' +'&key=' + apikey 
full_query_string = XC_API_URL +  '?query=' + 'gen:larus' + '+' + 'q:"A"' +'&key=' + apikey 
full_query_string = XC_API_URL +  '&key=' + apikey 

# for tests 
full_query_string = "https://xeno-canto.org/api/3/recordings?query=gen:larus+sp:fuscus&per_page=50&page=1&key=demo"
full_query_string = "https://xeno-canto.org/api/3/recordings' + '?query=gen:larus+sp:fuscus&key=demo"

r = requests.get(full_query_string, allow_redirects=True)
r
j = r.json()
j['numRecordings']

recs = j['recordings']
len(recs)


#---------------------
# delete apikey
# del apikey, full_query_string
# gc.collect()
# per_page=50

j = r.json()
j['numRecordings']


j['numSpecies']
j['page']
j['numPages']
j['recordings']


full_download_string = recs[3]["file"]


rq = requests.get(full_download_string, allow_redirects=True)

source_path = "C:/Users/sezau/Downloads"
finam2 = "testfile"

open(os.path.join(source_path, finam2 + '.mp3') , 'wb').write(rq.content)

qst = '?query=sp:"larus fuscus" &key=' + apikey
qst = '?query=sp:"larus fuscus" &key=' + apikey
qst = '?query=grp:soundscape+q:A+len:">3600" &key=' + apikey
qst = '?query=cnt:malaysia+smp:">192000" + q:">C" &key=' + apikey
qst = '?query=cnt:malaysia+smp:">192000" + q:"A" &key=' + apikey
qst = '?query=cnt:malaysia+smp:">192000" + q:"B" &key=' + apikey
qst = '?query=cnt:malaysia+smp:">192000" + q:">C"  &key=' + apikey
qst = '?query=gen:larus+sp:fuscus' + '&page=4' + '&key=' + apikey 
qst = '?query=gen:larus+cnt:france&key=' + apikey
qst = '?query=' + 'gen:"Larus"' + 'sp:"fuscus"' + '+cnt:"france"' + 'q:">C"' + '&key=' + apikey
qst = '?query=' + 'gen:"Larus"' + 'sp:"fuscus"' + '+cnt:"france"' + 'q:">C"' + 'len:">10"' + 'len:"<3600"' + '&key=' + apikey
qst = '?query=' + 'gen:"Parus"' + 'sp:"major"' + '+cnt:"switzerland"' + 'q:">C"' + 'len:">14"' + 'len:"<100"' + '&key=' + apikey
qst = '?query=' + 'gen:"Parus"'                + '+cnt:"switzerland"' + 'q:">C"' + 'len:">14"' + 'len:"<100"' + '&key=' + apikey

