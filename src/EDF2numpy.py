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
"""
This code illustrates how to utilize the functions of the EDFACCESSwraper.py to unpack an EyeLink Data File (EDF) into a structured numpy data array
To utilize the code one must first install the EyeLink Developers Kit:https://www.sr-research.com/support/thread-13.html and will also need to install numpy for you python environment: https://numpy.org/install/
"""

import os, sys
from EDFACCESSwrapper import *
try:
    import numpy as np
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('\n\nIt looks like you have ' + str(e) + ' installed. Please install the following modules for this code to run: numpy') from e
except:
    raise Exception('Importation error') from None
    exit()

##--------------------------------------------------------------------------------------------------------------------------------
##Constants
##--------------------------------------------------------------------------------------------------------------------------------
MISSING_VALUE = -32768  # missing data type
MISSING_TEXT = '.'      # missing data type

EyesTracked = ['Left','Right','Binocular']
pupilData = ['Area','Diameter']
recState = ['END','START']
dataTypes = ['Samples','Events','Samples & Events']
filterType = ['Off','Standard','Extra']
trackMode = ['Pupil Only','Pupil-CR']
parseType = ['RAW','HREF','GAZE']

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
MISSING = -32768        # missing data type
LEFT_EYE = 0            # left eye index
RIGHT_EYE = 1           # right eye index
BINOCULAR = 2           # both eye index
# how events were generated
PARSEDBY_GAZE = int(0x00C0)
PARSEDBY_HREF = int(0x0080)
PARSEDBY_RAW = int(0x0040)
##-----------------------------------------------------

##--------------------------------------------------------------------------------------------------------------------------------
## EDF2numpy functions
##--------------------------------------------------------------------------------------------------------------------------------
class EDF2numpy:
    """
    This class wraps the functions defined in EDFACCESSwrapper.py to extract the data from an EDF file into a series of structured Numpy arrays.
    """
    def __init__(self):
        self.Edfwrapper = EDFACCESSwrapper()        # import EDFAccess wrapper DDL/class
        self.EDFData = None                         # pointer for EDF file
        self.errmsg = None                          # holder for exceptions
        self.CurrentEyeTracked = 0                  # The eye currently being tracked based on the RecordINFO
        self.consistencyArgs = 2                    # consistency check flags
        self.eventCount = 0                         # number of events detected
        self.sampleCount = 0                        # number of samples detected
        self.msgCount = 0                           # number of messages detected
        self.IOCount = 0                            # number of button events detected
        self.recCount = 0                           # number of start recordings events detected
        self.trialCount = 0                         # number of trials detected in the file
        self.debugfile = None                       # place holder for debug file handle
        self.options = {
            'output_left_eye': 1,                   # 0 = Left eye data disabled;       1 = Left eye data enabled
            'output_right_eye': 1,                  # 0 = Right eye data disabled;      1 = Right eye data enabled
            'messages_enabled': 0,                  # 0 = Message Events disabled;      1 = Message Events enabled
            'ioevents_enabled': 0,                  # 0 = IOEVENTS data disabled;       1 = IOEVENTS Data Enabled
            'recinfo_enabled': 0,                   # 0 = Recording info disabled       1 = recording info Enabled
            'gaze_data_type': 2,                    # 0 = Output Raw Data;              1 = Output HREF Data;                          2 = Output Gaze Data
            'text_data_type': 'utf-8',              # default is 'utf-8' but could be any standard encoding: https://docs.python.org/3/library/codecs.html#:standard-encodings
            'output_data_ppd': 1,                   # 0 = PPD Data disabled;            1 = PPD Data enabled
            'output_data_velocity': 1,              # 0 = Velocity Data disabled;       1 = Velocity Data enabled
            'output_data_pupilsize': 1,             # 0 = Pupil Data disabled;          1 = Pupil Data enabled
            'output_data_debugflags': 1,            # 0 = Flag Data disabled;           1 = Flag Data enabled
            'output_dataviewer_commands': 1,        # 0 = Mask DV commands from output  1 = Include DV commands in output
        #Consistency check toggles
            'enable_consistency_check': 2,          # 0 = consistency check disabled;   1 = enable consistency check and report;       2 = enable consistency check and fix.
            'enable_failsafe': 0,                   # 0 = fail-safe mode disabled;      1 = fail-safe enabled
            'disable_large_timestamp_check': 0,     # 0 = timestamp check enabled;      1 = disable timestamp check flag
        #Event toggles
            'events_enabled': 1,                    # 0 = Event data disabled;          1 = Event Data Enabled
            'output_eventtype_start': 1,            # 0 = Start Events data disabled;   1 = Start Events Data Enabled
            'output_eventtype_end': 1,              # 0 = End Events data disabled;     1 = End Events Data Enabled
            'output_eventtype_saccade': 1,          # 0 = Saccade Events data disabled; 1 = Saccade Events Data Enabled
            'output_eventtype_fixation': 1,         # 0 = Fixation Events data disabled;1 = Fixation Events Data Enabled
            'output_eventtype_fixupdate': 0,        # 0 = FixUpdate Events data disabled;1 = FixUpdate Events Data Enabled
            'output_eventtype_blink': 1,            # 0 = Blink Events data disabled;   1 = Blink Events Data Enabled
            'output_eventdata_parse':0,             # 0 = Parse Event Data disabled;    1 = Parse Event Data enabled
            'output_eventdata_averages': 1,         # 0 = End Events data disabled;     1 = End Events Data Enabled
            'msg_offset_enabled': 1,                # 0 = no integer offset applied    1 = integer offset applied to message events
        #Sample toggles
            'samples_enabled' : 1,                  # 0 = Sample data disabled;         1 = Sample Data Enabled
            'output_headtargetdata_enabled':1,      # 0 = headTarget data disabled;     1 = headTarget Data Enabled
            'output_samplevel_model_type': 0,       # 0 = Standard model                1 = Fast model
            'output_sample_start_enabled': 0,       # 0 = Start Sample data disabled;   1 = Start Sample Data Enabled
            'output_sample_end_enabled': 0,         # 0 = End Sample data disabled;     1 = End Sample Data Enabled
        #Set the messages that marks the onset/offset of a trial. See comments for edf_set_trial_identifier for heuristics
            'trial_parse_start': 'TRIALID',         # the string used to mark the start of the trial
            'trial_parse_end': 'TRIAL_RESULT'       # the string used to mark the end of the trial
            }
