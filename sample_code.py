# --------------
# Author : Serge Zaugg
# Description : Demo example of xco usage in practice
# For dev : import src.xeno_canto_organizer.xco as xco
# --------------

# --------------------------
# detailed usage example
import os
import xeno_canto_organizer.xco as xco
# import src.xeno_canto_organizer.xco as xco

# make a projects dir, if it does not already exist
if not os.path.isdir('./temp_xc_project'):
    os.makedirs('./temp_xc_project')

# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = './temp_xc_project')

# custom queries can be run sequentially - xc.recs_pool accumulates the meta-data 
# On first use of download_summary xc api key must be provided
xc.download_summary(gen = "Corvus", cnt = "switzerland", q = "A", len_max = 14, verbose=True)
print(len(xc.recs_pool))
xc.download_summary(gen = "Pyrrhocorax", cnt = "switzerland", q = "B", len_min = 10, verbose=True)
print(len(xc.recs_pool))
xc.download_summary(gen = "Coloeus", cnt = "switzerland", q = "C",len_max = 100 , verbose=True)
print(len(xc.recs_pool))

# sequential queries can be wrappd into a loop 
for g in ["Corvus", "Pyrrhocorax", "Coloeus", "Garrulus", "Pica"]:
    xc.download_summary(gen = g, cnt = "France", q = "A", len_min = 5, len_max = 10)
    print("Cumulative N files: ", len(xc.recs_pool))

# compile all content gathered above into a single df
xc.compile_df_and_save(verbose = True)
# check 
xc.df_recs.shape
print(xc.df_recs['gen'].value_counts())
print(xc.df_recs['q'].value_counts())
print(xc.df_recs['lic'].value_counts())
print(xc.df_recs['full_spec_name'].value_counts())
# if session was closed
xc.reload_local_summary()
# Download the files 
xc.download_audio_files(verbose=True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(
    fs_tag = 24000, 
    segm_duration = 2.0, 
    segm_step = 0.5, 
    win_siz = 512, 
    win_olap = 192, 
    max_segm_per_file = 10, 
    specsub = True, 
    log_f_min = 0.005,
    colormap='viridis',
    verbose=True
    )


# xx = xc.tempX
# xx.shape
# yy = log_scale_spectrogram(S = xx, fmin=0.0001, bins=512)
# yy.shape





#---------------------------------------
# Open a new session
import xeno_canto_organizer.xco as xco
# The pre-downloaded mp3 files can be reprocessed with different parameters 
# Point XCO to the dir with pre-downloaded mp33
xc = xco.XCO(start_path = './temp_xc_project')
# Make wavs with fs = 20000 and then short spectrogram 
xc.mp3_to_wav(conversion_fs = 20000)
xc.extract_spectrograms(fs_tag = 20000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, win_olap = 220.5, max_segm_per_file = 20, 
                        log_f_min = None,
                        specsub = True, colormap='gray')

# Make  Make wavs with fs = 16000 and then long spectrogram 
xc.mp3_to_wav(conversion_fs = 16000)
xc.extract_spectrograms(fs_tag = 16000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, max_segm_per_file = 20, 
                        log_f_min = 0.005,
                        specsub = False, colormap='viridis')
