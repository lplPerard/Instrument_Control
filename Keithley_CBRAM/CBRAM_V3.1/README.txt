-------------------------------------------------------------------------------------CBRAM TestBench Software-----------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Developper : Luc PERARD
Depository : https://github.com/lplPerard/Instrument_Control/tree/Class-version/Keithley_CBRAM
Current version : 2.0 (see Release note for more information)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Project Description ###

The aim of this project is to develop an all in one software to characterize and track different geometry of CBRAM cells. The software is a controller for a Keithley SMU like the 2450 or the 2400.
Waveforms and processed implemented in the software are from the state of the art of CBRAM programming. However, some sequences may implement specific method developed by the Grenoble-inp LCIS lab.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Installation ###

No specific installation is needed to get the basic functions of the software running, you just have to double-click on CBRAM_Software.exe.
However, many functionalities may need the NIVISA driver to be installed on your computer. You can install it by double-clicking on the NIVISA_19.5.exe executable file.

Please consider not separating the executable file from its directory. You can create a shortcut on your desktop with a right-click on the exe file and then selecting "send to".

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Usage ###

The main window can be divided into 3 parts :

- The menu bar, which permits to navigate through the different sequence, to save/import result or to hide/show the parameters

- The current Sequence. A sequence is basically a test bench. There are currently 3 tests implemented in the software :
    - SINGLE : Send a chosen waveform (Ramp, Pulse) and trace Voltage, current, resistance, power or I/V curve.
    - CYCLING : Try to apply the highest possible number of SET/RESET cycles to the cell. SET waveform is a ramp and reset Waveform is a negative pulse.
    - IV : Send a triangular waveform to trace the IV characteristic of the cell.

- The parameters toolbar, which permits to access most of the useful parameters such as the automatic export PATH, the unit or the SMU address.

On each sequence, you have to precise the cell on which you are working on, you can then measure the current resistance by clicking on the MEASURE button. 

ACTUALIZE SEQUENCE should be used to actualize the current view if you modify the signal parameters of a sequence. You can use it to previsualize a sequence.
START SEQUENCE generate the described signal through the SMU and then plot data. if autoexport parameter is True, it will also automatically export the result file at the precised export PATH.

The GRAPH section in each sequence should be used to actualize the graphs and modify the view. 4 graphs can be shown on the main view, you can modify them using the different selectors.
By clicking on the SAVE GRAPH button under each graph, you can save a screenshot on with the format you want (you have to precise the format when creating the file, otherwise it will generate 2 files,
one without format and .PNG file)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Support ###

For any usage question or improvement ideas, please feel free to contact the developper at : luc.perard@lcis.grenoble-inp.fr

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### License ###

The project is open-source and can be freely used for academic and research purpose. 
It should not be used without specific authorization for a professional use.

▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░▒▒▒▒░░░▒▒▒▒░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒░▒▒▒▒▒▒░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒░░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒░░░░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░▒░░░░░░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒░▒▒▒░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒░░░░░▓▓
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒░░░░░░▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
_______▒__________▒▒▒▒▒▒▒▒▒▒▒▒▒▒
______▒_______________▒▒▒▒▒▒▒▒
_____▒________________▒▒▒▒▒▒▒▒
____▒___________▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
___▒
__▒______▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
_▒______▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓
▒▒▒▒___▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓
▒▒▒▒__▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓
▒▒▒__▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