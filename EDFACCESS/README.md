Module: EDFACCESSwrapper
========================

EDFACCESSwrapper This code wraps the functions and structures defined in
the EDFACCESS API C-based DLL into a python format. To utilize the code
one must first install the EyeLink Developers Kit:
https://www.sr-research.com/support/thread-13.html Once installed full
documentation of the EDFACCESS API functions and structures can be found
in the EDF Access C API user manual.pdf packaged with the API.

Classes
-------

## Class ALLF\_DATA 

> A union structure for linking multiple data types. This is used to
> capture data from edf\_get\_float\_data which can return multiple data
> types depending on where you are in the file.

-   **FEVENT** - The event structure.

-   **IMESSAGE** - The message structure.

-   **IOEVENT** - The Input/output event structure.

-   **FSAMPLE** - The sample structure.

-   **RECORDINGS** - The recording structure.

## Class FEVENT 

> A structure for storing the EDFaccess API\'s FEVENT structure this
> structure stored data for parser events(fixations, saccades, blinks,
> etc...).

-   **time** - The timestamp of the Event.

-   **etype** - The type of the event (SFIX, EFIX, SSACC, etc...).

-   **read** - The flags of which items were included.

-   **sttime** - The start time of the event.

-   **entime** - The end time of the event.

-   **hstx** - The HREF X start position.

-   **hsty** - The HREF Y start position.

-   **gstx** - The GAZE X start position.

-   **gsty** - The GAZE Y start position.

-   **sta** - The pupil size at the start of the event.

-   **henx** - The HREF X end position.

-   **heny** - The HREF Y end position.

-   **genx** - The GAZE X end position.

-   **geny** - The GAZE Y end position.

-   **ena** - The pupil size at the end of the event.

-   **havx** - The average HREF X gaze position.

-   **havy** - The average HREF Y gaze position.

-   **gavx** - The average GAZE X gaze position.

-   **gavy** - The average GAZE Y gaze position.

-   **ava** - The average pupil size during the event.

-   **avel** - The average velocity during the event.

-   **pvel** - The peak velocity during the event.

-   **svel** - The velocity at the start of the event.

-   **evel** - The velocity at the end of the event.

-   **supd\_x** - The pixels per degree at the start of the event.

-   **eupd\_x** - The pixels per degree at the end of the event.

-   **eye** - The eye that generated the event.

-   **status** - The status flags for the event.

-   **flags** - The flags generated from processing the event.

-   **input** - The state of the input port.

-   **buttons** - The state of the button definitions.

-   **parsedby** - The type of parser used to generate the event.

-   **message** - The string data from a message event.

## Class FSAMPLE 

> A structure for storing the EDFaccess API\'s FSAMPLE structure.

-   **time** - The timestamp of the sample

-   **px** - The RAW X gaze position

-   **py** - The RAW Y gaze position.

-   **hx** - The HREF X gaze position.

-   **hY** - The HREF Y gaze position.

-   **pa** - The pupil size.

-   **gx** - The GAZE X position.

-   **gy** - The GAZE Y position.

-   **rx** - The pixels per degree X.

-   **ry** - The pixels per degree Y.

-   **gxvel** - The GAZE X velocity using the standard model.

-   **gyvel** - The GAZE Y velocity using the standard model.

-   **hxvel** - The HREF X velocity using the standard model.

-   **hyvel** - The HREF Y velocity using the standard model.

-   **rxvel** - The RAW X velocity using the standard model.

-   **ryvel** - The RAW Y velocity using the standard model.

-   **fgxvel** - The GAZE X velocity using the fast model.

-   **fgyvel** - The GAZE Y velocity using the fast model.

-   **fhxvel** - The HREF X velocity using the fast model.

-   **fhyvel** - The HREF Y velocity using the fast model.

-   **frxvel** - The RAW X velocity using the fast model.

-   **fryvel** - The RAW Y velocity using the fast model.

-   **hdata** - The head target data.

-   **flags** - The flags from processing the sample.

-   **inputs** - The state of the input port.

-   **buttons** - The state of the button definitions.

-   **htype** - The head target data type.

-   **errors** - Errors generated from reading the samples.

## Class IMESSAGE 

> A structure for storing the EDFaccess API\'s IMESSAGE Structure.

-   **time** - The timestamp of the message event.

-   **mtype** - The type of message.

-   **length** - The length of the message string.

-   **text** - The string data from the message.

## Class IOEVENT 

> A structure for storing the EDFaccess API\'s IOEVENT Structure to
> store Input/Output events (input and button events).

-   **time** - The timestamp of the input/output event.

-   **itype** - The event type.

-   **data** - Data from that event.

## Class RECORDINGS 

