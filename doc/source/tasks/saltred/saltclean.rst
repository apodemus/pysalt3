.. _saltclean:

*********
saltclean
*********


Name
====

saltclean -- Gain, debias, flat field, xtalk and mosaic images in one step

Usage
=====

saltclean rawpath obslog gaindb xtalkfile geomfile subover trim median
function order rej_lo rej_hi niter masbias subbias (cleanup)
(clobber) logfile verbose (status)

Parameters
==========


*rawpath*
    String. Abolute or relative path to the directory which contains the
    input raw FITS files.

*obslog*
    String. The name of a FITS table file containing output from the
    saltlog task. If the file resides in a separate directory then the
    absolute or relative path must be supplied with the file name.

*gaindb*
    String. This is the name and path to an ascii table that contains the
    amplifier gains specific to a SALT instrument. The table is used to
    gain-correct amplifier raw count images. Gain is assumed to be uniform
    across an individual amplifier but assumed to vary from amplifier to
    amplifier.  An example of the table format follows::

        # Database of SALTICAM CCD amplifier properties
        # 10 Aug 2006 - Telescope Data
        # READOUT GAINSTATE GAIN RDNOISE BIAS AMP
        SLOW FAINT  1.06  3.60  300 amp1
        SLOW FAINT  0.99  3.43  300 amp2
        SLOW FAINT  1.06  3.71  300 amp3
        SLOW FAINT  1.07  3.69  300 amp4
        SLOW BRIGHT 2.32  3.98  300 amp1
        SLOW BRIGHT 2.17  3.78  300 amp2
        SLOW BRIGHT 2.32  4.07  300 amp3
        SLOW BRIGHT 2.33  3.96  300 amp4
        FAST FAINT  1.55  5.22  300 amp1
        FAST FAINT  1.45  5.11  300 amp2
        FAST FAINT  1.53  5.51  300 amp3
        FAST FAINT  1.58  5.61  300 amp4
        FAST BRIGHT 4.26  6.39  300 amp1
        FAST BRIGHT 3.96  5.88  300 amp2
        FAST BRIGHT 4.21  6.35  300 amp3
        FAST BRIGHT 4.32  7.02  300 amp4

    READOUT and GAINSTATE are the CCD readout speed and gain setting
    respectively. The GAIN column refers to the multiplicative gain
    factor. RDNOISE refers to readout noise and BIAS refers to typical CCD
    bias levels.  These data are calibrated regularly at the telescope and
    provided by the SALT project. Recent versions of the table are
    provided in the SALT IRAF distribution at
    salt$salticam/data/SALTICAMamps.dat and salt$pfis/data/PFISamps.dat,
    and updates will be publicized on the SALT web site at www.salt.ac.za.

*xtalkfile*
    String. This is the name of an ascii table that contains the CCD amplifier
    crosstalk coeffcients.  The table is used to subtract cross-talk contamination
    from the CCD amplifier images. Crosstalk is assumed to occur at a constant
    level across an individual amplifier, but the coefficients are assumed to
    vary across amplifer pairs. An example of the table format follows::

        # PFIS CCD amplifier crosstalk data
        # from 20041201 gain = bright distortion image, outer amps duplicated
        # Date    VCTM     2       1       4       3        6        5
        #         SRC      1       2       3       4        5        6
        2004-01-01     .001474 .001474 .001166  .001111  .001377  .001377

    The crosstalk-corrected amplifier image is given by SRC - VCTM * coeff.

*geomfile*
    String. Ascii formatted file containing geometric data for the IRAF
    task geotran which mosaics individual amplifiers into a single image::

        # SALTICAM CCD Geometry data
        # Translation and rotation of chip1 relative to chip2
        #
        # Date         gap   xshift(1)   yshift(1)   rot(1)
        2004-01-01   109    -54.5        0.0        0.0

*subover*
    Boolean. If 'yes', the level of charge in the overscan region of each
    image will be characterized using either row-dependent functions. The
    best-fit overscan level will then be subtracted from the image on a
    row-by-row basis. The overscan function is defined using the median,
    function, order, rej_lo, rej_hi and niter arguments. If subover is set
    to 'no' the the overscan is no subtracted from the image.

