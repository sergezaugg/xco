# --------------
# Author : Serge Zaugg
# Description : Demo example of xco usage in practice
# For dev : import src.xeno_canto_organizer.xco as xco
# --------------

# --------------------------
# detailed usage example
import xeno_canto_organizer.xco as xco

#---------------------------------
# (Example 1) custom search can be run sequentially - xc.recs_pool accumulates the meta-data 
# On first use of download_summary xc api key must be provided
# create instance if XCO and an empty dir at 'start_path'
xc = xco.XCO(start_path = './temp_xc_project_01')
xc.download_summary(gen = "Corvus", sp = "corax", cnt = "switzerland", q = "A", len_max = 200, smp_min = 44100, verbose=True)
xc.download_summary(gen = "Pyrrhocorax",          cnt = "France",      q = "B", len_max = 5,   smp_min = 44100, verbose=True)
xc.download_summary(gen = "Coloeus",              cnt = "Belgium",     q = "C", len_max = 50 , smp_min = 44100, verbose=True)
# compile all accumulated meta-data to a dataframe (xc.df_recs)
xc.compile_df_and_save(verbose = True)
# get some summaries 
xc.df_recs.shape
print(xc.df_recs['full_spec_name'].value_counts())
print(xc.df_recs['smp'].value_counts())
# if session was closed
xc.reload_local_summary()
# Download the mp3 files 
xc.download_audio_files(verbose=True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 44100)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(
    fs_tag = 44100, 
    segm_duration = 2.0, 
    segm_step = 0.1, 
    win_siz = 512, 
    win_olap = 256, 
    max_segm_per_file = 10, 
    specsub = True, 
    log_f_min = 0.02, 
    colormap='viridis',
    verbose=True
    )


#---------------------------------
# (Example 2) search can be based on family and larger areas + sampling rate limits 
xc = xco.XCO(start_path = './temp_xc_project_02')
xc.download_summary(fam = "Corvidae", area = "Europe", smp_min = 16000, smp_max = 16000,  len_min = 1, len_max = 10, verbose=True)
xc.compile_df_and_save(verbose = True)
xc.download_audio_files(verbose=True)
xc.mp3_to_wav(conversion_fs = 8000)
# log_f_min = None will return the default (linear) frequency scaling
xc.extract_spectrograms(fs_tag = 8000, segm_duration = 1.0, segm_step = 0.5, win_siz = 256, win_olap = 220.5, 
                        max_segm_per_file = 20, specsub = True, log_f_min = None, colormap='gray')

#---------------------------------
# (Example 3) sequential queries can be wrapped into a loop 
xc = xco.XCO(start_path = './temp_xc_project_03')
for g in ["Corvus", "Pyrrhocorax", "Coloeus", "Garrulus", "Pica"]:
    xc.download_summary(gen = g, cnt = "France", q = "A", len_min = 5, len_max = 8)
xc.compile_df_and_save(verbose = True)
xc.download_audio_files(verbose=True)
xc.mp3_to_wav(conversion_fs = 24000)
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, 
                        max_segm_per_file = 20, log_f_min = 0.02, specsub = False, colormap='inferno')



