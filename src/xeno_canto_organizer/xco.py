# -------------
# Author : Serge Zaugg
# Description : Main functionality of this codebase
# -------------

import os
import re
import json
import requests
import pandas as pd
import unidecode
import numpy as np 
import wave
import scipy.signal as sgn 
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt  
from PIL import Image
import struct
import subprocess
import datetime
import getpass

class XCO():

    def __init__(self, 
                 start_path, 
                 XC_API_URL = 'https://xeno-canto.org/api/3/recordings' # v3
                 ):
        self.XC_API_URL = XC_API_URL
        self.start_path = start_path 
        self.download_tag = 'downloaded_data' 
        self.recs_pool = []

    #----------------------------------
    # (1) helper functions
    
    def _convsec(self, x):
        """
        Description : Convert 'mm:ss' (str) to seconds (int)
        """
        x = x.split(':')
        x = int(x[0])*60 + int(x[1])
        return(x)
    
    def _clean_xc_filenames(self, s, max_string_size):
        """
        Description : keep only alphanumeric characters in a string and remove '.mp3'
        """
        stri = s.replace('.mp3', '')
        stri = unidecode.unidecode(stri)
        stri = stri.replace(' ', '_').replace('-', '_')
        stri = re.sub(r'[^a-zA-Z0-9_]', '', stri)
        stri = stri[0:max_string_size]
        return(stri)
    
    def _read_piece_of_wav(self, f, start_sec, durat_sec): 
        """ 
        Description : Reads a piece of a wav file 
        Arguments :
            f : (str), full path to a wav file 
            start_sec : (float), time location in seconds where the piece to be extracted starts
            durat_sec : (float), duration in seconds of the piece to be extracted 
        Returns: A 1D numpy-array (float) containing the extracted piece of the waveform  
        """
        # read wav 
        wave_file = wave.open(f, 'r')
        # extract metadata from wave file header
        fs = wave_file.getframerate()
        n_ch = wave_file.getnchannels()  
        sampwidth = wave_file.getsampwidth()
        # read bytes from the chunk of 
        wave_file.setpos(int(fs*start_sec)) 
        Nread = int(fs*durat_sec)
        sig_byte = wave_file.readframes(Nread) #read the all the samples from the file into a byte string
        wave_file.close()
        # convert bytes to a np-array 
        # struct.unpack(fmt, string)
        # h : int16 signed
        # H : int16 unsigned
        # i : int32 signed
        # I : int32 unsigned
        if sampwidth == 2 :
            unpstr = '<{0}h'.format(Nread*n_ch) # < = little-endian h = 2 bytes ,16-bit 
        else:
            raise ValueError("Not a 16 bit signed integer audio formats.")
        # convert byte string into a list of ints
        sig = (struct.unpack(unpstr, sig_byte)) 
        sig = np.array(sig, dtype=float)
        # convert from int to float
        sig = sig / ((2**(sampwidth*8))/2)
        # return 
        return(sig)

    def _log_scale_spectrogram(self, S, fmin=0.01, bins=128):
        # draft provied by https://chatgpt.com, edited by Serge
        """
        """
        n_freqs, _ = S.shape
        lin_freqs = np.linspace(0, 0.5, n_freqs)
        log_freqs = np.logspace(np.log10(fmin), np.log10(0.5), bins)
        # Interpolator over the frequency axis
        interp_func = interp1d(lin_freqs, S, axis=0, bounds_error=False, fill_value=0.0)
        S_log = interp_func(log_freqs)
        return(S_log) 



    #----------------------------------
    # (2) main methods 

    def download_summary(self, 
        gen = None,
        sp = None,
        cnt = None,
        q = None,
        len_min = None,
        len_max = None ,
        verbose = False,
        # full_query_string = None
        ):
        """ 
        Description: Prepares a data frame with info (XC metadata) on files to be downloaded 
        """
        # if full_query_string is not None:
        try:
            self.__apikey
        except:    
            self.__apikey = getpass.getpass("Key for XC-API-3: ")
        # helper functions 
        def aq(s):
            return('"' + s + '"')
        def nq_min(f):
            return('"' + '>' + str(f) + '"')
        def nq_max(f):
            return('"' + '<' + str(f) + '"')
        # handle when argument was not provided
        gen_p        = 'gen:'  + aq(gen)          if gen      is not None else ""
        sp_p         = 'sp:'   + aq(sp)           if sp       is not None else ""
        cnt_p        = 'cnt:'  + aq(cnt)          if cnt      is not None else ""
        q_p          = 'q:'    + aq(q)            if q        is not None else ""
        len_min_p    = 'len:'  + nq_min(len_min)  if len_min  is not None else ""
        len_max_p    = 'len:'  + nq_max(len_max)  if len_max  is not None else ""
        # start 
        last_page_reached = False
        page_counter = '&page=1'
        while not last_page_reached: 
            # construct final query key
            query_string = '?query=' + gen_p + sp_p + cnt_p + q_p + len_min_p + len_max_p + page_counter + '&key=' + self.__apikey
            full_query_string = self.XC_API_URL + query_string
            # API requests:
            r = requests.get(full_query_string, allow_redirects=True)
            # handle if invalid key 
            if r.status_code == 401:
                del(self.__apikey)
                return(r)
            elif r.status_code != 200:   
                return(r)
            else:
                j = r.json()
                recs = j['recordings']
                if verbose: print('numRecordings', j['numRecordings'])
                # remove objects 
                _ = [a.pop('sono') for a in recs]
                _ = [a.pop('osci') for a in recs]
                # exclude files with no-derivative licenses
                if verbose: print('Before removing lic=nd: ', len(recs))
                recs = [a for a in recs if not 'nd' in a['lic'].lower()] 
                if verbose: print('After removing lic=nd:  ', len(recs))
                # append items from current page 
                self.recs_pool.extend(recs)
                # handle next iter 
                pages_current = j['page']
                pages_total = j['numPages']
                if verbose: print("page " , str(pages_current), " / " , str(pages_total))
                # prepare page counter for next iter 
                page_counter = '&page=' + str(pages_current + 1)
                if pages_current >= pages_total:
                    last_page_reached = True 
        if len(recs) <= 0:
            print("This query fetched 0 records!")
      
    def compile_df_and_save(self, verbose = False):
        """
        """
        self.df_recs = pd.DataFrame(self.recs_pool)
        self.df_recs['full_spec_name'] = self.df_recs['gen'] + ' ' +  self.df_recs['sp']
        if verbose: print("Before removing duplicates: ", self.df_recs.shape)
        self.df_recs.drop_duplicates(inplace=True, subset = 'id')
        if verbose: print("After removing duplicates:  ", self.df_recs.shape)
        self.df_recs.to_pickle(os.path.join(self.start_path, 'summary_of_data.pkl') )
        print("Fetched info for " + str(self.df_recs.shape[0]) + " files")

    def reload_local_summary(self):
        """ re-load summary as attribute if necessary"""
        self.df_recs = pd.read_pickle(os.path.join(self.start_path, 'summary_of_data.pkl'))

    def download_audio_files(self, verbose = False):
        """ 
        Description : Downloads mp3 files from XCO.XC_API_URL and stores them in XCO.start_path
        Arguments : df_recs (data frame) : A dataframe returned by XCO.download_summary()
        Returns: Files are written to XCO.start_path; nothing is returned into Python session
        """
        # Create directory to where files will be downloaded
        source_path = os.path.join(self.start_path, self.download_tag + '_orig')
        if not os.path.exists(source_path):
            os.mkdir(source_path)
        # download one file for each row
        new_filename = []
        for i,row_i in self.df_recs.iterrows():
            re_i = row_i.to_dict()
            if verbose:
                print("Downloading file: ", re_i["file-name"])
            full_download_string = re_i["file"]
            # actually download files 
            rq = requests.get(full_download_string, allow_redirects=True)
            # simplify and clean filename
            finam2 = self._clean_xc_filenames(s = re_i["file-name"], max_string_size = 30)
            # write file to disc
            open(os.path.join(source_path, finam2 + '.mp3') , 'wb').write(rq.content)
            new_filename.append(finam2)
        # print(new_filename)
        df_all_extended = self.df_recs
        df_all_extended['file_name_stub'] = new_filename 
        df_all_extended['full_spec_name'] = df_all_extended['gen'] + ' ' +  df_all_extended['sp']
        df_all_extended.to_pickle(os.path.join(self.start_path, self.download_tag + '_meta.pkl') )
        print("Done! downloaded " + str(i+1) + " files") 

    def mp3_to_wav(self, conversion_fs, verbose = False):
            """   
            Description : Looks for files ending in .mp3 and attempt to convert them to wav with ffmpeg
            Arguments :   conversion_fs : the sampling rate of the saved wav file  
            Returns:      Writes wav files to disc
            """
            all_dirs = next(os.walk(os.path.join(self.start_path)))[1]
            thedir = [a for a in all_dirs if "_orig" in a and self.download_tag in a][0]
            path_source = os.path.join(self.start_path, thedir)
            path_destin = os.path.join(self.start_path, thedir.replace('_orig','_wav_' + str(conversion_fs) + 'sps'))
            if not os.path.exists(path_destin):
                os.mkdir(path_destin)
            all_mp3s = [a for a in os.listdir(path_source) if "mp3" in a]
            # loop over mp3 file and convert to wav by call to ffmpeg
            self.failed_wav_conv_li = []
            for ii, finam in enumerate(all_mp3s):
                if verbose:
                    print("Converting to wav: " + finam)
                patin = os.path.join(path_source, finam)
                paout = os.path.join(path_destin, finam.replace('.mp3','.wav' ))
                try:
                    retcode = subprocess.call(['ffmpeg', 
                        '-y', # -y overwrite without asking 
                        '-i', patin, # '-i' # infile must be specifitd after -i
                        '-ar', str(conversion_fs), # -ar rate set audio sampling rate (in Hz)
                        '-ac', '1', # stereo to mono, take left channel # -ac channels set number of audio channels
                        paout
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if retcode != 0:
                        print(f"Process failed with return code {retcode}", " --- File: " + finam)
                        self.failed_wav_conv_li.append(finam)
                except:
                    print("An exception occurred during mp3-to-wav conversion with ffmpeg!")
                    self.failed_wav_conv_li.append(finam)
            # finishing up        
            n_fails = len(self.failed_wav_conv_li)        
            print("Done! successfully converted: " + str(ii+1-n_fails) + ' files' + ', failed: ' + str(n_fails))

    def extract_spectrograms(self, fs_tag, segm_duration, segm_step = 1.0, win_siz = 256, win_olap = 128,  
                             specsub = True, log_f_min = None, max_segm_per_file = None, colormap = 'gray', eps = 1e-10, verbose = False):
        """
        Description : Process wav file by segments, for each segment makes a spectrogram, and saves a PNG
        Arguments : 
            fs_tag (float) : If wav with different fs are available, this will force to use only one fs.
            segm_duration (float) : Duration of a segment in seconds
            segm_step (float) : Overlap between consecutive segments, 1.0 = no overlap, 0.5 = 50% overlap
            win_siz (int) : Size in nb of bins of the FFT window used to compute the short-time fourier transform
            win_olap (int) : Size in nb of bins of the FFT window overlap
            specsub (Boolean) : Set True to apply spectral subtraction (suppresses stationary background noise), else set to False
            max_segm_per_file (int) : limit the max number of segments extracted per file
            colormap (str) : 
                Set to 'gray' to write one-channel images (default)
                Other strings will map spectrogram to 3-channel color images e.g. 'viridis', 'inferno', 'magma', 'inferno', 'plasma', 'twilight' 
                For full list see see plt.colormaps()
        Returns : PNG images are saved to disc
        """

        assert win_olap < win_siz, "win_olap must be strictly smaller that win_siz"

        #-------------------------------- 
        all_dirs = next(os.walk(os.path.join(self.start_path)))[1]
        thedir = [a for a in all_dirs if "_wav_" in a and self.download_tag in a]
        thedir = [a for a in thedir if str(fs_tag) in a]

        # check if dir exists
        if len(thedir) <= 0:
            print("WARNING - fs_tag is not equal to any of the dirs created with xco.mp3_to_wav()")
            return(None)
        else:
            4+4
        
        thedir = thedir[0] # why ?
        path_source = os.path.join(self.start_path,  thedir)
        tstmp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
        path_destin = os.path.join(self.start_path,  'images_' + str(fs_tag) + 'sps' + tstmp)

        if not os.path.exists(path_destin):
            os.mkdir(path_destin)
        all_wavs = [a for a in os.listdir(path_source) if "wav" in a]
        allWavFileNames = [os.path.join(path_source, a) for a in all_wavs]

        # pragmatically get time and frequency axes 
        sig_rand = np.random.uniform(size=int(segm_duration*fs_tag))   
        f_axe, t_axe, _ = sgn.spectrogram(x = sig_rand, fs = fs_tag, nperseg = win_siz, noverlap = win_olap, return_onesided = True)
      
        # save parameters for later traceability
        params_dict = {
            "sampling_frequency" : fs_tag,
            "segment_duration_sec" : segm_duration,
            "segment_step_size" : segm_step,
            "fft_window_size_bins" : win_siz,
            "fft_window_overlap_bins" : win_olap,
            "colormap" : colormap,
            "specsub" : specsub,
            "max_segm_per_file" : max_segm_per_file,
            "eps" : eps,
            "frequency_axis" : f_axe.tolist(),
            "time_axis" : t_axe.tolist(),
            }
        with open(os.path.join(path_destin, "_feature_extraction_parameters.json"), 'w') as f:
            json.dump(params_dict, f, indent=4)    

        # loop over wav files 
        tot_counter = 0
        self.failed_spectro_li = []
        for wavFileName in allWavFileNames: 
            try:
                # open wav file and get meta-information 
                waveFile = wave.open(wavFileName, 'r')
                myFs = waveFile.getframerate()
                totNsam = waveFile.getnframes()
                totDurFile_s = totNsam / myFs
                waveFile.close()

                # make sure fs is correct 
                if myFs != fs_tag:
                    print("Wav file ignored because its sampling frequency is not equal to fs_tag !  " + wavFileName)
                    continue
                if verbose:
                    print("Extracting spectrograms: " + wavFileName)
                
                # loop over segments within file   
                totNbSegments = int(totDurFile_s / segm_duration)  

                for ii in np.arange(0, (totNbSegments - 0.99), segm_step):
                    # print(ii)
                    if max_segm_per_file is not None:
                        if ii+1 >= max_segm_per_file:
                            break 
                    try:
                        startSec = ii*segm_duration
                        sig = self._read_piece_of_wav(f = wavFileName, start_sec = startSec, durat_sec = segm_duration)
                        sig = sig - sig.mean() # de-mean
                        # compute spectrogram
                        f_axe, t_axe, X = sgn.spectrogram(
                            x = sig, 
                            fs = myFs, 
                            window = 'hamming', 
                            nperseg = win_siz, 
                            noverlap = win_olap, 
                            detrend = 'constant', 
                            return_onesided = True, 
                            scaling = 'spectrum', 
                            mode = 'psd')
                        # remove nyquist freq
                        X = X[:-1, :]
                           
                        # log-transform 
                        X = np.log10(X + eps)

                        # spectral subtraction
                        if specsub:
                            noise_magnitude = np.median(X, axis=1, keepdims=True)
                            X = X - noise_magnitude
                            X = np.maximum(X, 0.0)  

                        # log mapping of freqs
                        if log_f_min is not None:
                            X = self._log_scale_spectrogram(S = X, fmin=log_f_min, bins=X.shape[0])

                        # flip
                        X = np.flip(X, axis=0) # so that high freqs at top of image 
                        # print('flip:' , X.shape)


                        # normalize 
                        X = X - X.min()
                        X = X/X.max()
                        # capture when X/X.max() went wrong (mostly at file start due to many zeros: fade-in)
                        if np.isnan(X).sum() > 0:   
                            # print(np.isnan(X).sum(), X.min(), X.max())
                            self.failed_spectro_li.append(wavFileName + " sec " + str(startSec))
                            continue
                        # apply color map  
                        if colormap == "gray":
                            im = Image.fromarray((X[:, :] * 255).astype(np.uint8))
                        else:           
                            cm = plt.get_cmap(colormap)
                            colored_image = cm(X)
                            im = Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8))
                        # print("PIL image size: ", im.size, im.mode)
                        # save as image 
                        startSec_str = "{:005.3f}".format(startSec).zfill(8) # make a fixed length string for start second
                        image_save_path = os.path.join(path_destin, os.path.basename(wavFileName).replace('.wav','_segm_') + str(startSec_str) + ".png")
                        im.save(image_save_path)
                        tot_counter += 1
                    except:
                        print("Error during loop over segments of wav file!")
            except:
                print("Error while reading wav file!")
        n_fails = len(self.failed_spectro_li)  
        print("Done! sucessfully extracted " + str(tot_counter) + " spectograms" + ', failed: ' + str(n_fails)) 
         
# devel code - supress execution if this is imported as module 
if __name__ == "__main__":
    plt.colormaps()
    xc = XCO(start_path = "aaa") 
    xc._clean_xc_filenames(s = "öüä%&/sdf__caca_.55&/())äöüöä5.mp3", max_string_size = 20)

    