*trim*
    Boolean. If 'yes', the overscan and underscan regions will be removed
    from the output images. This procedure saves disk space and removes
    redundant data from the image. It is recommended to trim data before
    mosaicing amplifiers into a signle image.

*median*
        Boolean. If median='yes' the columns in the overscan region will be
        median averaged before fitting a single function to characterize the
        row-dependent structure of the bias. If median='no' the overscan
        columns will be mean-averaged before fitting the function.

*function*
        String. The functional form of the fit intended to characterize the
        the bias structure in the ovrscan region. The user has variety of
        function options to choose from::

            chebyshev  - Chebyshev polynomial
            polynomial - standard polynomial
            legendre   - Legendre polynomial
            spline1    - linear splines
            spline3    - cubic splines

        If the chebyshev, legendre of spline functions are called then
        saltbias will use the IRAF task colbias to subtract the overscan bias
        from science frames and trim the images.

*order*
        Integer. The order of the polynomial, or number of spline knots, in
        the overscan function defined above.

*rej_lo*
        Float. The overscan fit is an iterative sigma-clipping procedure
        employed to remove the biasing effects of data outliers. After the
        first fit iteration, any data below the threshold of rej_lo (in units
        of the sigma deviation between data and fit) will be rejected and the
        fit re-performed. The iterations will continue until no more data
        points are rejected or the number of iteration exceeds the limit
        defined by the niter argument.

*rej_hi*
        Float.  After the first fit iteration, any data above the threshold of
        rej_hi (in units of the sigma deviation between data and fit) will be
        rejected and the fit re-performed. The iterations will continue until
        no more data points are rejected or the number of iteration exceeds
        the limit defined by the niter argument.

*niter*
        String. The maximum number of iteration to perform during the sigma
        clipping procedure.

*masbias*
        Boolean. If masbias='yes', any bias files residing in the path rawpath
        will be processed and combined to create one or more master bias
        frame.

*subbias*
        Boolean. If subbias='yes' and an appropraie master bias exists, the master
        bias will be subtracted from science images as well as subtracting a
        bias level computed from the overscan region.

*(cleanup)*
        Hidden Boolean. If cleanup='yes', all intermediate files will be deleted
        at the end of the task. The default is cleanup='no'.

*(clobber)*
        Hidden boolean. If clobber='yes', files contained within the working
        directory will be overwritten by newly created files of the same
        name.

*logfile*
        String. Name of an ascii file for storing log and error messages
        written by the task. The file may be new, or messages can also be
        appended to a pre-existing file.

*(verbose)*
        Hidden Boolean. If verbose='no', log messages will be suppressed from
        both the terminal and the log file.  Error messages are excluded from
        this rule.

Description
===========

The standard chain of reduction for cleaning SALT science images is to
prepare files for reduction (task saltprepare), mutliply each
amplifier by a gain factor (saltgain), correct for amplifier cross
talk on each CCD (saltxtalk), sbtract the bias level from the images
and trim the underscan/overscan regions (saltbias) and mosaic the
amplifiers into a single image (pmosaic and smosaic). Full
descriptions of these tasks are available within this
package. saltclean calls each of the tasks listed above in turn in
order to perform a standard pipeline reduction. The task also
discriminates between images from different instruments, differing
on-chip binning, gain setting, readout speed and readout mode, in
order to apply appropriate calibrations and reduction. Slot mode data
is reduced as special case at the end of the saltclean chain using the
subtask saltslot.

saltclean cannot be run until a formatted observation has been created
by the task saltlog.

SALTICAM science images are split beween four readout amplifiers (two
nodes on each of two CCDs in a linear array).  RSS science images are
split beween six readout amplifiers (two nodes on each of three CCDs
in a linear array). Each anplifer is stored in a separate FITS image
extension of a file. Generally one file corresponds to one exposure,
except in the case of slot mode observing where multiple exposures are
stored in each file. Generic scalar information, e.g. telescope
pointing, time, telescope diagnostics are stored as keywords in the
primary extension of the file.  Amplifier-dependent information,
e.g. location on the detector plane, is stored as keywords in the
image extensions.