##--------------------------------------------------------------------------------------------------------------------------------
## Data array Schemas
##--------------------------------------------------------------------------------------------------------------------------------
        # SAMPLE DATA STRUCTURE
        self.SAMPLEtype = np.dtype([
            ('time','i8'),                  # timestamp in milliseconds
            ('posXLeft','f4'),              # left_eye X gaze position [RAW, HREF, or GAZE]
            ('posYLeft','f4'),              # left_eye Y gaze position [RAW, HREF, or GAZE]
            ('pupilSizeLeft','f4'),         # left_eye pupil Area or Diameter in arbitrary camera pixel units
            ('posXRight','f4'),             # right_eye X gaze position [RAW, HREF, or GAZE]
            ('posYRight','f4'),             # right_eye Y gaze position [RAW, HREF, or GAZE]
            ('pupilSizeRight','f4'),        # right_eye pupil Area or Diameter in arbitrary camera pixel units
            ('PpdX','f4'),                  # X pixels per degree
            ('PpdY','f4'),                  # Y pixels per degree
            ('velXLeft','f4'),              # left_eye X velocity in degrees per second using either the standard (default) or fast velocity model
            ('velYLeft','f4'),              # left_eye X velocity in degrees per second using either the standard (default) or fast velocity model
            ('velXRight','f4'),             # right_eye X velocity in degrees per second using either the standard (default) or fast velocity model
            ('velYRight','f4'),             # right_eye X velocity in degrees per second using either the standard (default) or fast velocity model
            ('headTrackerType','f4'),       # Head tracker data type
            ('headTargetDataX','f4'),       # Head target X data
            ('headTargetDataY','f4'),       # Head target Y data
            ('headTargetDataZ','f4'),       # Head target Z data
            ('headTargetDataFlags','f4'),   # Head target Flags data
            ('inputPortData','f4'),         # Status of the input port
            ('buttonData','f4'),            # Status of BUTTON state
            ('flags','f4'),                 # Sample Flags
            ('errors','f4'),                # Error Flags
            ('elementIndex','i8'),          # index in EDF buffer
            ('sampleIndex','i8')            # index of sample data
            ])
        # IOEVENT Data Structure
        self.IOEVENTtype = np.dtype([
            ('ioEventType','U6'),           # Event type (Button or INPUT)
            ('time','i8'),                  # Timestamp in milliseconds
            ('IOData','i4'),                # Data from IO event
            ('iotype','i4'),                # Data Type Code
            ('elementIndex','i8'),          # Index in EDF buffer
            ('ioEventIndex','i8')           # Index of Event data
            ])
        # HEADER DATA Structure
        self.HEADERtype = np.dtype([
            ('Header','O')])                # the header data for the file
        # MASTER DATA Structure
        self.MASTERtype = np.dtype([
            ('HEADER','V'),                 # header data array
            ('EVENTS','V'),                 # event data array
            ('SAMPLES','V'),                # sample data array
            ('MESSAGES','V'),               # message data array
            ('RECORDINGS','V'),             # recording data array
            ('IOEVENTS','V')                # input/output event data array
            ])
        # EVENT DATA STRUCTURE
        self.EVENTtype = np.dtype([
            ('time','i8'),                                                      # Timestamp in milliseconds
            ('eventType','U16'),                                                # Event type (StartBlink, EndBlink, StartSacc, EndSacc, StartFix, EndFix, FixUpdate, MSG)
            ('eyeTracked','U36'),                                               # Eye that generate event: Left, Right, or Binocular
            ('gazeType','U'+str(np.string_(max(parseType, key=len)).itemsize)), # Type of gaze data reported: HREF or GAZE
            ('startTime','i8'),                                                 # Start time of event type
            ('startPosX','f4'),                                                 # Start X position of event type in [GAZE or HREF]
            ('startPosY','f4'),                                                 # Start Y position of event type in [GAZE or HREF]
            ('StartPupilSize','f4'),                                            # Pupil size at start of event type
            ('startVEL','f4'),                                                  # Velocity at start of event type in degrees per second
            ('startPPDX','f4'),                                                 # X pixels per degree at start of event type
            ('startPPDY','f4'),                                                 # Y pixels per degree at start of event type
            ('endTime','i8'),                                                   # End time of event type
            ('duration','i8'),                                                  # Total duration of event for End events (endTime-startTime)
            ('endPosX','f4'),                                                   # End X position of event type in [GAZE or HREF]
            ('endPosY','f4'),                                                   # End Y position of event type in [GAZE or HREF]
            ('endPupilSize','f4'),                                              # Pupil size at end of event type
            ('endVEL','f4'),                                                    # Velocity at end of event type in degrees per second
            ('endPPDX','f4'),                                                   # X pixels per degree at end of event type
            ('endPPDY','f4'),                                                   # Y pixels per degree at end of event type
            ('avgPosX','f4'),                                                   # Average X position for duration of event type in [GAZE or HREF]
            ('avgPosY','f4'),                                                   # Average Y position for duration of event type in [GAZE or HREF]
            ('avgPupilSize','f4'),                                              # Average of pupil size over duration of event type
            ('avgVEL','f4'),                                                    # Average velocity for duration of event type in degrees per second
            ('peakVEL','f4'),                                                   # Peak velocity for duration of event type in degrees per second
            ('message','U8'),                                                   # Message data from event
            ('readFlags','f4'),                                                 # reading warnings
            ('flags','f4'),                                                     # event warnings
            ('parsedby','U'+str(np.string_(max(parseType, key=len)).itemsize)), # parsing flags
            ('status','f4'),                                                    # event status
            ('elementIndex','i8'),                                              # Index in EDF buffer
            ('eventIndex','i8')                                                 # Index of Event data
            ])
        # MESSAGEdata Structure
        self.MESSAGETtype = np.dtype([
            ('time','i8'),                                                      # Timestamp in milliseconds
            ('message','U256'),                                                 # Message data from event
            ('TimingCorrected','?'),                                            # logs if timing correction was applied
            ('messageLength','i4'),                                             # Message length from msg event
            ('readFlags','i4'),                                                 # reading warnings
            ('flags','f4'),                                                     # event warnings
            ('parsedby','U'+str(np.string_(max(parseType, key=len)).itemsize)), # parsing flags
            ('status','i4'),                                                    # event status
            ('elementIndex','i8'),                                              # Index in EDF buffer
            ('msgIndex','i8')                                                   # Index of Event data
            ])
        # RECORDINGdata Structure
        self.RECORDINGStype = np.dtype([
            ('samplingRate','i4'),                                                      # samplingRate in hertz
            ('eyeTracked','U'+str(np.string_(max(EyesTracked, key=len)).itemsize)),     # Eye that generate event: Left, Right, or Binocular
            ('pupilDataType','U'+str(np.string_(max(pupilData, key=len)).itemsize)),    # Pupil size data type: Area or Diameter
            ('trackerState','U'+str(np.string_(max(recState, key=len)).itemsize)),      # Tracker state: Start or End
            ('recordType','U'+str(np.string_(max(dataTypes, key=len)).itemsize)),       # Type of data recorded: Samples,Events, or Samples & Events
            ('parsedbyType','U'+str(np.string_(max(parseType, key=len)).itemsize)),     # Event parsing data type: RAW, HREF, GAZE
            ('filterType','U'+str(np.string_(max(filterType, key=len)).itemsize)),      # File Sample Filter type: Off,Standard or Extra 
            ('recordingMode','U'+str(np.string_(max(trackMode, key=len)).itemsize)),    # Data Recording type: Pupil Only or Pupil-CR
            ('startflags','i4'),                                                        # start event flags
            ('endflags','i4'),                                                          # end event flags
            ('elementIndex','i8'),                                                      # Index in EDF buffer
            ('recordingIndex','i8')                                                     # Index of Event data
            ])
        # create empty data arrays so we have a place to store data
        self.HEADERdata = np.empty(1,dtype=self.HEADERtype)#: HEADERdata Structure
        self.RECORDINGdata = np.empty(1,dtype=self.RECORDINGStype)#: RECORDINGdata Structure
        self.MESSAGEdata = np.empty(1,dtype=self.MESSAGETtype)#: MESSAGEdata Structure
        self.EVENTdata = np.empty(1,dtype=self.EVENTtype)#: EVENTdata Structure
        self.SAMPLEdata = np.empty(1,dtype=self.SAMPLEtype)#: SAMPLEdata Structure
        self.IOEVENTdata = np.empty(1,dtype=self.IOEVENTtype)#: IOEVENTdata Structure
        #MASTERdata = np.array([self.HEADERdata,self.RECORDINGdata,self.MESSAGEdata, self.SAMPLEdata,self.EVENTdata,self.IOEVENTdata],dtype=self.MASTERtype)
