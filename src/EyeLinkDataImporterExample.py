# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, SR Research Ltd., All Rights Reserved
#
# Neither name of SR Research Ltd nor the name of contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Edits:
# WDM - 2024/02/12      Alpha version
#
#
'''
This code illustrates how to utilize the functions of the EDFACCESSwraper.py to unpack an EyeLink Data File (EDF) into a structured numpy data array
To utilize the code one must first install the EyeLink Developers Kit:https://www.sr-research.com/support/thread-13.html and will also need to install numpy for you python environment: https://numpy.org/install/
'''
import os, sys
from EDFACCESSwrapper import *
from EDF2numpy import *

def main(inputs):
    errmsg = None
    options = []
    try:
        EDFI = EDF2numpy()
        # Get EDF filename argument as first arg
        edfFilename = str(inputs[0]).strip()
        # check that it's actually an EDF file
        if edfFilename.endswith('.edf')==True or edfFilename.endswith('.EDF')==True:
            # Check that file actually exists
            if os.path.isfile(edfFilename):
                # Check if there are additional arguments
                if len(inputs)>=2:
                    args = inputs[1:]
                    # if extra args exist, make sure they are in the right format
                    for i in args:
                        fixed = i.replace('=',':').replace(';',':').replace(' ','')
                        options = options + fixed.split(',')
                    inputs = ','.join(options)
                    # update optional input arguments dictionary
                    EDFI.consumeInputArgs(inputs)
                if os.path.isfile(edfFilename):
                    #read in contents of EDF file
                    EDFfileData = EDFI.readEDF(edfFilename)
                    print('Your data has been added to a numpyarray: [HEADERdata,RECORDINGdata,MESSAGEdata,SAMPLEdata,EVENTdata,IOEVENTdata]')
                    if EDFfileData[0] is None:
                        print('\tHEADERdata: 0 records;')
                    else:
                        print('\tHEADERdata: ' + str(EDFfileData[0].size) + ' records;')
                    if EDFfileData[1] is None:
                        print('\tRECORDINGdata: 0 records;')
                    else:
                        print('\tRECORDINGdata: ' + str(EDFfileData[1].size) + ' records;')
                    if EDFfileData[2] is None:
                        print('\tMESSAGEdata: 0 records;')
                    else:
                        print('\tMESSAGEdata: ' + str(EDFfileData[2].size) + ' records;')
                    if EDFfileData[3] is None:
                        print('\tSAMPLEdata: 0 records;')
                    else:
                        print('\tSAMPLEdata: ' + str(EDFfileData[3].size) + ' records;')
                    if EDFfileData[4] is None:
                        print('\tEVENTdata: 0 records;')
                    else:
                        print('\tEVENTdata: ' + str(EDFfileData[4].size) + ' records;')
                    if EDFfileData[5] is None:
                        print('\tIOEVENTdata: 0 records')
                    else:
                        print('\tIOEVENTdata: ' + str(EDFfileData[5].size) + ' records')
                    #-----------------------------------------------------
                    '''
                    PLACE YOUR ANALYSIS CODE HERE
                    '''
                    #-----------------------------------------------------
                else:
                    raise FileNotFoundError(edfFilename + " does not seem to exist. Please double check the input path and filename")
            else:
                raise FileNotFoundError(edfFilename + " does not seem to exist. Please double check the input path and filename")
        else:
            raise TypeError('Wrong file type! Only EyeLink Data Files are allowed as input file type.')
    except Exception as e:
        print('An error has occurred in Main of EyeLinkDataImporter: '+ str(e))
    except:
        print('Could not execute main import function')