The observation log obslog is a formatted FITS table file which is
created by the task saltlog. It contains tabulated keyword records
from a list of raw image files. All raw image files must reside in a
single directory, referenced with the rawpath input argument. Data
from multiple nights or observing runs may be mixed. While files from
multiple instruments can be stored in the rawpath directory, only
files from a single instrument can be referenced within the
observation log file. Each instrument must have a separate observation
log. saltclean will reduce files from only one instrument in a single
call. If both RSS and SALTICAM data are to be reduced, two separate
calls to saltclean are required.

The saltprepare sub-task performs format consistency check on the raw
files and adds some keywords required for pipeline reduction. It
outputs new files with the prefix 'p'.

Gain correction factors are stored in an ascii file and given to
saltclean using the gaindb argument. They are employed in the saltgain
subtask. It is the user responsibility to ensure that the gain factor
file is suitable for all images files stored in the observation
log. The saltgain task will fail with an error message if the gain
file is incompatible.  saltgain is the only subtask which does not
create new data files.  It simply updates the files created by
saltprepare. Typically gain files will be named
/iraf/extern/salt/salticam/data/SALTICAMamps.dat or
/iraf/extern/salt/pfis/data/PFISamps.dat.

Cross talk correction ceofficents are stored in an ascii file and
given to saltclean using the xtalkfile argument. They are employed in
the saltxtalk subtask. It is the user responsibility to ensure that
the cross talk coefficent file is suitable for all images files stored
in the observation log. The saltxtalk task will fail with an error
message if the cross talk file is incompatible. Typically cross talk
files will be named /iraf/extern/salt/salticam/data/SALTICAMxtalk.dat
or /iraf/extern/salt/pfis/data/PFISxtalk.dat.

If mbias='yes' saltclean will employ task saltbias to create one or
more master bias frames. These frames are intended to characterize
residual structure in the bias distribution after overscan
subtraction. While there is often residual bias structure in the
images it is currently unclear how stable it is over time, so the
default is currently for master biases to be created in the pipeline
but not subtracted from science images.

saltclean filters through the obervation log and isolates all bias
frames.  Based on the contents of the INSTRUME, DETMODE, CCDTYPE,
CCDSUM, GAINSET and ROSPEED keywords, saltclean will create one or
more master bias frames using the functionality within the saltbias
subtask. Output master bias frames have names constructed to the
following rules: IYYYYMMDD{Mo}{NxN}{Gn}{Sp}.fits::

    I - the instrument, either S=SALTICAM, P=RSS
    YYYY - the year portion of the starting date of the night's observations
    MM - the month portion
    DD - the day portion
    Mo - the detector mode. It is not included if mode=full frame. Mo=FT if
    mode=frame transfer and Mo=Sl if mode=slot mode or videa mode.
    NxM - N is the integer pixel binning in the x direction, M the pixel
    binning in the y direction.
    Gn - The gain setting. Gn=Br if GAINSET=BRIGHT, or Gr=Fa if GAINSET=
    FAINT.
    Sp - The readout speed. Sp=Fa if ROSPEED=FAST, or Sp=Sl if ROSPEED=
    SLOW.

All science, bias, arc and flat field frames can be debiased using
polynomial fits to the y-structure in the overscan region of the
image, defined by the BIASSEC keyword. Use subover='y'.  The type of
function used in the fit and the order of the function are saltclean
arguments, where funtion=polynomial or chebyshev or legendre or
spline1 or spline3 and order>0. Sigma clipping is performed during the
fit. The saltclean user must choose upper and lower sigma thresholds
and a maximum number of iterations before stopping. Details can be
found in the saltbias help document. The user also has the choice of
averaging the overscan columns as a mean or median before fitting the
function. median='no' will invoke mean averaging and is the
default. The overscan and underscan regions will be removed from the
resulting images if trim='y'. This step is recommended. The underscan
region is not suitable for measuring the bias level.

