#--------------------------------
# Author : Serge Zaugg
# Description : Basic tests to check if process runs through
#--------------------------------

# import os
# import pandas as pd 
# import shutil
import pytest

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
str_dirty = "+++///Le_p%%eti(t_chi)èn_Milöu-vöüs_di(=)t_pi**pi_çac`^a.mp3"
str_cleaned_long  = xc._clean_xc_filenames(s = str_dirty, max_string_size = 999)
str_cleaned_short = xc._clean_xc_filenames(s = str_dirty, max_string_size = 10)

#----------------------------------------------
# perform unit tests

def test_clean_xc_filenames():
    assert str_cleaned_long == 'Le_petit_chien_Milou_vous_dit_pipi_caca'
    assert str_cleaned_short == 'Le_petit_c'
    assert len(str_cleaned_short) == 10

def test_convsec_expected_fails():
    with pytest.raises(Exception) as e_info:
        xc._convsec("02:00.626") # error
        xc._convsec("02-00") # error

def test_convsec_expected_success(): 
    xc._convsec("00:00") == 0 # should be 0
    xc._convsec("00:33") == 33 # should be 33
    xc._convsec("02:00") == 120 # should be 120
    xc._convsec("10:01") == 601 # should be 601






