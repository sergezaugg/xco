#--------------------------------
# Author : Serge Zaugg
# Description : Basic tests to check if process runs through
#--------------------------------

import os
import pandas as pd 
import shutil
try: # import from installed (built) package if possible
    import xeno_canto_organizer
    import xeno_canto_organizer.xco as xco
    pkg_import_source = xeno_canto_organizer.__file__
except: # for using test during local dev
    import src.xeno_canto_organizer
    import src.xeno_canto_organizer.xco as xco
    pkg_import_source = src.xeno_canto_organizer.__file__


#----------------------------------------------
# set up 
path_for_tests_only = './temp_xc_project'
try:
    shutil.rmtree(path_for_tests_only)
except:
    "ok"
if not os.path.isdir(path_for_tests_only):
    os.makedirs(path_for_tests_only)
shutil.copy('test_data/summary_of_data.pkl', 'temp_xc_project/summary_of_data.pkl')


#----------------------------------------------
# create objects to be tested
xc = xco.XCO(start_path = path_for_tests_only)
# xc.download_summary() not used in test 
xc.reload_local_summary()
xc.download_audio_files(verbose=True)
# from here we need ffmpeg installed
xc.mp3_to_wav(conversion_fs = 24000)
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, 
    log_f_min = 0.005,
    max_segm_per_file = 12, specsub = True, colormap='viridis',verbose=True)

#----------------------------------------------
# perform the tests

# not really a test, this will print the pkg_import_source with $ pytest -s
def test_import_location():    
    print('-->> pkg_import_source: ' , pkg_import_source)

# test xc.download_summary
def test_002():
    assert isinstance(xc.df_recs, pd.core.frame.DataFrame)
    assert xc.df_recs.shape[1] == 37 

# test xc.download_audio_files
def test_003():
    print(' -->>  getcwd: ', os.getcwd())
    print(' -->> listdir: ', os.listdir(os.getcwd()))
    assert len(os.listdir(os.path.join(path_for_tests_only, "downloaded_data_orig"))) == len(xc.df_recs)

# from here we need ffmpeg installed

# test xc.mp3_to_wav
def test_004():
    assert len(os.listdir(os.path.join(path_for_tests_only, "downloaded_data_wav_24000sps"))) == len(xc.df_recs)

# test xc.extract_spectrograms
def test_005():
    # the image dir has a dynamic naming with timestamp, so we need to get current name first 
    temp_image_path = [a for a in os.listdir(path_for_tests_only) if 'images_24000sps' in a ][0]
    assert len(os.listdir(os.path.join(path_for_tests_only, temp_image_path))) == 22





