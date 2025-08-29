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

To follow along with the demonstrations, participants will perform simulations and visualize results within Jupyter notebooks running under JupyterLab within a Docker container.  There is a separate container for day 1 on the ATS day 2 for Watershed Workflow.  The ATS container contains:

* A Linux-based operating system, including common command line tools.
* A build of Amanzi-ATS, with commonly-used environment variables, e.g. `$ATS_SRC_DIR` defined.
* All needed Third-Party Libraries and utilities (e.g., `h5dump`, `ncdump`, `meshconvert`, etc.)
* A python3 build with all needed libraries for common ATS-based tasks.

The Watershed workflow container contains:

* A Linux-based operating system, including common command line tools.
* An installation of Watershed Workflow, with commonly-used environment variables, e.g. `$ATS_SRC_DIR` defined.
* All needed Third-Party Libraries and utilities (Exodus, `h5dump`, `ncdump`, etc.)
* A python3 build with all needed libraries for common Watershed Workflow tasks.

In both cases, the short course demo files will reside on the participants' computers and any changes will be available after exiting the Docker container.

Note that these tools and this course material has been tested on Linux, Mac OSX, and, to a lesser extent, Windows systems. The expectation is that this short course should work on any of these systems, but there can always be challenges on individual systems, so please be patient. If you find bugs in the docker container or this material, please feel free to ask for help on the
`ATS user's group <mailto:ats-users@googlegroups.com>`_  or by submitting an Issue here.

.. |nbsp| unicode:: U+00A0 .. UNBREAKABLE SPACE 

Quickstart
----------

1. Install external tools:
^^^^^^^^^^^^^^^^^^^^^^^^^^
    
Docker (or Podman)
""""""""""""""""""

`Download Docker <https://www.docker.com/get-started>`_

.. admonition:: Windows

    Installation for Windows can be difficult since WSL 2 is required for the current version of Docker Desktop, so it is important to begin this process well before the short-course.

To manually update WSL 2:

* Open a terminal or Powershell.
* Update WSL ``wsl --update``
* Install WSL ``wsl --install``  |nbsp| |nbsp| **Note: The process will take awhile and prompt you for an account creation**
* Verify install using ``wsl --list``. You should see something like "Ubuntu".
* Set default WSL ``wsl --set-default-version 2``

.. seealso::

    * `WSL Installation <https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package>`_
    * `WSL Troublshooting Guide <https://learn.microsoft.com/en-us/windows/wsl/troubleshooting#installation-issues>`_


Podman (or Docker)
""""""""""""""""""

`Download Podman <https://podman-desktop.io/>`_

ParaView
""""""""

`Download Paraview <https://www.paraview.org/download/>`_

Visit
"""""

`Download Visit <https://wci.llnl.gov/simulation/computer-codes/visit/executables>`_

Git
"""

* **Mac OSX**: git is included in the *command line tools*, installed via ``xcode-select --install``, or in XCode itself.
* **Linux**: git is included as a standard package under most package managers, e.g. ``sudo apt-get install git``.
* **Windows**: See `Git Downloads <https://github.com/git-guides/install-git>`_. Note that the GitHub Desktop is also an option for Windows users and provides a GUI.


2. Clone the ats-short-course demos repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   git clone -b ats-short-course-20250908 https://github.com/amanzi/ats-short-course && cd ats-short-course
  
3. Download the short course Docker image and run the container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   docker pull metsi/ats-short-course:2025-ats-latest
   docker run -it --init --mount type=bind,source=$(pwd),target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest
  
4. Open the `Jupyter lab instance <http://127.0.0.1:8888/lab>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Getting the Short Course Files
------------------------------

The Jupyter notebooks, as well as the corresponding input files and data, are provided in this git repository. To get started you need to clone this repository:

.. code-block:: sh

    #
    # Select a local directory (here we assume starting at the top-level of your home directory)
    #
    cd ~/
    git clone -b ats-short-course-20250908 https://github.com/amanzi/ats-short-course

After cloning, change to the repository directory:

.. code-block:: sh

    cd ats-short-course


Download and run the ATS in a Container
---------------------------------------

The Docker container for this short-course includes installations of Watershed Workflow, TINerator, amanzi, and ats.  
As a result it is fairly large and best to separate the initial download and testing before we run JupyterLab.  

To get started, let's download the container:

.. code-block:: sh

    docker pull metsi/ats-short-course:2025-ats-latest

If this downloads successfully, check the version of ATS:

.. code-block:: shell

    docker run -it --rm metsi/ats-short-course:2025-ats-latest ats --version
    > ATS version 1.6.0_8d11cb0c

If this worked – great! Move on to :ref:`Run JupyterLab under Docker <run-jupyterlab>`.  
But if you ran into trouble with the download and/or Docker storage on your system, check some of the 
`troubleshooting tips <DockerTips.md>`_.


.. _run-jupyterlab:

Run Jupyer Lab in a Container
-----------------------------

The goal is for you to enable JupyterLab to interact with the ats-short-course repository files on your local system.  
This is accomplished through the ``--mount`` option which shares your *present working directory* (``$pwd``) with the Docker container.  

So make sure your ``$pwd`` is the top-level of the ``ats-short-course`` repository and cut-and-paste one of the following commands:

OSX
^^^

.. code-block:: sh

    docker run -it --init --mount type=bind,source=$(pwd),target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest

OR if you prefer the verbose version:

.. code-block:: sh

    docker run \
        --interactive \
        --init \
        --mount \
        type=bind,source=$(pwd),target=/home/ats_sc_user/work \
        --publish 8888:8888 \
        --workdir /home/ats_sc_user/work \
        metsi/ats-short-course:2025-ats-latest


Windows 10
^^^^^^^^^^

If you are using Windows 10's Command Prompt or PowerShell, where the variable ``$(pwd)`` is not recognized, it may be easier to type the location of ats-short-course explicitly.  
For example, if ``C:\Users\USERNAME\ats-short-course`` is the top-level of the ``ats-short-course`` repository, then:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\Users\USERNAME\ats-short-course,target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest

If you are getting a Docker error that **the working directory is not valid** and you don't recognize the directory Docker returns, it is possible you are using (or installed as part of packages like Git for Windows) a command line interface that changes the paths you are passing to Docker.  

If so, try double slashes in your Docker command:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\\Users\\USERNAME\\ats-short-course,target=//home//ats_sc_user//work -w //home//ats_sc_user//work -p 8888:8888 metsi/ats-short-course:2025-ats-latest


Connect to the Jupyer Lab Session from your local web browser
-------------------------------------------------------------

Independent of the OS you're using, the Docker run command described above will output several status messages to the screen, one of which is about the Jupyter server that it started.  

For example, you should see something like:

.. code-block:: sh

    [I 2021-08-17 21:59:38.111 ServerApp] Jupyter Server 1.10.2 is running at:
    # This address is unique to each system, so don't copy this one in your case
    [I 2021-08-17 21:59:38.111 ServerApp] http://58557662c177:8899/lab
    # This address is generic and will work on any system where this port on local host has not been allocated to another process
    [I 2021-08-17 21:59:38.111 ServerApp]  or http://127.0.0.1:8899/lab
    # To kill this server
    [I 2021-08-17 21:59:38.111 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

Once this is running you can open this URL in your browser:  
``http://127.0.0.1:8899/lab``  

You should see JupyterLab and the files from this repository.  

.. note::

   Most users see the message:

   .. code-block::

      No web browser found: could not locate runnable browser.

   This message is safe to ignore -- by manually copying and pasting the above address into your browser, you should see the Jupyter Lab instance.




