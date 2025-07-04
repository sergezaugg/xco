#--------------------------------
# Author : Serge Zaugg
# Description : Basic tests to check if process runs through
#--------------------------------

import pytest
import numpy as np

try: # import from installed (built) package if possible
    import xeno_canto_organizer
    import xeno_canto_organizer.xco as xco
    pkg_import_source = xeno_canto_organizer.__file__
except: # for using test during local dev
    import src.xeno_canto_organizer
    import src.xeno_canto_organizer.xco as xco
    pkg_import_source = src.xeno_canto_organizer.__file__

#----------------------------------------------
# create objects to be tested
xc = xco.XCO(start_path = "aaa") 

# dev - get fs of the files 
# import wave
# wave_file = wave.open("./tests/test_data/test_wave1.wav", 'r')
# fs = wave_file.getframerate()
# wave_file.close()

#----------------------------------------------
# perform unit tests

def test_clean_xc_filenames():
    str_dirty = "+++///Le_p%%eti(t_chi)èn_Milöu-vöüs_di(=)t_pi**pi_çac`^a.mp3"
    str_cleaned_long  = xc._clean_xc_filenames(s = str_dirty, max_string_size = 999)
    str_cleaned_short = xc._clean_xc_filenames(s = str_dirty, max_string_size = 10)
    assert str_cleaned_long == 'Le_petit_chien_Milou_vous_dit_pipi_caca'
    assert str_cleaned_short == 'Le_petit_c'
    assert len(str_cleaned_short) == 10

def test_convsec_expected_fails():
    with pytest.raises(Exception) as e_info:
        xc._convsec("02:00.626") # error
        xc._convsec("02-00") # error

def test_convsec_expected_success(): 
    assert xc._convsec("00:00") == 0 # should be 0
    assert xc._convsec("00:33") == 33 # 33 # should be 33
    assert xc._convsec("02:00") == 120 # should be 120
    assert xc._convsec("10:01") == 601 # should be 601

def test_read_piece_of_wav():
    sig01 = xc._read_piece_of_wav(f = "./tests/test_data/test_wave1.wav", start_sec = 0.0, durat_sec = 0.5)
    sig02 = xc._read_piece_of_wav(f = "./tests/test_data/test_wave2.wav", start_sec = 1.0, durat_sec = 3.0)
    assert sig01.shape == (12000,)
    assert sig02.shape == (72000,)

def test_log_scale_spectrogram():
    S = np.random.uniform(size=(44,55)) # the f dim (44) will be chages, the t-dim (55) should stay equal
    Slog01 = xc._log_scale_spectrogram(S, fmin=0.01, bins=77)
    Slog02 = xc._log_scale_spectrogram(S, fmin=0.01, bins=256)
    assert Slog01.shape == (77, 55)
    assert Slog02.shape == (256, 55)




