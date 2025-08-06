ATS Short Course
================

This course will be offered September 8-10, 2025, in Knoxville, Tennessee and virtually.

Key Links
---------

* `About Flyer <https://amanzi.github.io/ats-short-course/ats-short-course-20250908/_static/ATSShortCourse2025_Flyer.pdf>`_
* `Registration Page <https://docs.google.com/forms/d/1o6q5dRvoMmXagI3u6DNl2KvkBVKgDggjmMkgnBc7DjE/edit>`_
* `Tentative Agenda <https://amanzi.github.io/ats-short-course/ats-short-course-20250908/_static/ATSShortCourse2025_Agenda.pdf>`_


Registration
------------

The registration deadline is August 1, 2025.  Foreign nationals in
particular are encouraged to register as soon as possible, to expedite
visitor agreements with ORNL.  **All attendees** must register, or
they will not be admitted either in person or virtually!  **All
attendees** must go through ORNL's visitor process, and will be
contacted by Angela Hagler to begin that process.

To register, go to the `Registration Page <https://docs.google.com/forms/d/1o6q5dRvoMmXagI3u6DNl2KvkBVKgDggjmMkgnBc7DjE/edit>`_

Logistics
---------

* Dates: September 8-10, 2025
* Location: 
   * Sept 8: `Oak Ridge National Laboratory <https://maps.app.goo.gl/PUBGAVXYvcoWroET7>`_ (optional day)  1 Bethel Valley Rd, Oak Ridge, TN, 37830
   * Sept 9-10: `UT Conference Center <https://maps.app.goo.gl/9TWneRtzBLpcdJQq6>`_ 600 Henley St, Knoxville, TN 37902
* Lodging: A `block of rooms <https://www.hilton.com/en/attend-my-event/tyschup-90q-3c9b35ed-6e0d-4a2f-9897-f280c4476737/>`_, at the government rate, is available at the Cumberland House in Knoxville.  Please reserve your room by August 8th to be included in the room block.
* Getting around: Uber and Lyft are available in the Knoxville area, but are not as reliable as in some areas.  Carpooling from the hotel to ORNL will be necessary, and will be arranged closer to the time.  Once you are at the hotel, the conference center is within easy walking distance (~0.25 miles).

Agenda
------

See the `tentative agenda <https://amanzi.github.io/ats-short-course/ats-short-course-20250908/_static/ATSShortCourse2025_Agenda.pdf>`_


Participants
============

To follow along with the demonstrations, participants will perform simulations and visualize results within Jupyter notebooks running under JupyterLab within a Docker container.  The container contains:

* A Linux-based operating system, including common command line tools.
* A build of Amanzi-ATS, with corresponding commonly-used environment variables, e.g. `$ATS_SRC_DIR` defined.
* All needed Third-Party Libraries and utilities (`h5dump`, `ncdump`, `meshconvert`, etc)
* A python3 build with all needed libraries for common ATS-based tasks.
* Watershed Workflow, a common ATS meshing workflow tool.

The short course demo files will reside on the participants' computers and any changes will be available after exiting the Docker container.

Quickstart
==========

1. Install external tools: `Docker <https://www.docker.com/get-started>`_, `VisIt <https://wci.llnl.gov/simulation/computer-codes/visit/executables>`_, and `git <https://github.com/git-guides/install-git>`_

2. Clone the ats-short-course demos repository

.. code: sh

   git clone -b ats-short-course-20250908 https://github.com/amanzi/ats-short-course; cd ats-short-course

3. Download the short course Docker image and run the container 

.. code: sh

   docker pull metsi/ats-short-course:latest
   docker run -it -v $(pwd):/home/ats_sc_user/short-course:delegated -w /home/ats_sc_user/short-course -p 8899:8899 metsi/ats-short-course:latest

4. Open the `Jupyter lab instance <http://127.0.0.1:8899/lab>`_