As a final step, image files are mosaiced so that the individual
amplifiers are combined into a single image. The user must provide a
CCD geometry definition file to saltclean using the geomfile
argument. Mosacing is performed by one of the two IRAF tasks smosaic
or pmosaic. During the mosaicing RSS longslit science images are
interpolated across the chip gaps.  This facilitates source tracing
during spectral extraction. Typically, geometry files will be named
/iraf/extern/salt/salticam/data/SALTICAMgeom.dat or
/iraf/extern/salt/pfis/data/PFISgeom.dat.

Lastly, saltclean treats slot mode data as a special case. While slot
mode data can be reduced using all of the tasks (this statement
excludes mosaicing), a special task has been written to perform the
steps in a faster procedure. The one drawback is the loss of bias
level definition along the overscan columns, but this equates to a < 1
count deviation from the top of the slot to the bottom. saltclean
calls the subtask saltslot which performs the pipeline chain at speeds
faster than slot mode is taken, to ensure that the pipeline never
develops a backlog due to data capacity. All slot mode data contained
in the observation log are reduced separately at the end of the
sequence of tasks. Slot mode files are not mosaiced in the saltclean
procedure.

Output normal, and frame transfer mode files will have prefixes
'mbxp'. Output slot mode files will have prefixes 'bxp'.  Intermediate
files created during the saltclean procedure, e.g. with prefixes, 'p',
'xp', 'bxp' etc can be deleted from the working directory at the end
of the task by specifying cleanup='yes'. The default is cleanup='no'.

Examples
========


1. To reduce raw image files residing the directory /Volumes/data,
subtracting suitable master bias frames::

    --> saltclean rawpath='/Volumes/data' obslog='S20070816OBSLOG.fits'
    gaindb='/iraf/extern/salt/salticam/data/SALTICAMamps.dat'
    xtalkfile='/iraf/extern/salt/salticam/data/SALTICAMxtalk.dat'
    geomfile='/iraf/extern/salt/salticam/data/SALTICAMgeom.dat'
    subover='yes' trim='yes' median='no' function='polynomial'
    order=3 rej_lo=3.0 rej_hi=3.0 niter=10 masbias='yes'
    subbias='yes' logfile='salt.log' verbose='yes'

2. To reduce raw image files residing the directory /Volumes/data,
create master bias frames but do not subtract them from science
images, overwrite exisitng files and delete imtermediate files::

    --> saltclean rawpath='/Volumes/data' obslog='S20070816OBSLOG.fits'
    gaindb='/iraf/extern/salt/salticam/data/SALTICAMamps.dat'
    xtalkfile='/iraf/extern/salt/salticam/data/SALTICAMxtalk.dat'
    geomfile='/iraf/extern/salt/salticam/data/SALTICAMgeom.dat'
    subover='yes' trim='yes' median='no' function='polynomial'
    order=3 rej_lo=3.0 rej_hi=3.0 niter=10 masbias='yes'
    subbias='no' cleanup='yes' clobber='yes' logfile='salt.log'
    verbose='yes'

Time and disk requirements
==========================

Individual unbinned full frame RSS image files can be 112MB in
size. It is recommended to use workstations with a minimum of 512MB
RAM.  On a linux machine with 2.8 Ghz processor and 2 Gb of RAM, one
2051x2051 image in 0.31 sec.  Slot mode data can be processed up to 80 000
exposures per hour at that benchmark.

Bugs and limitations
====================

Currently no error propagation is performed through the
calculations. This can occur once the saltprepare tool writes bad
pixel and variance maps to raw data.

Functionality to flat field science frames is currently not included
in the processing chain. Flat fielding will not become appropriate
until the SALT payload is fully baffled.

The task currently assumes that no non-standard science windows are
used. this ambiguity may cause problems when subtracting master bias
frames and the mosaicing tools are untested on unusual science window
dimensions.

There is no current fucntionality for the removal of CCD fringe
structure, prevalant at the blue and red ends of SALT's bandpass.

There is no functionality to handle eligantly changes in calibration
data, such as those contained in gaindb and xtalkfile, over
time. Currently calibration files are good for one date only.

Send feedback and bug reports to salthelp@saao.ac.za

See also
========

 :ref:`saltpipe` :ref:`saltlog` :ref:`saltprepare` :ref:`saltgain` :ref:`saltxtalk` :ref:`saltbias` :ref:`saltslot`