> A structure for storing the EDFaccess API\'s RECORDINGS Structure This
> data is auto-populated each time a recording begins and ends.

-   **time** - Timestamp of the recording event.

-   **float sample\_rate** - the sampling rate of the recording.

-   **eflags** - end event processing flags.

-   **sflags** - start event flags.

-   **state** - the state of the recording (end or start).

-   **record\_type** - samples, events, or samples and events.

-   **pupil\_type** - Area or Diameter.

-   **recording\_mode** - Pupil only or Pupil-CR.

-   **filter\_type** - off, standard, or high sensitivity.

-   **posType** - Raw, HREF, or GAZE.

-   **eye** - Left, Right, or Binocular.

Class GAZEDATA 
--------------

> A structure for storing Left and Right eye data.

-   **left** - gaze data for left eye.

-   **right** - gaze data for right eye.

Class HDATA 
-----------

> A structure for storing head target data for remote mode sessions note
> some fields are not used but left for expansion purposes.

-   **targetX** - the X position of the head target sticker.

-   **targetY** - the Y position of the head target sticker.

-   **targetDist** - the Z distance of the head target sticker.

-   **targetFlags** - flags processing the head target data.

-   **hdata5** - reserved for future use.

-   **hdata6** - reserved for future use.

-   **hdata7** - reserved for future use.

-   **hdata8** - reserved for future use.

## Class LSTRING 

> A structure for storing packed message data from message events.

-   **length** - the length of the string

-   **text** - a char array of the message text

## Class BOOKMARK 

> A structure for storing bookmark data.

-   **id** - bookmark ID value.

Methods
-------

## Def checkAPI() 

> Attempt to find API files and return correct location if found.

### Return

> EDFAPI.DLL location if found or 0 if not found.

## Def edf\_close\_file(edfData) 

> Closes an EDF file pointed to by the given EDFFILE pointer and
> releases all of the resources (memory and physical file) related to
> this EDF file.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file ().

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_free\_bookmark(, edfData, bookmark) 

> Removes an existing bookmark

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file.

-   bookmark: pointer to a valid BOOKMARK structure. This structure will
    > be filled by this function. Before calling this function
    > edf\_set\_bookmark should be called and Bookmark should be
    > initialized there.

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_get\_element\_count(, edfData) 

> Returns the number of elements (samples, eye events, messages,
> buttons, etc) in the EDF file.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file.

### Returns

-   The number of elements in the EDF file

## Def edf\_get\_end\_trial\_identifier(, edfData) 

> Returns the trial identifier that marks the end of a trial.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

### Returns

-   A string that marks the end of a trial.

## Def edf\_get\_float\_data(, edfData) 

> Returns the float data with the type returned by
> edf\_get\_next\_data(). This function does not move the current data
> access pointer to the next element; use edf\_get\_next\_data() instead
> to step through the data elements.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This handle should be
    > created by calling edf\_open\_file().

### Returns

-   Returns a pointer to the ALLF\_DATA structure with the type returned
    > by edf\_get\_next\_data().

## Def edf\_get\_next\_data(, edfData) 

> Returns the type of the next data element in the EDF file pointed to
> by ∗edf. Each call to edf\_get\_next\_data() will retrieve the next
> data element within the data file. The contents of the data element
> are not accessed when using this method, only the type of the element
> is provided. Use edf\_get\_float\_data() instead to access the
> contents of the data element.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This handle should be
    > created by calling edf\_open\_file().

### Returns

-   STARTBLINK: the upcoming data is a start blink event.

-   STARTSACC: the upcoming data is a start saccade event.

-   STARTFIX: the upcoming data is a start fixation event.

-   STARTSAMPLES: the upcoming data is a start samples event.

-   STARTEVENTS: the upcoming data is a start events event.

-   STARTPARSE: the upcoming data is a start parse event.

-   ENDBLINK: the upcoming data is an end blink event.

-   ENDSACC: the upcoming data is an end saccade event.

-   ENDFIX: the upcoming data is an end fixation event.

-   ENDSAMPLES: the upcoming data is an end samples event.

-   ENDEVENTS: the upcoming data is an end events event.

-   ENDPARSE: the upcoming data is an end parse event.

-   FIXUPDATE: the upcoming data is a fixation update event.

-   BREAKPARSE: the upcoming data is a break parse event.

-   BUTTONEVENT: the upcoming data is a button event.

-   INPUTEVENT: the upcoming data is an input event.

-   MESSAGEEVENT: the upcoming data is a message event.

-   SAMPLE\_TYPE: the upcoming data is a sample.

-   RECORDING\_INFO: the upcoming data is recording info.

-   NO\_PENDING\_ITEMS: no more data left.

## Def edf\_get\_preamble\_text(, edfData, length) 

