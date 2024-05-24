# Module: EDF2numpy 
=================

EDF2numpy This code illustrates how to utilize the functions of the
EDFACCESSwraper.py to unpack an EyeLink Data File (EDF) into a
structured numpy data array. To utilize the code, one must first install
the EyeLink Developers Kit:
https://www.sr-research.com/support/thread-13.html and will also need to
install numpy for you python environment: https://numpy.org/install/.

Classes
-------

## Var EVENTdata 

> A structured numpy array that stores the information about Event data
> (Fixations, Saccades, Blinks, etc\...) in the data set.

### Fields

-   **time**: The timestamp of when the event was generated.

-   **eventType**: The type of event generated: StartBlink, EndBlink,
    > StartSacc, EndSacc, StartFix, EndFix, FixUpdate, or MSG.

-   **eyeTracked**: The eye that generated the event: Left, Right, or
    > Binocular.

-   **gazeType**: The gaze data type that generated the event: HREF or
    > GAZE.

-   **startTime**: The start time of the event.

-   **startPosX**: The X gaze position at the start of the event: HREF
    > or GAZE.

-   **startPosY**: The Y gaze position at the start of the event: HREF
    > or GAZE.

-   **StartPupilSize**: The pupil size at the start of the event in
    > arbitrary camera pixel units.

-   **startVEL**: The gaze velocity at start of event type in degrees
    > per second.

-   **startPPDX**: The X pixels per degree at start of event type.

-   **startPPDY**: The Y pixels per degree at start of event type.

-   **endTime**: The end time of the event.

-   **duration**: The total duration of event (endTime-startTime).

-   **endPosX**: The X gaze position at the end of the event: HREF or
    > GAZE.

-   **endPosY**: The X gaze position at the end of the event: HREF or
    > GAZE.

-   **endPupilSize**: The pupil size at the end of the event in
    > arbitrary camera pixel units.

-   **endVEL**: The gaze velocity at end of event type in degrees per
    > second.

-   **endPPDX**: The X pixels per degree at end of event type.

-   **endPPDY**: The Y pixels per degree at end of event type.

-   **avgPosX**: The average X position for duration of event type: GAZE
    > or HREF.

-   **avgPosY**: The average Y position for duration of event type: GAZE
    > or HREF.

-   **avgPupilSize**: The average pupil size for duration of event type:
    > GAZE or HREF.

-   **avgVEL**: The average velocity for duration of event type.

-   **peakVEL**: The peak velocity for duration of event type.

-   **message**: String of message data received during event.

-   **readFlags**: Flags generated from reading the message.

-   **flags**: Flags generated from processing the event.

-   **parsedby**: Which type of data was used for parsing events: RAW,
    > HREF, or GAZE.

-   **status**: The status of the event.

-   **elementIndex**: The index of the data in EDF buffer.

-   **eventIndex**: The index of the event in the EVENTdata structure.

## Var HEADERdata 

> A string variable that stores the header data from the EDF file.

## Var IOEVENTdata 

> A structured numpy array that stores the information about
> Input/Output events collected during the recording.

-   **ioEventType**: The input/output event type (Button or INPUT).

-   **time**: The timestamp of the input/output event in milliseconds.

-   **IOData**: The data from IO event.

-   **iotype**: The data type code for the event.

-   **elementIndex**: The index of the data in EDF buffer.

-   **ioEventIndex**: The index of the sample in the SAMPLEdata
    > structure.

## Var MESSAGEdata 

> A structured numpy array that stores the information about message
> events received in the EDF.

-   **time**: The timestamp of when the message was received in
    > milliseconds.

-   **message**: The string data of the message event.

