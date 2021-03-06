.. _slotutcfix:

**********
slotutcfix
**********


Name
====

slotutcfix -- Correct UTC times in slotmode data headers

Usage
=====

slotutcfix images update (outfile) (ampperccd) (ignorexp)
(droplimit) (inter) (plotdata) (logfile) (verbose) (debug)

Parameters
==========


*images*
    String. List of images to reduce. Data can be provided as a comma-delineated
    list, or a string with a wildcard (e.g. 'images=S20061210*.fits'), or
    a foreign file containing an ascii list of image filenames. For ascii
    list option, the filename containing the list must be provided
    preceded by a '@' character, e.g. 'images=@listoffiles.lis'. Note
    that SLOT mode fits files often contain more than one exposed frame.

*update*
    Boolean.  If yes, automatically updates the image headers for the
    appropriate dwell time.  If no, it will calculate the dwell time, but
    not update the headers.

*oufile*
    String. If outfile contains a falue, then an output ascii file will be
    created with the updated times for each of the frames.

*ampperccd*
    Int. The number of amplifiers per CCD.  If it is the newfits file and
    has already been processed by slotphot, then set to zero.

*ignorexp*
    Integer >= 0. If ignorexp > 0 the first ignorexp frames will be skipped
    over before extraction is performed on ignorexp + 1 and all subsequent
    frames. This functionality is useful for SLOT mode data because the
    first few frames are generally empty. This is simply because SLOT
    mode involves continuous readout. The exposed area of the chip is some
    way from the readout boundary, so the first few frames of a sequence
    will contain CCD bias only.

*droplimit*
    Integer >= 0. The maximum number of frames that can be dropped between
    exposures.

*inter*
    Boolean.  Ask for user input prior to updating the header data.

*plotdata*
    Boolean.  Plot the distribution of fits as a function of dwell times.

*logfile*
    String. Name of an ascii file for storing log and error messages
    from the tool. The file may be new, or messages can also be appended to a
    pre-existing file.

*verbose*
    Boolean. If verbose=n, log messages will be suppressed.

*debug*
    Boolean. If debug=y, will give more debug information if an error occurs (use this option to gather information when reporting a bug).

Description
===========


SLOTUTCFIX corrects the UTC values in the slotmode imaging data.  The
SCAM software was producing incorrect UTC values for three reasons:
(1) An additional 47 ms dwell time in the original DSP software, (2)
The computer losing time during readout, and (3) the number of frames
between observation and readout was assumed to be 6, when for
practically purposes, it is 8 frames.  All three issues have been
corrected in versions of SCAM software at SCAM-7.08 and above.
Earlier version prior to SCAM-4.42 unfortunately maintain a slightly
different header structure and cannot be corrected for these issues
although they are present.  SLOTUTCFIX is supplied to provide a fix
for SCAM software between versions SCAM-4.42 and SCAM-4.78.

To calculate the correct times for the images, two aspects of the SCAM
readout were verified in the lab.  All exposures have the same dwell
time (dead time plus exposure time) and the exposure closest to the
turn of the second can be considered a fiducial time.  The latter is
due to an independent pulse feed to SCAM to update the timing once a
second.


With these two assumptions, we can calculate the correct dwell time by
minimizing the following equation:

Y(t_dwell) =sum [ abs( (dt_i/t_dwell)-int(dt_i/t_dwell))]

In this equation, dt_i is the difference between the UTC time of
exposure i and the firt post-second exposure.  It is assumed that
there should be an integer number of frames between the first
post-second exposure and all other post-second exopures.  The value of
t_dwell that minimizes the equation will be calculated and can be used
to update the UTC value in the image headers.  Alternatively,
SLOTUTCFIX can be run manual and the user can enter in their desired
value for t_dwell.

Once the correct dwell time has been calculated, a new UTC is
calculated for every exposure.  The first exposure after the turn of a
second is assumed to be a fiducial exposure. Then the UTC is
calculated by multiplying the dwell time by the number of observed and
dropped frames between a given exposure and this fiducial one.
Exposures are dropped when data that has been readout has not been
recorded when another exposure has finished reading out.

The final correction is to correct for the wrong number of exposures
assumed to have been readout.  The correct time is found by taking the
UTC from the exposure 6 recorded exposures ahead and then correcting
that time by 8 times the dwell time.  Frames at the end of the run may
not have the correct exposure time as it is difficult to determine if
any frames may have been dropped, so the last 8 exposures of any track
should be ignored.

If the data are updated, UTC-OBS and TIME-OBS will be both replaced
with the correct time.  Two additional keywords will also be added:
DWETIME is the total exposure plus dead time for each image, and DUTC
is the change in UTC-OBS in seconds.

When running the task, the user has several options.  If update is
selected, the UTC values in the headers will be corrected along with
the addition of keywords with information on the change in UTC and the
dwell time.  If plotdata is selected, the relationship between the fit
and the range in t_dwell will be plotted for the user to examine.
inter allows the user to interactively approve the value of t_dwell or
enter in a value of their choice.

When running the task, the user should take care to only run it on
data from the same set of SCAM observations.  If a subset of
observations from a track has been restarted, then the program should
be run separately on each group of observations.

From investigation of a number of observations, it has generally been
found that the dwell time is given by the exposure time (or the
minimum exposure time for that binning) plus 47 milliseconds.  In the
end, the relative accuracy of the timing is, at best, approximately
0.01 seconds.

A fix to the SCAM software for this problem will be installed at some
point.  At that time, this software will no longer be needed.


Examples
========

1. To automatically correct the UTC values in the image``::

    --> slotutcfix images="*.fits" update=y outfile='out'
    amperccd=2 ignorexp=0 plotdat=y inter=y droplimit=100
    logfile=salt.log verbose=y

Time requirements
=================

A linux machine with 2 GB of RAM and a 2.8 Ghz processer was able to
process 12 SALTICAM slotmode exposures with 200 extensions in 16 seconds.

Bugs and limitations
====================

The current version of SLOTUTCFIX does not check for the SCAM software version
being used.

Send feedback and bug reports to salthelp@saao.ac.za

See also
========

 :ref:`saltslot` :ref:`slotview`