> Copies the preamble text into the given buffer. If the preamble text
> is longer than the length the text will be truncated. The returned
> content will always be null terminated.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This handle should be
    > created by calling edf\_open\_file().

-   length: length of the buffer.

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_get\_preamble\_text\_length(, edfData) 

> Returns the length of the preamble text.

### Parameters

-   edfData: a valid pointer to c EDFFILE structure. This handle should
    > be created by calling edf\_open\_file().

### Returns

-   An integer for the length of preamble text.

## Def edf\_get\_start\_trial\_identifier(, edfData) 

> Returns the trial identifier that marks the beginning of a trial.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

### Returns

-   A string that marks the beginning of a trial.

## Def edf\_get\_trial\_count(, edfData) 

> Returns the number of trials in the EDF file.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

### Returns

-   An integer for the number of trials in the EDF file.

## Def edf\_get\_trial\_header(, edfData, trial) 

> Returns the trial specific information. See the TRIAL structure for
> more details.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

-   trial: pointer to a valid TRIAL structure (note trial must be
    > initialized before being used as a parameter for this function).
    > This pointer is used to hold information of the current trial.

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_goto\_bookmark(, edfData, bookmark) 

> Jumps to the given bookmark.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file.

-   bookmark: pointer to a valid BOOKMARK structure. This structure will
    > be filled by this function. Before calling this function
    > edf\_set\_bookmark should be called and Bookmark should be
    > initialized there.

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_goto\_next\_trial(, edfData) 

> Jumps to the beginning of the next trial.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_goto\_previous\_trial(, edfData) 

> Jumps to the beginning of the previous trial.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_goto\_trial\_with\_end\_time(, edfData, end\_time) 

> Jumps to the trial that has the same start time as the given end time.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

-   end\_time: end time of the EDF trial

### Returns

-   Returns 0 if the operation is successful.

## defedf\_goto\_trial\_with\_start\_time(, edfData, start\_time) 

> Jumps to the trial that has the same start time as the given start
> time.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

-   start\_time: start time of the EDF trial

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_jump\_to\_trial(, edfData, trial) 

> Jumps to the beginning of a given trial.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file().

-   trial: trial number. This should be a value between 0 and
    > (edf\_get\_trial\_count () -- 1).

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_open\_file(, edfFilename, consistency, loadevents, loadsamples) 

> Opens the EDF file passed in by edf\_file\_name and pre-processes the
> EDF file.

### Parameters

-   edfFilename: name of the EDF file to be opened.

-   consistency: consistency check control (for the time stamps of the
    > start and end events, etc). 0, no consistency check. 1, check
    > consistency and report. 2, check consistency and fix.

-   loadevents: load/skip loading events 0, do not load events. 1, load
    > events.

-   loadsamples: load/skip loading of samples 0, do not load samples. 1,
    > load samples.

### Returns

-   If successful a pointer to EDFFILE structure is returned. Otherwise,
    > NULL is returned.

## Def edf\_set\_bookmark(, edfData, bookmark) 

> Bookmark the current position of the edf file.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file.

-   bookmark: a valid pointer to a valid BOOKMARK structure. This
    > structure will be filled by this function. Bookmark should be
    > initialized before being used by this function.

### Returns

-   Returns 0 if the operation is successful.

## Def edf\_set\_trial\_identifier(, edfData, start\_marker\_string, end\_marker\_string) 

> Sets the message strings that mark the beginning and the end of a
> trial. The message event that contains the marker string that is
> considered start or end of the trial.

### Parameters

-   edfData: a valid pointer to EDFFILE structure. This should be
    > created by calling edf\_open\_file(). start\_marker\_string:
    > string that contains the marker for beginning of a trial.
    > end\_marker\_string: string that contains the marker for end of
    > the trial.

### Returns

-   Returns 0 if the operation is successful.

### Remarks

> NOTE: The following restrictions apply for collecting the trials.

1.  The start\_marker\_string message should be before the start
    > recording (indicated by message "START").

2.  The end\_marker\_string message should be after the end recording
    > (indicated by message "END").

3.  If the start\_marker\_string is not found before start recording or
    > if the start\_marker\_string is null, start recording will be the
    > starting position of the trial. 4.If the end\_marker\_string is
    > not found after the end recording, the end recording will be the
    > ending position of the trial. 5.If start\_marker\_string is not
    > specified the string "TRIALID", if found, will be used as the
    > start\_marker\_string. 6.If the end\_marker\_string is not
    > specified, the beginning of the next trial is the end of the
    > current trial.

## Def loadAPI() 

> Attempt to load the CDLL from the default EyeLink Developers Kit
> location.

### Returns

-   Returns 0 if the operation is successful.