-   **TimingCorrected**: If the message starts with an integer value and
    > self.options\[\'msg\_offset\_enabled\'\] is set to 1 then the
    > integer value will be subtracted from the time and this value will
    > be set to TRUE to reflect that an offset was applied to that
    > message.

-   **messageLength**: The length of the string contained in the message
    > event.

-   **readFlags**: Flags generated from reading the message.

-   **flags**: Flags generated from processing the event.

-   **parsedby**: Which type of data was used for parsing events: RAW,
    > HREF, GAZE.

-   **status**: The status of the event.

-   **elementIndex**: The index of the data in EDF buffer.

-   **msgIndex**: The index of the message event in the MESSAGEdata
    > structure.

## var RECORDINGdata 

> A structured numpy array that stores the information about the
> configuration of each recording in the data set.

-   **samplingRate**: The Sampling Rate of the recording in Hertz.

-   eyeTracked: Which type of Eye Data was recorded: Left, Right, or
    > Binocular.

-   **pupilDataType**: Which pupil size data type was recorded: Area or
    > Diameter.

-   **trackerState**: The state of the recording event: Start or End.

-   **recordType**: Which data streams were recorded: Samples,Events, or
    > Samples & Events.

-   **parsedbyType**: Which type of data used for parsing events: RAW,
    > HREF, GAZE.

-   **filterType**: Which file Sample filter was used: Off,Standard or
    > Extra.

-   **recordingMode**: Which objects were used for gaze data: Pupil Only
    > or Pupil-CR.

-   **startflags**: Flags generated for start events.

-   **endflags**: Flags generated for end events.

-   **elementIndex**: The index of the data in EDF buffer.

-   **recordingIndex**: The index of the recording in the RECORDINGdata
    > structure.

## Var SAMPLEdata 

> A structured numpy array that stores the information about each gaze
> sample collected during the recording.

-   **time**: The timestamp of when the event was generated.

-   **posXLeft**: The left\_eye X gaze position: RAW, HREF, or GAZE.

-   **posYLeft**: The Y gaze position: RAW, HREF, or GAZE.

-   **pupilSizeLeft**: The left\_eye pupil Area or Diameter in arbitrary
    > camera pixel units.

-   **posXRight**: The right\_eye X gaze position: RAW, HREF, or GAZE.

-   **posYRight**: The right\_eye Y gaze position: RAW, HREF, or GAZE.

-   **pupilSizeRight**: The right\_eye pupil Area or Diameter in
    > arbitrary camera pixel units.

-   **PpdX**: The X pixels per degree.

-   **PpdY**: The Y pixels per degree.

-   **velXLeft**: The left\_eye X velocity in degrees per second:
    > standard velocity model or fast velocity model.

-   **velYLeft**: The left\_eye Y velocity in degrees per second:
    > standard velocity model or fast velocity model.

-   **velXRight**: The right\_eye X velocity in degrees per second:
    > standard velocity model or fast velocity model.

-   **velYRight**: The right\_eye Y velocity in degrees per second:
    > standard velocity model or fast velocity model.

-   **headTrackerType**: The data type of the head target data.

-   **headTargetDataX**: The X position of the Head target sticker.

-   **headTargetDataY**: The Y position of the Head target sticker.

-   **headTargetDataZ**: The Z position of the Head target sticker.

-   **headTargetDataFlags**: Flags generated from processing the head
    > target data.

-   **inputPortData**: Status of the input port.

-   **buttonData**: State of the Button definitions.

-   **flags**: Flags generated from processing the sample.

-   **errors**: Error Flags generated from processing the sample.

-   **elementIndex**: The index of the data in EDF buffer.

-   **sampleIndex**: The index of the sample in the SAMPLEdata
    > structure.

## Var options 

> This dictionary contains a number of optional flags which will govern
> how the EDF data is processed. Most fields are binary with a value of
> 1 representing \"Enabled\" and 0 representing \"Disabled.\" Integer
> inputs are noted in parentheses.

-   **output\_left\_eye**: Left eye data enabled (1) or disabled (0).

-   **output\_right\_eye**: Right eye data enabled (1) or disabled (0).

-   **messages\_enabled**: Message event data enabled (1) or disabled
    > (0).

-   **ioevents\_enabled**: Input/Output event data enabled (1) or
    > disabled (0).

-   **recinfo\_enabled**: Recording event data enabled (1) or disabled
    > (0).

-   **gaze\_data\_type**: Sample gaze data type: Raw Data (0); HREF Data
    > (1); Gaze Data (2).

-   **text\_data\_type**: any standard encoding: [Standard
    > Encodings](https://docs.python.org/3/library/codecs.html#standard-encodings).

-   **output\_data\_ppd**: Pixel Per Degree of visual angle data
    > enabled (1) or disabled (0).

-   **output\_data\_velocity**: Sample velocity data enabled (1) or
    > disabled (0).

-   **output\_data\_pupilsize**: Pupil size data enabled (1) or disabled
    > (0).

-   **output\_data\_debugflags**: debugging flags and .debug output file
    > enabled (1) or disabled (0).

-   **output\_dataviewer\_commands**: 0: Mask DV commands from output;
    > 1: Include DV commands in output.

-   **enable\_consistency\_check**: 0: consistency check disabled; 1:
    > enable consistency check and report; 2: enable consistency check
    > and fix.

-   **enable\_failsafe**: 0: fail-safe mode disabled; 1: fail-safe
    > enabled.

-   **disable\_large\_timestamp\_check**: 0: timestamp check enabled; 1:
    > disable timestamp check flag.

-   **events\_enabled**: 0: Event data disabled; 1: Event Data Enabled.

-   **output\_eventtype\_start**: 0: Start Events data disabled; 1:
    > Start Events Data Enabled.

-   **output\_eventtype\_end**: 0: End Events data disabled; 1: End
    > Events Data Enabled.

-   **output\_eventtype\_saccade**: 0: Saccade Events data disabled; 1:
    > Saccade Events Data Enabled.

-   **output\_eventtype\_fixation**: 0: Fixation Events data disabled;1:
    > Fixation Events Data Enabled.

-   **output\_eventtype\_fixupdate**: 0: FixUpdate Events data
    > disabled;1: FixUpdate Events Data Enabled.

-   **output\_eventtype\_blink**: 0: Blink Events data disabled; 1:
    > Blink Events Data Enabled.

-   **output\_eventdata\_parse**: 0: Parse Event Data disabled; 1: Parse
    > Event Data enabled.

-   **output\_eventdata\_averages**: 0: End Events data disabled; 1: End
    > Events Data Enabled.

-   **msg\_offset\_enabled**: 0: no integer offset applied; 1: integer
    > offset applied to message events.

-   **samples\_enabled**: 0: Sample data disabled; 1: Sample Data
    > Enabled.

-   **output\_headtargetdata\_enabled**: 0: headTarget data disabled; 1:
    > headTarget Data Enabled.

-   **output\_samplevel\_model\_type**: 0: Standard model; 1: Fast
    > model.

-   **output\_sample\_start\_enabled**: 0: Start Sample data disabled;
    > 1: Start Sample Data Enabled.

-   **output\_sample\_end\_enabled**: 0: End Sample data disabled; 1:
    > End Sample Data Enabled.

-   **trial\_parse\_start**: the string used to mark the start of the
    > trial.

-   **trial\_parse\_end**: the string used to mark the end of the trial.

Methods
-------

## Def appendDebugFile (fileHandle, data) 

> Appends new line to debug file.

### Parameters

> **fileHandle**: The handle of the debug file created by
> openDebugFile() data: The line you would like appended to the data
> file.

### Return

> Returns 0 if the operation is successful.

## Def appendIOEvent (Data, index) 

> Updates event event data in the IOData structure.

### Parameters

> **data**: The event data from edf\_get\_float\_data() that you would
> like appended to the IOData structure. index: The index of the IOData
> structure that you want to overwrite with the data values.

### Return

> Returns 0 if the operation is successful.

## Def appendMessage (Data, index) 

> Updates event event data in the MESSAGEdata structure.

### Parameters

> **data**: The event data from edf\_get\_float\_data() that you would
> like appended to the MESSAGEdata structure. index: The index of the
> MESSAGEdata structure that you want to overwrite with the data values.

### Return

> Returns 0 if the operation is successful.

## Def appendRecording (Data, index) 

> Updates event event data in the RECORDINGdata structure.

### Parameters

> **data**: The event data from edf\_get\_float\_data() that you would
> like appended to the RECORDINGdata structure. index: The index of the
> RECORDINGdata structure that you want to overwrite with the data
> values.

### Return

> Returns 0 if the operation is successful.

## Def closeDebugFile (fileHandle) 

> Closed debug file.

### Parameters

> **fileHandle**: The handle of the debug file created by
> openDebugFile().

### Return

> Returns 0 if the operation is successful.

## Def closeEDF (edfHandle) 

> Close out EDF file, and the debug file if one exists.

### Parameters

> **edfHandle**: the pointer to the EDF file created by openEDF.

### Return

> Returns 0 if the operation is successful.

## Def combineConsistencyArgs () 

> Combine different consistency flags contained in .options into one
> binary flag as required for openEDF().

### Return

> binary output of consistency flags.

## Def consumeInputArgs (inputArgs) 

> Parse input arguments and reject bad value assignments.

### Parameters

> **inputArgs**: A list or string of input arguments to be updated in
> .options dictionary.

### Return

> Returns 0 if the operation is successful.

## Def openDebugFile (Outputfilename) 

> Opens debug file.

### Parameters

> **outputfilename**: the name of the debug file.

### Return

> Returns handle of debug file.

## Def openEDF (edfFilename) 

> Opens EDF file and returns buffer of data/contents.

### Parameters

> **edfFilename**: The path or filename of the EDF you want to open.

### Return

> **EDFData**: the handle for the EDF data contents.

## Def prealocateArraySize (edfFilename) 

> Resize the data arrays to close to their expected size for better
> memory management. Note: may over-provision so make sure to trim the
> arrays afterwards.

### Parameters

> **edfFilename**: the handle to the EDF data contents generated by
> openEDF().

### Return

> Returns 0 if the operation is successful.

## Def readEDF (edfFilename) 

> Read in and parse EDF file into data structures Note: Make sure to
> consume any input arguments before running this function to make sure
> .options is updated.

### Parameters

> **edfFilename**: the path/filename of the EDF you want to extract the
> contents of.

### Return

> Returns a Numpy array of structured numpy arrays:
> \[HEADERdata,RECORDINGdata,MESSAGEdata,SAMPLEdata,EVENTdata,IOEVENTdata\].

## Def trimArray () 

> Remove any empty rows from the data arrays to cut out the fat.

### Return

> Returns 0 if the operation is successful.

## Def updateEvent (Data, eventtype, index) 

> Updates event event data in the EVENTdata structure.

### Parameters

> **Data**: The event data from edf\_get\_float\_data() that you would
> like appended to the EVENTdata structure. eventtype: The event type
> code (SFIX,EFIX,FIXUPDATE,SSACC,ESACC,SBLINK,EBLINK) index: The index
> of the EVENTdata structure that you want to overwrite with the data
> values.

### Return

> Returns 0 if the operation is successful.

## Def updateSample (Data, index) 

> Updates sample data in the SAMPLEdata structure.

### Parameters

> **Data**: The sample data from edf\_get\_float\_data() that you would
> like appended to the SAMPLEdata structure. index: The index of the
> SAMPLEdata structure that you want to overwrite with the data values.

### Return

> Returns 0 if the operation is successful.
