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

# helper code to generate project dirs
def make_temp_dir(tag):
    if not os.path.isdir('./temp_xc_project_' + tag):
        os.makedirs('./temp_xc_project_' + tag)
make_temp_dir('01')
make_temp_dir('02')
make_temp_dir('03')


#---------------------------------
# (Example 1) custom search can be run sequentially - xc.recs_pool accumulates the meta-data 
# On first use of download_summary xc api key must be provided
xc = xco.XCO(start_path = './temp_xc_project_01')
xc.download_summary(gen = "Corvus", sp = "corax", cnt = "switzerland", q = "A", len_max = 200, verbose=True)
xc.download_summary(gen = "Pyrrhocorax", cnt = "France", q = "B", len_min = 10, verbose=True)
xc.download_summary(gen = "Coloeus", cnt = "Belgium", q = "C", len_max = 100 , verbose=True)
print(len(xc.recs_pool))
xc.compile_df_and_save(verbose = True)
# get some summaries 
print(xc.df_recs['full_spec_name'].value_counts())
print(xc.df_recs['gen'].value_counts())
print(xc.df_recs['cnt'].value_counts())
# if session was closed
xc.reload_local_summary()
# Download the mp3 files 
xc.download_audio_files(verbose=True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 2.0, segm_step = 0.5, win_siz = 512, win_olap = 256, 
    max_segm_per_file = 10, specsub = True, log_f_min = 0.02, colormap='viridis',verbose=True)


#---------------------------------
# (Example 2) search can be based on family and larger areas + sampling rate limits 
xc = xco.XCO(start_path = './temp_xc_project_02')
xc.download_summary(fam = "Corvidae", area = "Europe", smp_min = 23000, smp_max = 24001,  len_max = 10, verbose=True)
xc.compile_df_and_save(verbose = True)
xc.download_audio_files(verbose=True)
xc.mp3_to_wav(conversion_fs = 20000)
xc.extract_spectrograms(fs_tag = 20000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, win_olap = 220.5, 
                        max_segm_per_file = 20, specsub = True, log_f_min = None, colormap='gray')

#---------------------------------
# (Example 3) sequential queries can be wrapped into a loop 
xc = xco.XCO(start_path = './temp_xc_project_03')
for g in ["Corvus", "Pyrrhocorax", "Coloeus", "Garrulus", "Pica"]:
    xc.download_summary(gen = g, cnt = "France", q = "A", len_min = 5, len_max = 8)
xc.compile_df_and_save(verbose = True)
xc.download_audio_files(verbose=True)
xc.mp3_to_wav(conversion_fs = 16000)
xc.extract_spectrograms(fs_tag = 16000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, 
                        max_segm_per_file = 20, log_f_min = 0.005, specsub = False, colormap='viridis')
