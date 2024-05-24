# Module: EyeLinkDataImporterExample 
==================================

EyeLinkData2NumpyArray This code illustrates how to utilize the
functions of the EDFACCESSwraper.py to unpack an EyeLink Data File (EDF)
into a structured numpy data array. To utilize the code, one must first
install the EyeLink Developers Kit:
https://www.sr-research.com/support/thread-13.htmland will also need to
install numpy for you python environment: https://numpy.org/install/.

Functions
---------

## Def main(*inputs*) 

> This function consumes the name of the EDF file you want to import and
> the optional input arguments from terminal and passes those arguments
> to the functions of the EDF2Numpy to process the EDF file. The section
> of the code that says \'Place your analysis code here\' is where you
> would insert you own code to utilize the imported data.

### Inputs

-   **EDF\_FileName**

-   \[*Optional arguments*\]

    -   **output\_left\_eye**: Left eye data enabled (1) or disabled
        > (0).

    -   **output\_right\_eye**: Right eye data enabled (1) or disabled
        > (0).

    -   **messages\_enabled**: Message event data enabled (1) or
        > disabled (0).

    -   **ioevents\_enabled**: Input/Output event data enabled (1) or
        > disabled (0).

    -   **recinfo\_enabled**: Recording event data enabled (1) or
        > disabled (0).

    -   **gaze\_data\_type**: Sample gaze data type: Raw Data (0); HREF
        > Data (1); Gaze Data (2).

    -   **text\_data\_type**: any standard encoding: [Standard
        > Encodings](https://docs.python.org/3/library/codecs.html#standard-encodings)

    -   **output\_data\_ppd**: Pixel Per Degree of visual angle data
        > enabled (1) or disabled (0).

    -   **output\_data\_velocity**: Sample velocity data enabled (1) or
        > disabled (0).

    -   **output\_data\_pupilsize**: Pupil size data enabled (1) or
        > disabled (0).

    -   **output\_data\_debugflags**: output debugging flags and create
        > a .debug output file enabled (1) or disabled (0).

    -   **output\_dataviewer\_commands**: 0: Mask DV commands from
        > output; 1: Include DV commands in output.

    -   **enable\_consistency\_check**: 0: consistency check disabled;
        > 1: enable consistency check and report; 2: enable consistency
        > check and fix.

    -   **enable\_failsafe**: 0: fail-safe mode disabled; 1: fail-safe
        > enabled.

    -   **disable\_large\_timestamp\_check**: 0: timestamp check
        > enabled; 1: disable timestamp check flag.

    -   **events\_enabled**: 0: Event data disabled; 1: Event Data
        > Enabled.

    -   **output\_eventtype\_start**: 0: Start Events data disabled; 1:
        > Start Events Data Enabled.

    -   **output\_eventtype\_end**: 0: End Events data disabled; 1: End
        > Events Data Enabled.

    -   **output\_eventtype\_saccade**: 0: Saccade Events data disabled;
        > 1: Saccade Events Data Enabled.

    -   **output\_eventtype\_fixation**: 0: Fixation Events data
        > disabled;1: Fixation Events Data Enabled.

    -   **output\_eventtype\_fixupdate**: 0: FixUpdate Events data
        > disabled;1: FixUpdate Events Data Enabled.

    -   **output\_eventtype\_blink**: 0: Blink Events data disabled; 1:
        > Blink Events Data Enabled.

    -   **output\_eventdata\_parse**: 0: Parse Event Data disabled; 1:
        > Parse Event Data enabled.

    -   **output\_eventdata\_averages**: 0: End Events data disabled; 1:
        > End Events Data Enabled.

    -   **msg\_offset\_enabled**: 0: no integer offset applied; 1:
        > integer offset applied to message events.

    -   **samples\_enabled**: 0: Sample data disabled; 1: Sample Data
        > Enabled.

    -   output\_headtargetdata\_enabled: 0: headTarget data disabled; 1:
        > headTarget Data Enabled.

    -   **output\_samplevel\_model\_type**: 0: Standard model; 1: Fast
        > model.

    -   **output\_sample\_start\_enabled**: 0: Start Sample data
        > disabled; 1: Start Sample Data Enabled.

    -   **output\_sample\_end\_enabled**: 0: End Sample data disabled;
        > 1: End Sample Data Enabled.

    -   **trial\_parse\_start**: the string used to mark the start of
        > the trial.

    -   **trial\_parse\_end**: the string used to mark the end of the
        > trial.

### Return

> Returns 0 if the operation is successful.