if __name__ == '__main__':
    options = []
    # check for input arguments
    if len(sys.argv)>1:
        # strip args from script name
        inputs = sys.argv[1:]
        # Get EDF filename argument as first arg
        EDFfile = str(inputs[0]).strip()
        # check that it's actually an EDF file
        if EDFfile.endswith('.edf')==True or EDFfile.endswith('.EDF')==True:
            # Check that file actually exists
            if os.path.isfile(EDFfile):
                # Check if there are additional arguments
                if len(inputs)>=2:
                    args = inputs[1:]
                    # if extra args exist, make sure they are in the right format
                    for i in args:
                        fixed = i.replace('=',':').replace(';',':').replace(' ','')
                        options = options + fixed.split(',')
                    inputs = ','.join(options)
                    # Call main function
                    main([EDFfile, inputs])
                else:
                    # Call main function
                    main([EDFfile])
            else:
                raise FileNotFoundError(EDFfile + " does not seem to exist. Please double check the input filename'")
        else:
            raise TypeError('\nWrong file type! Only EyeLink Data Files are allowed as input file type') 
    else:
        print('The main function of the example will take the following Input arguments and return a numpy data structure.\n'
            + 'EyeLinkData2NumpyArray.py <EDF_FileName> <optional arguments>\n'
            + 'Input Arguments:\n\tREQUIRED:\n\t\t<EDF_FileName>\t[the path and filename of the EDF file to unpack]\n\n\tOPTIONAL:\n'
            + '\t\toutput_left_eye:1\t\t[0=Left eye data disabled;\t\t1=Left eye data enabled]\n'
            + '\t\toutput_right_eye:1\t\t[0=Right eye data disabled;\t\t1=Right eye data enabled]\n'
            + '\t\tgaze_data_type:2\t\t[0=Output Raw Data;\t\t\t1=Output HREF Data;\n\t\t\t\t\t\t2=Output Gaze Data]\n'
            + '\t\tioevents_enabled:1\t\t[0=IOEVENTS data disabled;\t\t1=IOEVENTS Data Enabled]\n'
            + '\t\tmessages_enabled:1\t\t[0=Message Events disabled;\t\t1=Message Events enabled]\n'
            + '\t\tmsg_offset_enabled:0\t\t[0=no integer offset applied;\t\t1=integer offset applied to message events]\n'
            + '\t\toutput_data_ppd:1\t\t[0=PPD Data disabled;\t\t\t1=PPD Data enabled]\n'
            + '\t\toutput_data_velocity:1\t\t[0=Velocity Data disabled;\t\t1=Velocity Data enabled]\n'
            + '\t\toutput_data_pupilsize:1\t\t[0=Pupil Data disabled;\t\t\t1=Pupil Data enabled]\n'
            + '\t\toutput_data_debugflags:0\t[0=Flag Data disabled;\t\t\t1=Flag Data enabled]\n'
            + '\t\toutput_dataviewer_commands:1\t[0=Mask DV commands from output;\t1=Include DV commands in output]\n'
            + '\t\trecinfo_enabled:1\t\t[0=Recording info disabled;\t\t1=recording info Enabled]\n'
            + '\t\tenable_consistency_check:2\t[0=consistency check disabled;\t\t1=enable consistency check and report;\n\t\t\t\t\t\t2=enable consistency check and fix]\n'
            + '\t\tenable_failsafe:0\t\t[0=fail-safe mode disabled;\t\t1=fail-safe enabled]\n'
            + '\t\tdisable_large_timestamp_check:0\t[0=timestamp check enabled;\t\t1=disable timestamp check flag]\n'
            + '\t\tevents_enabled:1\t\t[0=Event data disabled;\t\t\t1=Event Data Enabled]\n'
            + '\t\toutput_eventtype_start:1\t[0=Start Events data disabled;\t\t1=Start Events Data Enabled]\n'
            + '\t\toutput_eventtype_end:1\t\t[0=End Events data disabled;\t\t1=End Events Data Enabled]\n'
            + '\t\toutput_eventtype_saccade:1\t[0=Saccade Events data disabled;\t1=Saccade Events Data Enabled]\n'
            + '\t\toutput_eventtype_fixation:1\t[0=Fixation Events data disabled;\t1=Fixation Events Data Enabled]\n'
            + '\t\toutput_eventtype_fixupdate:0\t[0=FixUpdate Events data disabled;\t1=FixUpdate Events Data Enabled]\n'
            + '\t\toutput_eventtype_blink:1\t[0=Blink Events data disabled;\t\t1=Blink Events Data Enabled]\n'
            + '\t\toutput_eventdata_parse:1\t[0=Parse Event Data disabled;\t\t1=Parse Event Data enabled]\n'
            + '\t\toutput_eventtype_button:1\t[0=Button Events disabled;\t\t1=Button Events enabled]\n'
            + '\t\toutput_eventtype_input:1\t[0=Input Port Data Disabled;\t\t1=Input Port Data enabled]\n'
            + '\t\toutput_eventdata_averages:0\t[0=End Events data disabled;\t\t1=End Events Data Enabled]\n'
            + '\t\tsamples_enabled:0\t\t[0=Sample data disabled;\t\t1=Sample Data Enabled]\n'
            + '\t\toutput_headtargetdata_enabled:0\t[0=headTarget data disabled;\t\t1=headTarget Data Enabled]\n'
            + '\t\toutput_samplevel_model_type:0\t[0=Standard model;\t\t\t1=Fast model]\n'
            + '\t\toutput_sample_start_enabled:1\t[0=Start sample data disabled;\t\t1=Start sample Data Enabled]\n'
            + '\t\toutput_sample_end_enabled:1\t[0=End sample data disabled;\t\t1=End sample Data Enabled]\n'
            + '\t\ttrial_parse_start: "TRIALID"\t[the string used to mark the start of the trial]\n'
            + '\t\ttrial_parse_end:"TRIAL_RESULT"\t[the string used to mark the end of the trial]\n')
