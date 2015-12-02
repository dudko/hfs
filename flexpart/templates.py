""" Templates for RELEASES and COMMAND """

from string import Template

RELEASES = Template('''\
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
+++++++++++++++++ HEADER +++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++
1
001

$relStartDate $relStartTime
$relEndDate $relEndTime
$relBoxLonLL
$relBoxLatLL
$relBoxLonUR
$relBoxLatRL
1
0.0000000E+00
200.0000
$particles
1
SAMPLE_1.0''')
    
COMMAND = Template('''\
+++++++++++++ HEADER +++++++++++++++++
+++++++++++++ HEADER +++++++++++++++++
+++++++++++++ HEADER +++++++++++++++++
+++++++++++++ HEADER +++++++++++++++++
+++++++++++++ HEADER +++++++++++++++++
+++++++++++++ HEADER +++++++++++++++++
+++++++++++++ HEADER +++++++++++++++++
$simDir
$simStartDate $simStartTime
$simEndDate $simEndTime
3600
3600
900
99999999
900   SYNC
-5.0  CTL
4     IFINE
1     IOUT
1     IPOUT
1     LSUBGRID
1     LCONVECTION
1     LAGESPECTRA
0     IPIN
1     IOFR
0     IFLUX
0     MDOMAINFILL
2     IND_SOURCE
2     IND_RECEPTOR
0     MQUASILAG
0     NESTED_OUTPUT
0     LINIT_COND\n''')