##--------------------------------------------------------------------------------------------------------------------------------
## import functions
##--------------------------------------------------------------------------------------------------------------------------------
    def consumeInputArgs(self, inputArgs):
        """
        Parse input arguments and reject bad value assignments
        Parameters
            inputArgs = A list or string of input arguments to be updated in self.options dictionary.
        Return
            Returns 0 if the operation is successful.
        """
        try:
            updates = {}
            # Check that there are arguments
            if inputArgs != None:
                # if the arguments are a string break them into  a list of individual options or treat them as a list
                if type(inputArgs) == str:
                    args = inputArgs.split(',')
                else:
                    args = inputArgs
                # break list into attribute and value pairs
                for i in args:
                    attribute =i.split(':')[0].strip()
                    value = i.split(':')[1].strip()
                    # Check that attribute is a valid option
                    if attribute in self.options:
                        # validate the value contents 
                        if value.isnumeric() or type(value)==bool:
                            if (attribute == 'gaze_data_type' or attribute == 'enable_consistency_check') and (int(value) in range(3)):
                                updates[attribute]=int(value)
                            elif int(value) in range(2):
                                updates[attribute]=int(value)
                            else:
                                print('\n!! Invalid input value assignment: "' + str(i) + '". This option will be ignored!')
                        elif attribute == 'trial_parse_start' or attribute == 'trial_parse_end' or attribute == 'text_data_type': 
                            updates[attribute]=str(value)
                        else:
                            print('\n!! Invalid input value assignment: "' + str(i) + '". This option will be ignored!')
                    else:
                        print('\n!! Invalid input argument: "' + str(i) + '". This option will be ignored!\n')
                print('...Updating the following options: '+ str(updates))
                # Force the updates to override the defaults
                self.options.update(updates)
                # Encode consistency options into binary form
                self.combineConsistencyArgs()
                return 0
            else:
                return 0
        except Exception as e:
            raise Exception('An error has occurred with consumeInputArgs: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with consumeInputArgs')
    def openEDF(self,edfFilename):
        """
        Opens EDF file and returns buffer of data/contents.
        Parameters
            edfFilename = The path or filename of the EDF you want to open
        Return
            EDFData = the handle for the EDF data contents
        """
        try:
            print('...Attempting to Open ' + str(edfFilename)+ "...")
            if os.path.isfile(edfFilename):
                if self.options['output_data_debugflags'] ==1:
                    #opening debugging file
                    if os.path.isfile(edfFilename):
                        self.debugfile = self.openDebugFile(os.path.join(os.path.dirname(edfFilename),os.path.basename(edfFilename).split('.')[0] +'.debug'))
                    else:
                        self.debugfile = self.openDebugFile(os.path.join(edfFilename +'.debug'))
                # Open EDF file and read in the data
                EDFData = self.Edfwrapper.edf_open_file(edfFilename, self.consistencyArgs, self.options['events_enabled'], self.options['samples_enabled']) # read in EDF file
                # Set trial identifiers
                self.Edfwrapper.edf_set_trial_identifier(EDFData, self.options['trial_parse_start'], self.options['trial_parse_end'])
                return EDFData
            else:
                raise Exception(str(edfFilename)+' is not a valid EDF filename')
        except Exception as e:
            raise Exception('An error has occurred with openEDF: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with openEDF')
    def closeEDF(self, edfHandle):
        """
        Close out EDF file, and the debug file if one exists
        Parameters
            edfHandle = the pointer to the EDF file created by openEDF
        Return
            Returns 0 if the operation is successful..
        """
        try:
            # If there is a debug file open, close it
            if self.debugfile != None:
                self.closeDebugFile(self.debugfile)
            # If the handle isn't empty
            if edfHandle != None:
                self.Edfwrapper.edf_close_file(edfHandle) # destroy handle
                self.EDFData = None # clear pointer
                return 0
        except Exception as e:
            raise Exception('An error has occurred with closeEDF: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with closeEDF')
    def combineConsistencyArgs(self):
        """
        Combine different consistency flags contained in self.options into one binary flag as required for openEDF()
        Return
            binary output of consistency flags
        """
        try:
            # concatenate consistency flags into binary value
            self.consistencyArgs = int(bin(int(bin(self.options['enable_consistency_check']),2) + int(bin(self.options['enable_failsafe']<<2),2) + int(bin(self.options['disable_large_timestamp_check']<<3),2)),2)
            return self.consistencyArgs
        except Exception as e:
            raise Exception('An error has occurred with combineConsistencyArgs: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with combineConsistencyArgs')
    def prealocateArraySize(self, edfFilename):
        """
        Resize the data arrays to close to their expected size for better memory management.
        Note: may over-provision so make sure to trim the arrays afterwards
        Parameters
            edfFilename = the handle to the EDF data contents generated by openEDF().
        Return
            Returns 0 if the operation is successful..
        """
        #print('...Allocating data arrays...')
        try:
            #import data
            tempData = self.Edfwrapper.edf_open_file(edfFilename, self.consistencyArgs, self.options['events_enabled'],self.options['samples_enabled']) # read in EDF file
            #set trial identifiers
            self.Edfwrapper.edf_set_trial_identifier(tempData, self.options['trial_parse_start'], self.options['trial_parse_end'])
            #initialize counters
            numberOfElements = self.Edfwrapper.edf_get_element_count(tempData)
            numberOfSamples = 0
            numberOfEvents = 0
            numberOfIOEvents = 0
            numberOfParseEvents = 0
            numberOfRecordings = 0
            numberOfMessages = 0
            maxStrLength = 0
            #Get the trial count from the API
            self.trialCount = self.Edfwrapper.edf_get_trial_count(tempData) 
            if(self.trialCount%2):
                print('There are trials not starting or ending properly.\n')
            # Cycle through buffer to count records
            while(True):
                #get current record
                DataType = self.Edfwrapper.edf_get_next_data(tempData)
                #check record type and increment counter
                if DataType == STARTSACC or DataType == STARTBLINK or DataType == STARTFIX or DataType == ENDSACC or DataType == ENDBLINK or DataType == ENDFIX or DataType == FIXUPDATE:
                    numberOfEvents +=1
                elif DataType == MESSAGEEVENT:
                    numberOfMessages +=1
                    #get the size of the message
                    strlen = self.Edfwrapper.edf_get_float_data(tempData).FEVENT.message.contents.length
                    #check if this is the longest message
                    if strlen>maxStrLength:
                        #update maximum string length
                        maxStrLength = strlen
                        strlen = None
                    else:
                        strlen = None
                elif DataType == BUTTONEVENT or DataType == INPUTEVENT:
                    numberOfIOEvents +=1
                elif DataType == STARTEVENTS or DataType == ENDEVENTS:
                    numberOfEvents +=1
                elif DataType == SAMPLE_TYPE:
                    numberOfSamples += 1
                elif DataType == STARTSAMPLES or DataType == ENDSAMPLES:
                    numberOfSamples += 1
                elif DataType == RECORDING_INFO:
                    sys.stdout.write('. ')
                    sys.stdout.flush()
                    numberOfRecordings +=1
                elif DataType == STARTPARSE or DataType == ENDPARSE or DataType == BREAKPARSE:
                    numberOfParseEvents +=1
                elif DataType == NO_PENDING_ITEMS:
                    sys.stdout.write('. ')
                    sys.stdout.flush()
                    break
                else:
                    raise Exception('Datatype unknown: ' + str(DataType) + ' cannot allocate data value')
            # resize arrays to appropriate size (may over-provision)
            strSize = '<U'+str(maxStrLength)
            # if recinfo enabled, resize RECORDINGdata structure
            if self.options['recinfo_enabled']==1:
                #preallocate arrays to the proper size
                self.RECORDINGdata = np.resize(self.RECORDINGdata,numberOfRecordings)
                #print a dot as a pseudo progress bar
                sys.stdout.write('. ')
                sys.stdout.flush()
            else:
                self.RECORDINGdata = None
            # if messages enabled, resize MESSAGEdata structure
            if self.options['messages_enabled']==1:
                #update the size of the message container to max message size - This needs to be optimized
                self.MESSAGETtype = np.dtype([('time','i8'),('message',strSize),('TimingCorrected','?'),('messageLength','i4'),('readFlags','i4'),('flags','f4'),('parsedby',np.str_),('status','i4'),('elementIndex','i8'),('msgIndex','i8')])
                #reassign data type to proper size
                self.MESSAGEdata = np.empty(1,dtype=self.MESSAGETtype)
                #preallocate arrays to the proper size
                self.MESSAGEdata = np.resize(self.MESSAGEdata,numberOfMessages)
                #print a dot as a pseudo progress bar
                sys.stdout.write('. ')
                sys.stdout.flush()
            else:
                self.MESSAGEdata = None
            # if events are enabled, resize EVENTdata structure
            if self.options['events_enabled'] ==1:
                #preallocate arrays to the proper size
                self.EVENTdata = np.resize(self.EVENTdata,numberOfEvents)
                #print a dot as a pseudo progress bar
                sys.stdout.write('. ')
                sys.stdout.flush()
            else:
                self.EVENTdata = None
            # if samples are enabled, resize SAMPLEdata structure
            if self.options['samples_enabled']==1:
                #preallocate arrays to the proper size
                self.SAMPLEdata = np.resize(self.SAMPLEdata,numberOfSamples)
                #print a dot as a pseudo progress bar
                sys.stdout.write('. ')
                sys.stdout.flush()
            else:
                self.SAMPLEdata = None
            # if ioevents are enabled, resize IOEVENTdata structure
            if self.options['ioevents_enabled']==1:
                #preallocate arrays to the proper size
                self.IOEVENTdata = np.resize(self.IOEVENTdata,numberOfIOEvents)
                #print a dot as a pseudo progress bar
                sys.stdout.write('. ')
                sys.stdout.flush()
            else:
                self.IOEVENTdata = None
            #end pseudo progress bar
            sys.stdout.write('. \n')
            sys.stdout.flush()
            # print counts for validation
            if self.options['output_data_debugflags'] ==1: 
                print('Detected Number of Elements: ' + str(numberOfElements))
                print('Detected Number of Trials: ' + str(self.trialCount))
                if self.options['samples_enabled']==1:
                    print('Detected Number of Samples: ' + str(numberOfSamples))
                    print('Size of SAMPLEdata: ' + str(self.SAMPLEdata.size))
                if self.options['events_enabled'] ==1:
                    print('Detected Number of Events: ' + str(numberOfEvents))
                    print('Size of EVENTdata: ' + str(self.EVENTdata.size))
                if self.options['messages_enabled']==1:
                    print('Detected Number of Messages: ' + str(numberOfMessages))
                    print('Size of MESSAGEdata: ' + str(self.MESSAGEdata.size))
                if self.options['recinfo_enabled']==1:
                    print('Detected Number of Recordings: ' + str(numberOfRecordings))
                    print('Size of RECORDINGdata: ' + str(self.RECORDINGdata.size))
                if self.options['ioevents_enabled']==1:
                    print('Detected Number of IOEvents: ' + str(numberOfIOEvents))
                    print('Size of IOEVENTdata: ' + str(self.IOEVENTdata.size))
                print('Detected Number of ParseEvents: ' + str(numberOfParseEvents))
            # clear variables
            tempData = None
            DataType = None
        except Exception as e:
            raise Exception('An error has occurred with prealocateArraySize: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with prealocateArraySize')
    def trimArray(self):
        """
        Remove any empty rows from the data arrays to cut out the fat.
        Return
            Returns 0 if the operation is successful..
        """
        print('...Trimming empty cells from array...')
        try:
            #print a dot as a pseudo progress bar
            sys.stdout.write('. ')
            sys.stdout.flush()
            #Trim empty rows from array
            if self.options['recinfo_enabled']==1:
                self.RECORDINGdata = np.array([i for i in self.RECORDINGdata if i['elementIndex']>0])
            #print a dot as a pseudo progress bar
            sys.stdout.write('. ')
            sys.stdout.flush()
            #Trim empty rows from array
            if self.options['messages_enabled']==1:
                self.MESSAGEdata = np.array([i for i in self.MESSAGEdata if i['elementIndex']>0])
            #print a dot as a pseudo progress bar
            sys.stdout.write('. ')
            sys.stdout.flush()
            #Trim empty rows from array
            if self.options['events_enabled'] ==1:
                self.EVENTdata = np.array([i for i in self.EVENTdata if i['elementIndex']>0])
            #print a dot as a pseudo progress bar
            sys.stdout.write('. ')
            sys.stdout.flush()
            #Trim empty rows from array
            if self.options['samples_enabled']==1:
                self.SAMPLEdata = np.array([i for i in self.SAMPLEdata if i['elementIndex']>0])
            #print a dot as a pseudo progress bar
            sys.stdout.write('. ')
            sys.stdout.flush()
            #Trim empty rows from array
            if self.options['ioevents_enabled']==1:
                self.IOEVENTdata = np.array([i for i in self.IOEVENTdata if i['elementIndex']>0])
            #end pseudo progress bar
            sys.stdout.write('\n')
            sys.stdout.flush()
            return 0
        except Exception as e:
            raise Exception('An error has occurred with trimArray: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with trimArray')
    def openDebugFile(self,Outputfilename):
        """
        Opens debug file
        Parameters
            outputfilename = the name of the debug file.
        Return
            Returns handle of debug file.
        """
        print('...Attempting to Open Debug file...')
        try:
            # Open file with write flag
            f = open(Outputfilename, "w")
            return f
        except Exception as e:
            raise Exception('An error has occurred with openDebugFile: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with openDebugFile')
    def appendDebugFile(self,fileHandle,data):
        """
        Appends new line to debug file
        Parameters
            fileHandle = The handle of the debug file created by openDebugFile()
            data = The line you would like appended to the data file
        Return
            Returns 0 if the operation is successful.
        """
        try:
            output = ""
            #Reformat data into tab delimited output
            for i in data:
                output = output + str(i) + "\t"
            output = output + '\n' 
            #Append tab delimited line to debug file
            fileHandle.write(output)
            return 0
        except Exception as e:
            raise Exception('An error has occurred with trimArray: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with trimArray')
    def closeDebugFile(self,fileHandle):
        """
        Closed debug file.
        Parameters
            fileHandle = The handle of the debug file created by openDebugFile()
        Return
            Returns 0 if the operation is successful.
        """
        print('...Attempting to close the debug file...')
        try:
            # close file
            fileHandle.close()
            # clear variables
            fileHandle = None
            self.debugfile = None
            return 0
        except Exception as e:
            print('An error has occurred with closeDebugFile: ' + str(e))
            pass
        except:
            print('Failed to property close debug file.')
            pass
    def updateEvent(self,Data,eventtype,index):
        """
        Updates event event data in the EVENTdata structure.
        Parameters
            Data = The event data from edf_get_float_data() that you would like append to the EVENTdata structure.
            eventtype = The event type code (SFIX,EFIX,FIXUPDATE,SSACC,ESACC,SBLINK,EBLINK) 
            index = The index of the EVENTdata structure that you want to overwrite with the data values
        Return
            Returns 0 if the operation is successful.
        """
        msg = ''
        try:
            #update fevent data structure to numpy structured array
            self.EVENTdata[index]['eventIndex'] = index
            self.EVENTdata[index]['eyeTracked']=EyesTracked[Data.eye]
            self.EVENTdata[index]['gazeType'] = ['RAW','HREF','GAZE'][self.options['gaze_data_type']]
            if Data.message:
                #unpack message data
                msg = repr(str(Data.message.contents.text,self.options['text_data_type']))
                self.EVENTdata[index]['message'] = np.string_(msg)
                # for i in struct.unpack('<'+str(Data.message.contents.length-1)+'c',Data.message.contents.text):
                    # msg = msg + i.decode(self.options['text_data_type'])
                # self.EVENTdata[index]['message']=msg
            else:
                self.EVENTdata[index]['message'] = MISSING_TEXT
            #Check that we should be updating event structure
            if ((Data.eye == LEFT_EYE or Data.eye == BINOCULAR) and self.options['output_left_eye'] == 1) or ((Data.eye == RIGHT_EYE or Data.eye == BINOCULAR) and self.options['output_right_eye'] == 1):
                #If start events enabled
                self.EVENTdata[index]['time']=Data.sttime
                if self.options['output_eventtype_start'] ==1:
                    self.EVENTdata[index]['startTime']=Data.sttime
                    if self.options['gaze_data_type'] == 1:
                        self.EVENTdata[index]['startPosX']=Data.hstx
                        self.EVENTdata[index]['startPosY']=Data.hsty
                    elif self.options['gaze_data_type'] == 2:
                        self.EVENTdata[index]['startPosX']=Data.gstx
                        self.EVENTdata[index]['startPosY']=Data.gsty
                    else:
                        self.EVENTdata[index]['startPosX']=MISSING_VALUE
                        self.EVENTdata[index]['startPosY']=MISSING_VALUE
                    if self.options['output_data_pupilsize'] == 1:
                        self.EVENTdata[index]['StartPupilSize']=Data.sta
                    else:
                        self.EVENTdata[index]['StartPupilSize']=MISSING_VALUE
                    if self.options['output_data_velocity'] == 1:
                        self.EVENTdata[index]['startVEL']=Data.svel
                    else:
                        self.EVENTdata[index]['startVEL']=MISSING_VALUE
                    if self.options['output_data_ppd'] == 1:
                        self.EVENTdata[index]['startPPDX']=Data.supd_x
                        self.EVENTdata[index]['startPPDY']=Data.supd_y
                    else:
                        self.EVENTdata[index]['startPPDX']=MISSING_VALUE
                        self.EVENTdata[index]['startPPDY']=MISSING_VALUE
                #If an end event update additional variables
                if (eventtype == ENDBLINK or eventtype == ENDFIX or eventtype == ENDSACC or eventtype == FIXUPDATE) and self.options['output_eventtype_end'] ==1:
                    self.EVENTdata[index]['time']=Data.entime
                    self.EVENTdata[index]['endTime']=Data.entime
                    self.EVENTdata[index]['duration']=Data.entime - Data.sttime
                    if self.options['gaze_data_type'] == 1:
                        self.EVENTdata[index]['endPosX']=Data.henx
                        self.EVENTdata[index]['endPosY']=Data.heny
                    elif self.options['gaze_data_type'] == 2:
                        self.EVENTdata[index]['endPosX']=Data.genx
                        self.EVENTdata[index]['endPosY']=Data.geny
                    else:
                        self.EVENTdata[index]['endPosX']=MISSING_VALUE
                        self.EVENTdata[index]['endPosY']=MISSING_VALUE
                    if self.options['output_data_pupilsize'] == 1:
                        self.EVENTdata[index]['endPupilSize']=Data.ena
                    else:
                        self.EVENTdata[index]['endPupilSize']=MISSING_VALUE
                    if self.options['output_data_velocity'] == 1:
                        self.EVENTdata[index]['endVEL']=Data.evel
                    else:
                        self.EVENTdata[index]['endVEL']=MISSING_VALUE
                    if self.options['output_data_ppd'] == 1:
                        self.EVENTdata[index]['endPPDX']=Data.eupd_x
                        self.EVENTdata[index]['endPPDY']=Data.eupd_y
                    else:
                        self.EVENTdata[index]['endPPDX']=MISSING_VALUE
                        self.EVENTdata[index]['endPPDY']=MISSING_VALUE
                    if self.options['gaze_data_type'] == 1:
                        self.EVENTdata[index]['avgPosX']=Data.havx
                        self.EVENTdata[index]['avgPosY']=Data.havy
                    elif self.options['gaze_data_type'] == 2:
                        self.EVENTdata[index]['avgPosX']=Data.gavx
                        self.EVENTdata[index]['avgPosY']=Data.gavy
                    else:
                        self.EVENTdata[index]['avgPosX']=MISSING_VALUE
                        self.EVENTdata[index]['avgPosY']=MISSING_VALUE
                    if self.options['output_data_pupilsize'] == 1:
                        self.EVENTdata[index]['avgPupilSize']=Data.ava
                    else:
                        self.EVENTdata[index]['avgPupilSize']=MISSING_VALUE
                    if self.options['output_data_velocity'] == 1:
                        self.EVENTdata[index]['avgVEL']=Data.avel
                        self.EVENTdata[index]['peakVEL']=Data.pvel
                    else:
                        self.EVENTdata[index]['avgVEL']=MISSING_VALUE
                        self.EVENTdata[index]['peakVEL']=MISSING_VALUE
                else:
                    self.EVENTdata[index]['time']=MISSING_VALUE
                    self.EVENTdata[index]['endTime']=MISSING_VALUE 
                    self.EVENTdata[index]['duration']=MISSING_VALUE
                    self.EVENTdata[index]['endPosX']=MISSING_VALUE
                    self.EVENTdata[index]['endPosY']=MISSING_VALUE
                    self.EVENTdata[index]['endPupilSize']=MISSING_VALUE
                    self.EVENTdata[index]['endVEL']=MISSING_VALUE
                    self.EVENTdata[index]['endPPDX']=MISSING_VALUE 
                    self.EVENTdata[index]['endPPDY']=MISSING_VALUE
                    self.EVENTdata[index]['avgPosX']=MISSING_VALUE 
                    self.EVENTdata[index]['avgPosY']=MISSING_VALUE 
                    self.EVENTdata[index]['avgPupilSize']=MISSING_VALUE 
                    self.EVENTdata[index]['avgVEL']=MISSING_VALUE 
                    self.EVENTdata[index]['peakVEL']=MISSING_VALUE
                #If debug flags enabled add some additional values
                if self.options['output_data_debugflags'] ==1:
                    self.EVENTdata[index]['readFlags']=Data.read
                    self.EVENTdata[index]['flags']=Data.flags
                    self.EVENTdata[index]['parsedby']=Data.parsedby
                    self.EVENTdata[index]['status']=Data.status
                    self.appendDebugFile(self.debugfile,self.EVENTdata[index])
                else:
                    self.EVENTdata[index]['readFlags']= MISSING_VALUE
                    self.EVENTdata[index]['flags']= MISSING_VALUE
                    self.EVENTdata[index]['parsedby']= MISSING_TEXT
                    self.EVENTdata[index]['status']= MISSING_VALUE
            return 0
        except Exception as e:
            raise Exception('An error has occurred with updateEvent: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with updateEvent')
    def updateSample(self,Data,index):
        """
        Updates sample data in the SAMPLEdata structure.
        Parameters
            Data = The sample data from edf_get_float_data() that you would like append to the SAMPLEdata structure.
            index = The index of the SAMPLEdata structure that you want to overwrite with the data values
        Return
            Returns 0 if the operation is successful.
        """
        try:
            #Update FSample data to numpy structured array
            self.SAMPLEdata[index]['sampleIndex'] = index
            self.SAMPLEdata[index]['time']=Data.time
            #Determine appropriate gaze position data for selected data type
            if self.options['gaze_data_type'] == 0:
                self.SAMPLEdata[index]['posXLeft']= Data.px.left
                self.SAMPLEdata[index]['posYLeft']= Data.py.left
                self.SAMPLEdata[index]['posXRight']= Data.px.right
                self.SAMPLEdata[index]['posYRight']= Data.py.right
            elif self.options['gaze_data_type'] == 1:
                self.SAMPLEdata[index]['posXLeft']= Data.hx.left
                self.SAMPLEdata[index]['posYLeft']= Data.hy.left
                self.SAMPLEdata[index]['posXRight']= Data.hx.right
                self.SAMPLEdata[index]['posYRight']= Data.hy.right
            elif self.options['gaze_data_type'] == 2:
                self.SAMPLEdata[index]['posXLeft']= Data.gx.left
                self.SAMPLEdata[index]['posYLeft']= Data.gy.left
                self.SAMPLEdata[index]['posXRight']= Data.gx.right
                self.SAMPLEdata[index]['posYRight']= Data.gy.right
            else:
                self.SAMPLEdata[index]['posXLeft']= MISSING_VALUE
                self.SAMPLEdata[index]['posYLeft']= MISSING_VALUE
                self.SAMPLEdata[index]['posXRight']= MISSING_VALUE
                self.SAMPLEdata[index]['posYRight']= MISSING_VALUE
            #Determine pupil if data size should be reported
            if self.options['output_data_pupilsize'] == 1:
                self.SAMPLEdata[index]['pupilSizeLeft']= Data.pa.left
                self.SAMPLEdata[index]['pupilSizeRight']= Data.pa.right
            else:
                self.SAMPLEdata[index]['pupilSizeLeft']= MISSING_VALUE
                self.SAMPLEdata[index]['pupilSizeRight']= MISSING_VALUE
            #if pupil size enabled
            if self.options['output_data_ppd'] == 1:
                self.SAMPLEdata[index]['PpdX']= Data.rx
                self.SAMPLEdata[index]['PpdY']= Data.ry
            else:
                self.SAMPLEdata[index]['PpdX']= (MISSING_VALUE)
                self.SAMPLEdata[index]['PpdY']= (MISSING_VALUE)
            #If velocity enabled set velocity output to appropriate gaze type and velocity model
            if self.options['gaze_data_type'] == 0 and self.options['output_data_velocity'] == 1 and self.options['output_samplevel_model_type'] == 0:
                self.SAMPLEdata[index]['velXLeft']= Data.rxvel.left
                self.SAMPLEdata[index]['velYLeft']= Data.ryvel.left
                self.SAMPLEdata[index]['velXRight']= Data.rxvel.right
                self.SAMPLEdata[index]['velYRight']= Data.ryvel.right
            elif self.options['gaze_data_type'] == 1 and self.options['output_data_velocity'] == 1 and self.options['output_samplevel_model_type'] == 0:
                self.SAMPLEdata[index]['velXLeft']= Data.hxvel.left
                self.SAMPLEdata[index]['velYLeft']= Data.hyvel.left
                self.SAMPLEdata[index]['velXRight']= Data.hxvel.right
                self.SAMPLEdata[index]['velYRight']= Data.hyvel.right
            elif self.options['gaze_data_type'] == 2 and self.options['output_data_velocity'] == 1 and self.options['output_samplevel_model_type'] == 0:
                self.SAMPLEdata[index]['velXLeft']= Data.gxvel.left
                self.SAMPLEdata[index]['velYLeft']= Data.gyvel.left
                self.SAMPLEdata[index]['velXRight']= Data.gxvel.right
                self.SAMPLEdata[index]['velYRight']= Data.gyvel.right
            elif self.options['gaze_data_type'] == 0 and self.options['output_data_velocity'] == 1 and self.options['output_samplevel_model_type'] == 1:
                self.SAMPLEdata[index]['velXLeft']= Data.frxvel.left
                self.SAMPLEdata[index]['velYLeft']= Data.fryvel.left
                self.SAMPLEdata[index]['velXRight']= Data.frxvel.right
                self.SAMPLEdata[index]['velYRight']= Data.fryvel.right
            elif self.options['gaze_data_type'] == 1 and self.options['output_data_velocity'] == 1 and self.options['output_samplevel_model_type'] == 1:
                self.SAMPLEdata[index]['velXLeft']= Data.fhxvel.left
                self.SAMPLEdata[index]['velYLeft']= Data.fhyvel.left
                self.SAMPLEdata[index]['velXRight']= Data.fhxvel.right
                self.SAMPLEdata[index]['velYRight']= Data.fhyvel.right
            elif self.options['gaze_data_type'] == 2 and self.options['output_data_velocity'] == 1 and self.options['output_samplevel_model_type'] == 1:
                self.SAMPLEdata[index]['velXLeft']= Data.fgxvel.left
                self.SAMPLEdata[index]['velYLeft']= Data.fgyvel.left
                self.SAMPLEdata[index]['velXRight']= Data.fgxvel.right
                self.SAMPLEdata[index]['velYRight']= Data.fgyvel.right
            else:
                self.SAMPLEdata[index]['fastVelXLeft']= MISSING_VALUE
                self.SAMPLEdata[index]['fastVelYLeft']= MISSING_VALUE
                self.SAMPLEdata[index]['fastVelXRight']= MISSING_VALUE
                self.SAMPLEdata[index]['fastVelYRight']= MISSING_VALUE
            #If Head target data enabled
            if self.options['output_headtargetdata_enabled'] == 1:
                if Data.htype != MISSING:
                    self.SAMPLEdata[index]['headTrackerType']= Data.htype
                    self.SAMPLEdata[index]['headTargetDataX']= Data.hdata.targetX
                    self.SAMPLEdata[index]['headTargetDataY']= Data.hdata.targetY
                    self.SAMPLEdata[index]['headTargetDataZ']= Data.hdata.targetDist
                    self.SAMPLEdata[index]['headTargetDataFlags']= Data.hdata.targetFlags
                else:
                    self.SAMPLEdata[index]['headTrackerType'] = MISSING_VALUE
                    self.SAMPLEdata[index]['headTrackerType']= MISSING_VALUE
                    self.SAMPLEdata[index]['headTargetDataX']= MISSING_VALUE
                    self.SAMPLEdata[index]['headTargetDataY']= MISSING_VALUE
                    self.SAMPLEdata[index]['headTargetDataZ']= MISSING_VALUE
                    self.SAMPLEdata[index]['headTargetDataFlags']= MISSING_VALUE
            #If IO Data enabled
            if self.options['ioevents_enabled'] == 1:
                self.SAMPLEdata[index]['inputPortData']= Data.inputs
                self.SAMPLEdata[index]['buttonData']= Data.buttons
            else:
                self.SAMPLEdata[index]['inputPortData']= MISSING_VALUE
                self.SAMPLEdata[index]['buttonData']= MISSING_VALUE
            #If debug flags enabled add some additional values
            if self.options['output_data_debugflags'] == 1:
                self.SAMPLEdata[index]['flags']= Data.flags
                self.SAMPLEdata[index]['errors']=Data.errors
                self.appendDebugFile(self.debugfile,self.SAMPLEdata[index])
            else:
                self.SAMPLEdata[index]['flags']= MISSING_VALUE
                self.SAMPLEdata[index]['errors']= MISSING_VALUE
            return 0
        except Exception as e:
            raise Exception('An error has occurred with updateSample: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with updateSample')
    def appendMessage(self,Data,index):
        """
        Updates event event data in the MESSAGEdata structure.
        Parameters
            data = The event data from edf_get_float_data() that you would like append to the MESSAGEdata structure.
            index = The index of the MESSAGEdata structure that you want to overwrite with the data values
        Return
            Returns 0 if the operation is successful.
        """
        decoded = ''
        offset = 0
        try:
            self.MESSAGEdata[index]['msgIndex'] = index
            self.MESSAGEdata[index]['time']=Data.sttime
            msg = repr(str(Data.message.contents.text,self.options['text_data_type']))
            self.MESSAGEdata[index]['message'] = np.string_(msg)
            #for i in msg:
                #decoded = decoded + i.decode(self.options['text_data_type'])
            # try:
                # for i in struct.unpack('<'+str(Data.message.contents.length-1)+'c',repr(str(Data.message.contents.text))):
                    # print('b')
                    # msg = msg + i.decode(self.options['text_data_type'])
                    # print('c')
            # except:
                # print('d')
                # msg = msg + repr(str(Data.message.contents.text,'utf-8'))
            # If integer offset present, adjust timestamp to corrected time value
            if self.options['msg_offset_enabled'] == 1:
                try:
                    #Check if there is an offset present
                    offset = int(decoded.split(" ")[0])
                except:
                    pass
                #If offset present handle timing correction based on input arguments
                if offset!=0 and self.options['msg_offset_enabled'] == 1:
                    self.MESSAGEdata[index]['time']= Data.sttime - int(decoded.split(" ")[0])
                    self.MESSAGEdata[index]['TimingCorrected'] = True
                else:
                    self.MESSAGEdata[index]['time']= Data.sttime
                    self.MESSAGEdata[index]['TimingCorrected'] = False
            else:
                self.MESSAGEdata[index]['time']= Data.sttime
                self.MESSAGEdata[index]['TimingCorrected'] = False
            #skip data viewer commands based on input arguments
            if self.options['output_dataviewer_commands'] == 0 and decoded.find('!V')>= 0:
                self.MESSAGEdata[index]['time'] = MISSING_VALUE
                self.MESSAGEdata[index]['message'] = MISSING_TEXT
                self.MESSAGEdata[index]['messageLength'] = MISSING_VALUE
            #If debugflags enabled add some additional values
            if self.options['output_data_debugflags'] == 1:
                self.MESSAGEdata[index]['messageLength'] = Data.message.contents.length
                self.appendDebugFile(self.debugfile,self.MESSAGEdata[index])
            else:
                self.MESSAGEdata[index]['messageLength'] = MISSING_VALUE
            return 0
        except Exception as e:
            raise Exception('An error has occurred with appendMessage: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with appendMessage')
    def appendIOEvent(self,Data,index):
        """
        Updates event event data in the IOData structure.
        Parameters
            data = The event data from edf_get_float_data() that you would like append to the IOData structure.
            index = The index of the IOData structure that you want to overwrite with the data values
        Return
            Returns 0 if the operation is successful.
        """
        try:
            self.IOEVENTdata[index]['ioEventIndex'] = index
            self.IOEVENTdata[index]['time']= Data.FEVENT.sttime
            self.IOEVENTdata[index]['IOData']= Data.IOEVENT.data
            #If debugflags enabled add some additional values
            if self.options['output_data_debugflags'] ==1:
                self.IOEVENTdata[index]['iotype']= Data.IOEVENT.itype
                self.appendDebugFile(self.debugfile,self.IOEVENTdata[index])
            else:
                self.IOEVENTdata[index]['iotype']= MISSING_VALUE
            return 0
        except Exception as e:
            raise Exception('An error has occurred with appendIOEvent: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with appendIOEvent')
    def appendRecording(self,Data,index):
        """
        Updates event event data in the RECORDINGdata structure.
        Parameters
            data = The event data from edf_get_float_data() that you would like append to the RECORDINGdata structure.
            index = The index of the RECORDINGdata structure that you want to overwrite with the data values
        Return
            Returns 0 if the operation is successful.
        """
        try:
            self.RECORDINGdata[index]['recordingIndex'] = index
            self.RECORDINGdata[index]['samplingRate'] = Data.sample_rate
            self.RECORDINGdata[index]['eyeTracked'] = EyesTracked[int(Data.eye-1)]
            #parse which eye was tracked
            if int(Data.eye) ==3:
                self.CurrentEyeTracked = slice(int(Data.eye-1))
            else:
                self.CurrentEyeTracked = int(Data.eye-1)
            self.RECORDINGdata[index]['pupilDataType'] = pupilData[int(Data.pupil_type)]
            self.RECORDINGdata[index]['trackerState'] = recState[int(Data.state)]
            self.RECORDINGdata[index]['recordType'] = dataTypes[int(Data.record_type)-1]
            #decode parsedby flags
            if abs(Data.posType) == PARSEDBY_GAZE:
                self.RECORDINGdata[index]['parsedbyType'] = 'GAZE'
            elif abs(Data.posType) == PARSEDBY_HREF:
                self.RECORDINGdata[index]['parsedbyType'] = 'HREF'
            elif abs(Data.posType) == PARSEDBY_RAW:
                self.RECORDINGdata[index]['parsedbyType'] = 'RAW'
            else:
                self.RECORDINGdata[index]['parsedbyType'] = 'Unknown.  Please Contact Support@sr-research.com'
            self.RECORDINGdata[index]['filterType'] = filterType[Data.filter_type]
            self.RECORDINGdata[index]['recordingMode'] = trackMode[int(Data.recording_mode)]
            #If debugflags enabled add some additional values
            if self.options['output_data_debugflags'] == 1:
                self.RECORDINGdata[index]['endflags'] = Data.eflags
                self.RECORDINGdata[index]['startflags'] = Data.sflags
                self.appendDebugFile(self.debugfile,self.RECORDINGdata[index])
            else:
                self.RECORDINGdata[index]['endflags'] = MISSING_VALUE
                self.RECORDINGdata[index]['startflags'] = MISSING_VALUE
            return 0
        except Exception as e:
            raise Exception('An error has occurred with appendRecording: ' + str(e))
        except:
            raise Exception('An unhandled exception has occurred with appendRecording')
    def readEDF(self,edfFilename):
        """
        Read in and parse EDF file into data structures
        Note: Make sure to consume any input arguments before running this function to make sure self.options is updated
        Parameters
            edfFilename = the path/filename of the EDF you want to extract the contents of
        Return
            Returns a Numpy array of structured numpy arrays: [HEADERdata,RECORDINGdata,MESSAGEdata,SAMPLEdata,EVENTdata,IOEVENTdata]
        """
        print('...Attempting to read in data...')
        # Resize empty arrays to appropriate size
        self.prealocateArraySize(edfFilename)
        # Import the contents of the EDF file
        self.EDFData = self.openEDF(edfFilename)
        try:
            if (self.EDFData != None):
                # Read in file preamble text
                preambleTextLength = self.Edfwrapper.edf_get_preamble_text_length(self.EDFData) # read EDF preamble text
                if(preambleTextLength > 0):
                    # Append preamble to header array
                    self.HEADERdata['Header'] = self.Edfwrapper.edf_get_preamble_text(self.EDFData,preambleTextLength+1)
                    if self.options['output_data_debugflags'] ==1: 
                        # Append to debug file
                        self.appendDebugFile(self.debugfile,self.HEADERdata['Header'])
                else:
                    print("No preamble text found")
                print('...Attempting to read contents of EDF...')
                sys.stdout.write('.')
                if self.trialCount > 0:
                    currentElement = 1
                    while(True):
                        # Get the data type of the current element in the EDF File buffer
                        DataType = self.Edfwrapper.edf_get_next_data(self.EDFData)
                        if DataType == STARTPARSE:
                            continue
                            # print('this feature is not yet enabled')
                            # if self.options['output_eventdata_parse']== 1 and self.options['events_enabled']== 1:
                                # #sparseData = self.Edfwrapper.edf_get_float_data(self.EDFData)
                        elif DataType == ENDPARSE:
                            continue
                            # print('this feature is not yet enabled')
                            # if self.options['output_eventdata_parse']== 1 and self.options['events_enabled']== 1:
                                # #eparseData = self.Edfwrapper.edf_get_float_data(self.EDFData)
                        elif DataType == BREAKPARSE:
                            continue
                            # print('this feature is not yet enabled')
                            # if self.options['output_eventdata_parse']== 1 and self.options['events_enabled']== 1:
                                # #bparseData = self.Edfwrapper.edf_get_float_data(self.EDFData)
                        elif DataType == STARTBLINK:
                            # Copy Start Blink data to Event Array
                            if self.options['output_eventtype_blink']==1 and self.options['output_eventtype_start']==1 and self.options['events_enabled']==1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "STARTBLINK"
                                sblinkData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(sblinkData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == ENDBLINK:
                            # Copy End Blink data to Event Array
                            if self.options['output_eventtype_blink']== 1 and self.options['output_eventtype_end']==1 and self.options['events_enabled']== 1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "ENDBLINK"
                                eblinkData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(eblinkData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == STARTSACC:
                            # Copy Start Saccade data to Event Array
                            if self.options['output_eventtype_saccade']== 1 and self.options['output_eventtype_start']==1 and self.options['events_enabled']== 1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "STARTSACC"
                                ssaccData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(ssaccData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == ENDSACC:
                            # Copy End Saccade data to Event Array
                            if self.options['output_eventtype_saccade']== 1 and self.options['output_eventtype_end']==1 and self.options['events_enabled']== 1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "ENDSACC"
                                esaccData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(esaccData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == STARTFIX:
                            # Copy Start Fixation data to Event Array
                            if self.options['output_eventtype_fixation']==1 and self.options['output_eventtype_start']==1 and self.options['events_enabled']==1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "STARTFIX"
                                sfixData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(sfixData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == ENDFIX:
                            # Copy End Fixation data to Event Array
                            if self.options['output_eventtype_fixation']== 1 and self.options['output_eventtype_end']==1 and self.options['events_enabled']== 1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "ENDFIX"
                                efixData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(efixData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == FIXUPDATE:
                            # Copy Fixation Update data to Event Array
                            if self.options['output_eventtype_fixupdate']== 1 and self.options['events_enabled']== 1:
                                self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                self.EVENTdata[self.eventCount]['eventType'] = "FIXUPDATE"
                                fixupdateData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.updateEvent(fixupdateData,DataType,self.eventCount)
                                self.eventCount +=1
                        elif DataType == STARTSAMPLES:
                            # Copy Start Samples to Sample Array
                            continue
                            # print('this feature is not yet enabled')
                            #if self.options['output_sample_start_enabled']== 1 and self.options['samples_enabled']== 1:
                                # self.SAMPLEdata[self.sampleCount]['elementIndex'] = currentElement
                                # sSampleData = self.Edfwrapper.edf_get_float_data(self.EDFData).FSAMPLE
                                # self.updateSample(sSampleData, self.sampleCount)
                                # self.sampleCount +=1
                        elif DataType == ENDSAMPLES:
                            # Copy end Samples to Sample Array
                            continue
                            # print('this feature is not yet enabled')
                            #if self.options['output_sample_end_enabled']== 1 and self.options['samples_enabled']== 1:
                                # self.SAMPLEdata[self.sampleCount]['elementIndex'] = currentElement
                                # sSampleData = self.Edfwrapper.edf_get_float_data(self.EDFData).FSAMPLE
                                # self.updateSample(sSampleData, self.sampleCount)
                                # self.sampleCount +=1
                        elif DataType == STARTEVENTS:
                            # Copy Start Samples to Event Array
                            continue
                            # print('this feature is not yet enabled')
                            #if self.options['output_eventtype_start']== 1 and self.options['events_enabled']== 1:
                                # self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                # self.EVENTdata[self.eventCount]['eventType'] = "STARTEVENT"
                                # startEventData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                # self.updateEvent(startEventData,DataType,self.eventCount)
                                # self.eventCount +=1
                        elif DataType == ENDEVENTS:
                            # Copy End Samples to Event Array
                            continue
                            # print('this feature is not yet enabled')
                            #if self.options['output_eventtype_end']== 1 and self.options['events_enabled']== 1:
                                # self.EVENTdata[self.eventCount]['elementIndex'] = currentElement
                                # self.EVENTdata[self.eventCount]['eventType'] = "ENDEVENTS"
                                # endEventData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                # self.updateEvent(endEventData,DataType,self.eventCount)
                                # self.eventCount +=1
                        elif DataType == MESSAGEEVENT:
                            # Copy Message data to Message Array
                            if self.options['messages_enabled']== 1 and self.options['events_enabled']== 1:
                                self.MESSAGEdata[self.msgCount]['elementIndex'] = currentElement
                                msgData = self.Edfwrapper.edf_get_float_data(self.EDFData).FEVENT
                                self.appendMessage(msgData,self.msgCount)
                                self.msgCount +=1
                        elif DataType == BUTTONEVENT:
                            # Copy Button data to IOEVENT Array
                            if self.options['ioevents_enabled']== 1 and self.options['events_enabled']== 1:
                                self.IOEVENTdata[self.IOCount]['elementIndex'] = currentElement
                                self.IOEVENTdata[self.IOCount]['ioEventType'] = "BUTTONEVENT"
                                buttData = self.Edfwrapper.edf_get_float_data(self.EDFData)
                                self.appendIOEvent(buttData,self.IOCount)
                                self.IOCount +=1
                        elif DataType == INPUTEVENT:
                            # Copy Input data to IOEVENT Array
                            if self.options['ioevents_enabled']== 1 and self.options['events_enabled']== 1:
                                self.IOEVENTdata[self.IOCount]['elementIndex'] = currentElement
                                self.IOEVENTdata[self.IOCount]['ioEventType'] = "INPUTEVENT"
                                inpData = self.Edfwrapper.edf_get_float_data(self.EDFData)
                                self.appendIOEvent(inpData,self.IOCount)
                                self.IOCount +=1
                        elif DataType == RECORDING_INFO:
                            # Copy recording data to Recording Array
                            sys.stdout.write('. ')
                            sys.stdout.flush()
                            if self.options['recinfo_enabled'] == 1:
                                self.RECORDINGdata[self.recCount]['elementIndex'] = currentElement
                                recData = self.Edfwrapper.edf_get_float_data(self.EDFData).RECORDINGS
                                self.appendRecording(recData,self.recCount)
                                self.recCount += 1
                        elif DataType == SAMPLE_TYPE:
                            # Copy Sample data to SAMPLE Array
                            if self.options['samples_enabled']== 1:
                                self.SAMPLEdata[self.sampleCount]['elementIndex'] = currentElement
                                self.SAMPLEdata[self.sampleCount]['sampleIndex'] = self.sampleCount
                                sampleData = self.Edfwrapper.edf_get_float_data(self.EDFData).FSAMPLE
                                self.updateSample(sampleData, self.sampleCount)
                                self.sampleCount +=1
                        elif DataType == NO_PENDING_ITEMS:
                            # Terminate because there is no data left in the buffer
                            sys.stdout.write('\n')
                            sys.stdout.flush()
                            print('Converted successfully: ' + str(int(self.trialCount/2)) + ' Trials; ' + str(self.sampleCount) + ' Samples; ' + str(self.eventCount) + ' Events; ' + str(self.msgCount) + ' Messages; ' + str(self.IOCount) + ' Input Events ')
                            #remove empty records arrays if items were skipped
                            self.trimArray()
                            #copy individual arrays to master array
                            self.MASTERdata = np.array([self.HEADERdata,self.RECORDINGdata,self.MESSAGEdata, self.SAMPLEdata,self.EVENTdata,self.IOEVENTdata],dtype=object)
                            self.closeEDF(self.EDFData)
                            return self.MASTERdata
                        else:
                            raise Exception("Unknown data type #: " + str(DataType) + '@element#' + str(currentElement))
                            break
                        currentElement +=1
                else:
                    raise Exception('No trials detected! Please make sure that you preallocate the data arrays prior to running the readEDF function.')
            else:
                raise Exception('EDF contains no data. Make sure the EDF is an EyeLink Data File')
        except Exception as e:
            self.closeEDF(self.EDFData)
            raise Exception('An error has occurred with readEDF: ' + str(e))
        except:
            self.closeEDF(self.EDFData)
            raise Exception('An unhandled exception has occurred with readEDF')

