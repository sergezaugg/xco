# --------------
# Author : Serge Zaugg
# Description : Demo example of xco usage in practice
# For dev : import src.xeno_canto_organizer.xco as xco
# --------------

import xeno_canto_organizer.xco as xco

# Store API key in env variable of current session - needed for download_summary()
xco.api_key_to_env()

#---------------------------------
# (Example 1) custom search can be run sequentially - xc.recs_pool accumulates the meta-data 
# create instance of XCO - triggers creation of empty dir at 'start_path' - requests api key  
xc1 = xco.XCO(start_path = './temp_xc_project_01') 
xc1.download_summary(gen = "Corvus", sp = "corax", cnt = "switzerland", q = "A", len_max = 200, smp_min = 44100, verbose=True)
xc1.download_summary(gen = "Pyrrhocorax",          cnt = "France",      q = "B", len_max = 5,   smp_min = 44100, verbose=True)
xc1.download_summary(gen = "Coloeus",              cnt = "Belgium",     q = "C", len_max = 50 , smp_min = 44100, verbose=True)
# compile all accumulated meta-data to a dataframe (xc1.df_recs)
xc1.compile_df_and_save(verbose = True)
# or if session was closed 
xc1.reload_local_summary()
# get some summaries 
xc1.df_recs.shape
print(xc1.df_recs['full_spec_name'].value_counts())
print(xc1.df_recs['smp'].value_counts())
# Trigger download of mp3 files 
xc1.download_audio_files(verbose=True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc1.mp3_to_wav(conversion_fs = 44100)
# Extract spectrograms from segments and store as PNG
xc1.extract_spectrograms(
    fs_tag = 44100, # used to find the set of wav to be processed
    segm_duration = 2.0, # Segment duration in seconds 
    segm_step = 0.1, # relative step size between two consecutive segments (0.1 = 90% overlap, 1.0 = no overlap)
    win_siz = 512, # FFT window (nb of samples) used to compute spectrogram
    win_olap = 256, # FFT window overlap (nb of samples)
    max_segm_per_file = 10, # Limit the number of segments extracted per file
    specsub = True, # apply spectral subtraction
    log_f_min = 0.02, # log scaling of frequency from log_f_min (relative freq in [0.0. 1.1])
    colormap='viridis', # color map use to generate PGN image
    verbose=True # control verbosity of console feedback
    )

#---------------------------------
# (Example 2) search can be based on family and larger areas + sampling rate limits 
xc2 = xco.XCO(start_path = './temp_xc_project_02')
xc2.download_summary(fam = "Corvidae", area = "Europe", smp_min = 16000, smp_max = 16000,  len_min = 1, len_max = 10, verbose=True)
xc2.compile_df_and_save(verbose = True)
xc2.reload_local_summary()
xc2.download_audio_files(verbose=True)
xc2.mp3_to_wav(conversion_fs = 8000)
xc2.extract_spectrograms(fs_tag = 8000, segm_duration = 1.0, segm_step = 0.5, win_siz = 256, win_olap = 220.5, 
                        max_segm_per_file = 20, specsub = True, log_f_min = None, colormap='gray')

#---------------------------------
# (Example 3) sequential queries can be wrapped into a loop 
xc3 = xco.XCO(start_path = './temp_xc_project_03')
for g in ["Corvus", "Pyrrhocorax", "Coloeus", "Garrulus", "Pica"]:
    xc3.download_summary(gen = g, cnt = "France", q = "A", len_min = 6, len_max = 7)
xc3.compile_df_and_save(verbose = True)
xc3.download_audio_files(verbose=True)
xc3.mp3_to_wav(conversion_fs = 24000)
xc3.extract_spectrograms(fs_tag = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, 
                        max_segm_per_file = 20, log_f_min = 0.02, specsub = False, colormap='inferno')



