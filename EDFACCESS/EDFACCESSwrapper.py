# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, SR Research Ltd., All Rights Reserved
# Contact: support@sr-research.com
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
This code wraps the functions and structures defined in the EDFACCESS API C-based DLL into a python format.
To utilize the code one must first install the EyeLink Developers Kit:https://www.sr-research.com/support/thread-13.html
Once installed full documentation of the EDFACCESS API functions and structures can be found in the EDF Access C API user manual.pdf packaged with the API.
'''
try:
    from ctypes import *
    import os, sys, platform, struct
    import numpy as np
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('\n\nIt looks like you have ' + str(e) + ' installed. Please install the following modules for this code to run: '+ str(e) + '\n')
except:
    raise ImportError('Importation error')
    exit()

##--------------------------------------------------------------------------------------------------------------------------------
##Constants
##--------------------------------------------------------------------------------------------------------------------------------
edfFilename = None      # placeholder for edf filename
MISSING_VALUE = -32768  # missing data type
MISSING_TEXT = '.'      # missing data type

##-----------------------------------------------------
## EDFAPI data types - Do not alter
NO_PENDING_ITEMS = 0    # End of EDF data
STARTPARSE = 1          # Trial parsing start Event
ENDPARSE = 2            # Trial parsing end event
STARTBLINK = 3          # Start of Blink Event
ENDBLINK = 4            # End of Blink Event
STARTSACC = 5           # Start of saccade event
ENDSACC = 6             # End of saccade event
STARTFIX = 7            # Start of fixation event
ENDFIX = 8              # End of fixation event
FIXUPDATE = 9           # Fixation update event
BREAKPARSE = 10         # Parse break event
STARTSAMPLES = 15       # Start of events in block
ENDSAMPLES = 16         # End of samples in block
STARTEVENTS = 17        # start of events in block
ENDEVENTS = 18          # end of events in block
MESSAGEEVENT = 24       # Message event
BUTTONEVENT = 25        # Button state change
INPUTEVENT = 28         # Input port event
RECORDING_INFO = 30     # Recording event
SAMPLE_TYPE = 200       # Sample event
PARSEDBY_GAZE = int(0x00C0)  # how events were generated
PARSEDBY_HREF = int(0x0080)
PARSEDBY_RAW = int(0x0040)
MISSING = -32768        # missing data type
LEFT_EYE = 0            # left eye index
RIGHT_EYE = 1           # right eye index
BINOCULAR = 2           # both eye index
##-----------------------------------------------------

##--------------------------------------------------------------------------------------------------------------------------------
## EDFACCESS data structures
##--------------------------------------------------------------------------------------------------------------------------------
class GAZEDATA(Structure):
    '''
    A structure for storing Left and Right eye data
    '''
    _fields_ = [
        ('left',c_float),
        ('right',c_float)
        ]

class BOOKMARK(Structure):
    '''
    A structure for storing bookmark data
    '''
    _fields_ = [('id',c_int)]

class LSTRING(Structure):
    '''
    A structure for storing packed message data from message events
    '''
    _fields_ = [('length', c_ushort),
                ('text', c_char*64000)]

class HDATA(Structure):
    '''
    A structure for storing head target data for remote mode sessions
    note some fields are not used but left for expansion purposes
    '''
    _fields_=[
        ('targetX', c_int16),
        ('targetY',  c_int16),
        ('targetDist', c_int16),
        ('targetFlags', c_int16),
        ('hdata5', c_int16),
        ('hdata6', c_int16),
        ('hdata7', c_int16),
        ('hdata8', c_int16)]

class RECORDINGS(Structure):
    '''
    A structure for storing the EDFaccess API's RECORDINGS Structure
    This data is auto-populated each time a recording begins and ends
    '''
    _fields_=[
        ('time',c_uint32),
        ('sample_rate',c_float),
        ('eflags', c_uint16),
        ('sflags', c_uint16),
        ('state', c_byte),
        ('record_type', c_byte),
        ('pupil_type', c_byte),
        ('recording_mode', c_byte),
        ('filter_type', c_byte),
        ('posType', c_byte),
        ('eye', c_byte) ]

class IMESSAGE(Structure):
    '''
    A structure for storing the EDFaccess API's IMESSAGE Structure
    '''
    _fields_=[
        ('time', c_uint32),
        ('mtype', c_int16),
        ('length', c_int16),
        ('text', POINTER(LSTRING))]

class IOEVENT(Structure):
    '''
    A structure for storing the EDFaccess API's IOEVENT Structure to store Input/Output events (input and button events)
    '''
    _fields_=[
        ('time', c_uint32),
        ('itype', c_int16),
        ('data', c_uint16)]

class FSAMPLE(Structure):
    '''
    A structure for storing the EDFaccess API's FSAMPLE structure
    '''
    _fields_ = [
        ('time',c_uint32),
        ('px',GAZEDATA),
        ('py',GAZEDATA),
        ('hx',GAZEDATA),
        ('hY',GAZEDATA),
        ('pa',GAZEDATA),
        ('gx',GAZEDATA),
        ('gy',GAZEDATA),
        ('rx',c_float),
        ('ry',c_float),
        ('gxvel',GAZEDATA),
        ('gyvel',GAZEDATA),
        ('hxvel',GAZEDATA),
        ('hyvel',GAZEDATA),
        ('rxvel',GAZEDATA),
        ('ryvel',GAZEDATA),
        ('fgxvel',GAZEDATA),
        ('fgyvel',GAZEDATA),
        ('fhxvel',GAZEDATA),
        ('fhyvel',GAZEDATA),
        ('frxvel',GAZEDATA),
        ('fryvel',GAZEDATA),
        ('hdata',HDATA),
        ('flags',c_uint16),
        ('inputs',c_uint16),
        ('buttons',c_uint16),
        ('htype',c_int16),
        ('errors',c_uint16) ]

class FEVENT(Structure):
    '''
    A structure for storing the EDFaccess API's FEVENT structure 
    this structure stored data for parser events(fixations, saccades, blinks, etc...)
    '''
    _fields_=[
        ('time', c_uint32),
        ('etype', c_int16),
        ('read', c_uint16),
        ('sttime', c_uint32),
        ('entime', c_uint32),
        ('hstx', c_float),
        ('hsty', c_float),
        ('gstx', c_float),
        ('gsty', c_float),
        ('sta', c_float),
        ('henx', c_float),
        ('heny', c_float),
        ('genx', c_float),
        ('geny', c_float),
        ('ena', c_float),
        ('havx', c_float),
        ('havy', c_float),
        ('gavx', c_float),
        ('gavy', c_float),
        ('ava', c_float),
        ('avel', c_float),
        ('pvel', c_float),
        ('svel', c_float),
        ('evel', c_float),
        ('supd_x', c_float),
        ('eupd_x', c_float),
        ('supd_y', c_float),
        ('eupd_y', c_float),
        ('eye', c_int16),
        ('status', c_uint16),
        ('flags', c_uint16),
        ('input', c_uint16),
        ('buttons', c_uint16),
        ('parsedby', c_uint16),
        ('message', POINTER(LSTRING))]

class ALLF_DATA(Union):
    '''
    A union structure for linking multiple data types. This is used to capture data from edf_get_float_data
    which can return multiple data types depending on where you are in the file
    '''
    _fields_=[
        ('FEVENT',FEVENT),
        ('IMESSAGE',IMESSAGE),
        ('IOEVENT',IOEVENT),
        ('FSAMPLE',FSAMPLE),
        ('RECORDINGS',RECORDINGS)]

##--------------------------------------------------------------------------------------------------------------------------------
## EDFACCESS API functions
##--------------------------------------------------------------------------------------------------------------------------------
class EDFACCESSwrapper:
    '''
    A class to wrap all of the functions from the EDFaccess API
    '''
    def __init__(self):
        self.EDFlib = None #placeholder for CDLL once imported
        self.err = c_int(0) #store error data
        self.errmsg = None
        self.EDFData = None #place holder for the pointer used for the EDFfile once imported
        self.loadAPI() # Load CDLL
    def checkAPI(self):
        '''
        Attempt to find API files and return correct location if found
        RETURN:
            EDFAPI.DLL location if found or 0 if not found
        '''
        try:
            shared_lib_path = 0
            print('...Determining Environment...')
            if sys.platform.startswith('win32'):                                             #if windows
                msg = 'Windows with '
                windowsEDKpath = os.path.join(os.environ['ProgramFiles(x86)'], 'SR Research','EyeLink')
                if os.path.exists(windowsEDKpath):
                    libpathx86 = os.path.join(os.environ['ProgramFiles(x86)'], 'SR Research','EyeLink','libs')
                    libpathx64 = os.path.join(os.environ['ProgramFiles(x86)'], 'SR Research','EyeLink','libs','x64')
                    #figure out python architecture
                    if os.environ['PROCESSOR_ARCHITECTURE'].endswith('64'):     #if 64 bit Python
                        msg = msg + 'python x64 detected'
                        if os.path.exists(libpathx64):
                            shared_lib_path = os.path.join(libpathx64,'edfapi64.dll')
                            print(msg)
                            return shared_lib_path
                        else:
                            raise RuntimeError('We could not find an installation of the EyeLink Developers Kit on your system.\nExpected directory: ' + str(windowsEDKpath) + '.\nPlease make sure that you have the EyeLink Developers Kit installed')
                    else:                                                      #default to 32 bit Python
                        msg = msg + 'python x86 detected'
                        if os.path.exists(libpathx86):
                            shared_lib_path = os.path.join(libpathx86,'edfapi.dll')
                            print(msg)
                            return shared_lib_path
                        else:
                            raise RuntimeError('We could not find an installation of the EyeLink Developers Kit on your system.\nExpected directory: ' + str(windowsEDKpath) + '.\nPlease make sure that you have the EyeLink Developers Kit installed')
                else:
                    self.errmsg = 'We could not find an installation of the EyeLink Developers Kit on your system.\nExpected directory: ' + str(windowsEDKpath) + '.\nPlease make sure that you have the EyeLink Developers Kit installed'
            elif sys.platform.startswith('darwin'):        # if macOS
                print('macOS detected')
                macOSEDKpath = os.sep + os.path.join('Library','Frameworks','edfapi.framework')
                if os.path.exists(macOSEDKpath):
                            shared_lib_path = os.path.join(macOSEDKpath,'edfapi')
                            return shared_lib_path
                else:
                    raise RuntimeError('We could not find an installation of the EyeLink Developers Kit on your system.\nExpected directory: ' + str(macOSEDKpath) + '.\nPlease make sure that you have the EyeLink Developers Kit installed')
            elif sys.platform.startswith('linux'):         # if Linux
                print('Linux detected')
                LinuxEDKpath = os.sep + os.path.join('usr','lib','x86_64-linux-gnu')
                if os.path.exists(LinuxEDKpath):
                            shared_lib_path = os.path.join(LinuxEDKpath,'libedfapi.so')
                            return shared_lib_path
                else:
                    raise RuntimeError('We could not find an installation of the EyeLink Developers Kit on your system.\nExpected directory: ' + str(LinuxEDKpath) + '.\nPlease make sure that you have the EyeLink Developers Kit installed')
            else:
                raise OSError('The detected operating system environment is not yet supported: ' + str(sys.platform)+ '.  Please contact support@sr-research.com')
        except Exception as e:
            print('An error has occurred in the CheckAPI function: '+ str(e))
        except:
            raise Exception('Unhandled exception with checkAPI function')
    def loadAPI(self):
        '''
        Attempt to load the CDLL from the default EyeLink Developers Kit location
        '''
        libpath = None
        try:
            lib_path = self.checkAPI()
            if lib_path != None:
                print('...Attempting to load EDFAPI from ' + lib_path + ' ...')
                self.EDFlib = CDLL(lib_path)
                print('Successfully loaded API from '+ lib_path)
                if not self.EDFlib == None:
                    ##-------------------------------------------------------------------------------
                    ##C binds
                    ##-------------------------------------------------------------------------------
                    #edf_open_file
                    self.EDFlib.edf_open_file.restype=c_void_p
                    self.EDFlib.edf_open_file.argtypes=[c_char_p, c_int,c_int,c_int,POINTER(c_int)]
                    #edf_close_file
                    self.EDFlib.edf_close_file.restype=c_int
                    self.EDFlib.edf_close_file.argtypes=[c_void_p]
                    #edf_get_preamble_text
                    self.EDFlib.edf_get_preamble_text.restype=c_int
                    self.EDFlib.edf_get_preamble_text.argtypes=[c_void_p, c_char_p, c_int]
                    #edf_get_preamble_text_length
                    self.EDFlib.edf_get_preamble_text_length.restype=c_int
                    self.EDFlib.edf_get_preamble_text_length.argtypes=[c_void_p]
                    #edf_get_element_count
                    self.EDFlib.edf_get_element_count.restype=c_int
                    self.EDFlib.edf_get_element_count.argtypes=[c_void_p]
                    #edf_get_trial_count
                    self.EDFlib.edf_get_trial_count.restype=c_int
                    self.EDFlib.edf_get_trial_count.argtypes=[c_void_p]
                    #edf_get_next_data
                    self.EDFlib.edf_get_next_data.restype=c_int
                    self.EDFlib.edf_get_next_data.argtypes=[c_void_p]
                    #edf_get_float_data
                    self.EDFlib.edf_get_float_data.restype=POINTER(ALLF_DATA)
                    self.EDFlib.edf_get_float_data.argtypes=[c_void_p]
                    #edf_set_trial_identifier
                    self.EDFlib.edf_set_trial_identifier.restype=c_int
                    self.EDFlib.edf_set_trial_identifier.argtypes=[c_void_p, c_char_p, c_char_p]
                    #edf_get_start_trial_identifier
                    self.EDFlib.edf_get_start_trial_identifier.restype=c_int
                    self.EDFlib.edf_get_start_trial_identifier.argtypes=[c_void_p]
                    #edf_get_end_trial_identifier
                    self.EDFlib.edf_get_end_trial_identifier.restype=c_int
                    self.EDFlib.edf_get_end_trial_identifier.argtypes=[c_void_p]
                    #edf_jump_to_trial
                    self.EDFlib.edf_jump_to_trial.restype=c_int
                    self.EDFlib.edf_jump_to_trial.argtypes=[c_void_p, c_int]
                    #edf_get_trial_header
                    self.EDFlib.edf_get_trial_header.restype=c_int
                    self.EDFlib.edf_get_trial_header.argtypes=[c_void_p, c_int]
                    #edf_goto_previous_trial
                    self.EDFlib.edf_goto_previous_trial.restype=c_int
                    self.EDFlib.edf_goto_previous_trial.argtypes=[c_void_p]
                    #edf_goto_next_trial
                    self.EDFlib.edf_goto_next_trial.restype=c_int
                    self.EDFlib.edf_goto_next_trial.argtypes=[c_void_p]
                    #edf_goto_trial_with_start_time
                    self.EDFlib.edf_goto_trial_with_start_time.restype=c_int
                    self.EDFlib.edf_goto_trial_with_start_time.argtypes=[c_void_p, c_int]
                    #edf_goto_trial_with_end_time
                    self.EDFlib.edf_goto_trial_with_end_time.restype=c_int
                    self.EDFlib.edf_goto_trial_with_end_time.argtypes=[c_void_p, c_int]
                    #edf_set_bookmark
                    self.EDFlib.edf_set_bookmark.restype=c_int
                    self.EDFlib.edf_set_bookmark.argtypes=[c_void_p, c_void_p]
                    #edf_free_bookmark
                    self.EDFlib.edf_free_bookmark.restype=c_int
                    self.EDFlib.edf_free_bookmark.argtypes=[c_void_p, c_void_p]
                    #edf_goto_bookmark
                    self.EDFlib.edf_goto_bookmark.restype=c_int
                    self.EDFlib.edf_goto_bookmark.argtypes=[c_void_p, c_void_p]
                    return self.EDFlib
                else:
                    raise RuntimeError('EDFACCESS API could not be loaded.')
            else:
                raise RuntimeError('We could not find an installation of the EyeLink Developers Kit on your system.\nPlease make sure that you have the EyeLink Developers Kit installed')
        except Exception as e:
            print('An error has occurred in the LoadAPI function: '+ str(e))
        except:
            raise Exception('Unhandled exception with LoadAPI function')
##--------------------------------------------------------------------------------------------------------------------------------
## EDF Data Access Functions
##--------------------------------------------------------------------------------------------------------------------------------
    def edf_open_file(self, edfFilename, consistency, loadevents, loadsamples):
        '''
        Opens the EDF file passed in by edf_file_name and pre-processes the EDF file.
        Parameters:
            edfFilename = name of the EDF file to be opened.
            consistency  = consistency check control (for the time stamps of the start and end events, etc). 0, no consistency check. 1,
                check consistency and report. 2, check consistency and fix.
            loadevents  = load/skip loading events 0, do not load events. 1, load events.
            loadsamples  = load/skip loading of samples 0, do not load samples. 1, load samples.
        Returns:
            if successful a pointer to EDFFILE structure is returned. Otherwise NULL is returned.
        '''
        try:
            self.EDFData = self.EDFlib.edf_open_file(edfFilename.encode('utf-8'), c_int(consistency), c_int(loadevents), c_int(loadsamples),self.err)
            if self.EDFData == None:
                raise RuntimeError('EDF File could not be opened. EDF API errval= ' + str(self.err.value) + ' Please contact support@sr-research.com') 
            return self.EDFData
        except Exception as e:
            print('An error has occurred in the edf_open_file function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_open_file function')
    def edf_close_file(self, edfData):
        '''
        Closes an EDF file pointed to by the given EDFFILE pointer and releases all of the resources (memory and physical file) related to this EDF file.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file ().
        Returns:
            Returns 0 if the operation is successful.
        '''
        try:
            result = self.EDFlib.edf_close_file(self.EDFData)
            if result != 0:
                raise RuntimeError('Could not close EDF file')
            return result
        except Exception as e:
            print('An error has occurred in the edf_close_file function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_close_file function')
    def edf_get_preamble_text_length(self, edfData):
        '''
        Returns the length of the preamble text.
        Parameters:
            edfData = a valid pointer to c EDFFILE structure. This handle should be created by calling edf_open_file().
        Returns:
            An integer for the length of preamble text
        '''
        try:
            EDFpreambleLength = self.EDFlib.edf_get_preamble_text_length(self.EDFData)
            return EDFpreambleLength
        except Exception as e:
            print('An error has occurred in the edf_get_preamble_text_length function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_preamble_text_length function')
    def edf_get_preamble_text(self, edfData, length):
        '''
        Copies the preamble text into the given buffer. If the preamble text is longer than the length the text will be truncated.
        The returned content will always be null terminated.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This handle should be created by calling edf_open_file().
            length = length of the buffer.
        Returns:
            Returns 0 if the operation is successful.
        '''
        try:
            preamble = create_string_buffer(1024)
            EDFpreamble = self.EDFlib.edf_get_preamble_text(self.EDFData, preamble, c_int(length))
            preamble = str(preamble.value.decode()).strip()
            if len(str(preamble).strip()) >= 0:
                print('Preamble Text:\n####################\n' + str(preamble) + '\n####################')
            else:
                print('Preamble Text Empty')
            return preamble
        except Exception as e:
            print('An error has occurred in the edf_get_preamble_text function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_preamble_text function')
    def edf_get_trial_count(self, edfData):
        '''
        Returns the number of trials in the EDF file.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
        Returns:
            an integer for the number of trials in the EDF file
        '''
        try:
            trialCount = self.EDFlib.edf_get_trial_count(edfData)
            print(str(int(trialCount/2)) + " trials detected.")
            return trialCount
        except Exception as e:
            print('An error has occurred in the edf_get_trial_count function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_trial_count function')
    def edf_get_element_count(self, edfData):
        '''
        Returns the number of elements (samples, eye events, messages, buttons, etc) in the EDF file.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file.
        Returns:
            the number of elements in the EDF file
        '''
        try:
            EDFcount = self.EDFlib.edf_get_element_count(edfData)
            return EDFcount
        except Exception as e:
            print('An error has occurred in the edf_get_element_count function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_element_count function')
    def edf_get_next_data(self, edfData):
        '''
        Returns the type of the next data element in the EDF file pointed to by ∗edf. Each call to edf_get_next_data() will
        retrieve the next data element within the data file. The contents of the data element are not accessed using this
        method, only the type of the element is provided. Use edf_get_float_data() instead to access the contents of the data element.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This handle should be created by calling edf_open_file().
        Returns:
            STARTBLINK = the upcoming data is a start blink event.
            STARTSACC = the upcoming data is a start saccade event.
            STARTFIX = the upcoming data is a start fixation event.
            STARTSAMPLES = the upcoming data is a start samples event.
            STARTEVENTS = the upcoming data is a start events event.
            STARTPARSE = the upcoming data is a start parse event.
            ENDBLINK = the upcoming data is an end blink event.
            ENDSACC = the upcoming data is an end saccade event.
            ENDFIX = the upcoming data is an end fixation event.
            ENDSAMPLES = the upcoming data is an end samples event.
            ENDEVENTS = the upcoming data is an end events event.
            ENDPARSE = the upcoming data is an end parse event.
            FIXUPDATE = the upcoming data is a fixation update event.
            BREAKPARSE = the upcoming data is a break parse event.
            BUTTONEVENT = the upcoming data is a button event.
            INPUTEVENT = the upcoming data is an input event.
            MESSAGEEVENT = the upcoming data is a message event.
            SAMPLE_TYPE = the upcoming data is a sample.
            RECORDING_INFO = the upcoming data is a recording info.
            NO_PENDING_ITEMS = no more data left.
        '''
        try:
            EDFdata = self.EDFlib.edf_get_next_data(edfData)
            return EDFdata
        except Exception as e:
            print('An error has occurred in the edf_get_next_data function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_next_data function')
    def edf_get_float_data(self, edfData):
        '''
        Returns the float data with the type returned by edf_get_next_data(). This function does not move the current data
        access pointer to the next element; use edf_get_next_data() instead to step through the data elements.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This handle should be created by calling edf_open_file().
        Returns:
            Returns a pointer to the ALLF_DATA structure with the type returned by edf_get_next_data().
        '''
        try:
            EDFdata = self.EDFlib.edf_get_float_data(edfData).contents
            return EDFdata
        except Exception as e:
            print('An error has occurred in the edf_get_float_data function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_float_data function')
##--------------------------------------------------------------------------------------------------------------------------------
## Trial Related Functions
##--------------------------------------------------------------------------------------------------------------------------------
    def edf_set_trial_identifier(self, edfData, start_marker_string, end_marker_string):
        '''
        Sets the message strings that mark the beginning and the end of a trial. The message event that contains the
        marker string is considered start or end of the trial.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
            start_marker_string = string that contains the marker for beginning of a trial.
            end_marker_string = string that contains the marker for end of the trial.
        Returns
            0 if no error occurred.
        Remarks
            NOTE: The following restrictions apply for collecting the trials.
            1.The start_marker_string message should be before the start recording (indicated by message “START”).
            2.The end_marker_string message should be after the end recording (indicated by message “END”).
            3.If the start_marker_string is not found before start recording or if the start_marker_string is null,
                start recording will be the starting position of the trial.
            4.If the end_marker_string is not found after the end recording, end recording will be the ending position of the trial.
            5.If start_marker_string is not specified the string “TRIALID”, if found, will be used as the start_marker_string.
            6.If the end_marker_string is not specified, the beginning of the next trial is the end of the current trial.
        '''
        try:
            trialID = self.EDFlib.edf_set_trial_identifier(edfData, start_marker_string.encode('utf-8'), end_marker_string.encode('utf-8'))
            return trialID
        except Exception as e:
            print('An error has occurred in the edf_set_trial_identifier function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_set_trial_identifier function')
    def edf_get_start_trial_identifier(self, edfData):
        '''
        Returns the trial identifier that marks the beginning of a trial.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
        Returns
            a string that marks the beginning of a trial.
        '''
        try:
            trialID = self.EDFlib.edf_get_start_trial_identifier(edfData)
            return trialID
        except Exception as e:
            print('An error has occurred in the edf_get_start_trial_identifier function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_start_trial_identifier function')
    def edf_get_end_trial_identifier(self, edfData):
        '''
        Returns the trial identifier that marks the end of a trial.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
        Returns
            a string that marks the end of a trial.
        '''
        try:
            trialID = self.EDFlib.edf_get_end_trial_identifier(edfData)
            return trialID
        except Exception as e:
            print('An error has occurred in the edf_get_end_trial_identifier function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_end_trial_identifier function')
    def edf_jump_to_trial(self, edfData, trial):
        '''
        Jumps to the beginning of a given trial.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
            trial = trial number. This should be a value between 0 and edf_get_trial_count ()- 1.
        Returns:
            Returns 0 if the operation is successful.
        '''
        try:
            trialData = self.EDFlib.edf_jump_to_trial(edfData, trial)
            return trialData
        except Exception as e:
            print('An error has occurred in the edf_jump_to_trial function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_jump_to_trial function')
    def edf_get_trial_header(self, edfData, trial):
        '''
        Returns the trial specific information. See the TRIAL structure for more details.
        Parameters:
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
            trial = pointer to a valid TRIAL structure (note trial must be initialized before being used as a
                parameter for this function). This pointer is used to hold information of the current trial.
        Returns:
            Returns 0 if the operation is successful.
        '''
        try:
            trialheader = self.EDFlib.edf_get_trial_header(edfData, trial)
            return trialheader
        except Exception as e:
            print('An error has occurred in the edf_get_trial_header function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_get_trial_header function')
    def edf_goto_previous_trial(self, edfData):
        '''
        Jumps to the beginning of the previous trial.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            prevTrial = self.EDFlib.edf_goto_previous_trial(edfData)
            return prevTrial
        except Exception as e:
            print('An error has occurred in the edf_goto_previous_trial function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_goto_previous_trial function')
    def edf_goto_next_trial(self, edfData):
        '''
        Jumps to the beginning of the next trial.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            nextTrial = self.EDFlib.edf_goto_next_trial(edfData)
            return nextTrial
        except Exception as e:
            print('An error has occurred in the edf_goto_next_trial function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_goto_next_trial function')
    def edf_goto_trial_with_start_time(self, edfData, start_time):
        '''
        Jumps to the trial that has the same start time as the given start time.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
            start_time = start time of the EDF trial
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            trialData = self.EDFlib.edf_goto_trial_with_start_time(edfData, start_time)
            return trialData
        except Exception as e:
            print('An error has occurred in the edf_goto_trial_with_start_time function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_goto_trial_with_start_time function')
    def edf_goto_trial_with_end_time(self, edfData, end_time):
        '''
        Jumps to the trial that has the same start time as the given end time.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file().
            end_time = end time of the EDF trial
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            trialData = self.EDFlib.edf_goto_trial_with_end_time(edfData, end_time)
            return trialData
        except Exception as e:
            print('An error has occurred in the edf_goto_trial_with_end_time function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_goto_trial_with_end_time function')
#--------------------------------------------------------------------------------------------------------------------------------
## Bookmark Related Functions
##--------------------------------------------------------------------------------------------------------------------------------
    def edf_set_bookmark(self, edfData, bookmark):
        '''
        Bookmark the current position of the edf file.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file.
            bookmark = pointer to a valid BOOKMARK structure. This structure will be filled by this function. Bookmark should
                be initialized before being used by this function.
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            result = self.EDFlib.edf_set_bookmark(edfData, bookmark)
            return result
        except Exception as e:
            print('An error has occurred in the edf_set_bookmark function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_set_bookmark function')
    def edf_free_bookmark(self, edfData, bookmark):
        '''
        Removes an existing bookmark
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file.
            bookmark = pointer to a valid BOOKMARK structure. This structure will be filled by this function. Before
                calling this function edf_set_bookmark should be called and Bookmark should be initialized there.
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            result = self.EDFlib.edf_free_bookmark(self,edfData, bookmark)
            return result
        except Exception as e:
            print('An error has occurred in the edf_free_bookmark function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_free_bookmark function')
    def edf_goto_bookmark(self, edfData, bookmark):
        '''
        Jumps to the given bookmark.
        Parameters
            edfData = a valid pointer to EDFFILE structure. This should be created by calling edf_open_file.
            bookmark = pointer to a valid BOOKMARK structure. This structure will be filled by this function. Before
                calling this function edf_set_bookmark should be called and Bookmark should be initialized there.
        Returns
            Returns 0 if the operation is successful.
        '''
        try:
            EDFbookmark = self.EDFlib.edf_goto_bookmark(edfData, bookmark)
            return EDFbookmark
        except Exception as e:
            print('An error has occurred in the edf_goto_bookmark function: '+ str(e))
        except:
            raise Exception('Unhandled exception with edf_goto_bookmark function')
