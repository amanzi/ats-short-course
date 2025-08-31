Software Setup
==============

To follow along with the demonstrations, participants will perform simulations and visualize results within Jupyter notebooks running under JupyterLab within a Docker container.  All participants are expected to supply their own laptop; any relatively modern machine and operating system should be sufficient. There are two containers: one for ATS and one for Watershed Workflow.  **Please install these containers prior to joining the short course.**

.. contents::
   :local:
   :depth: 2

The ATS container contains:

* A Linux-based operating system, including common command line tools.
* A build of Amanzi-ATS, with commonly-used environment variables, e.g. `$ATS_SRC_DIR` defined.
* All needed Third-Party Libraries and utilities (e.g., `h5dump`, `ncdump`, `meshconvert`, etc.)
* A python3 build with all needed libraries for common ATS-based tasks (data introspection, visualization).

The Watershed workflow container contains:

* A Jupyter Lab environment.
* An installation of Watershed Workflow, including a supporting environment with all needed libraries.

In both cases, the short course demo files will reside on the participants' computers and any changes will be available after exiting the Docker container.

Note that these tools and this course material has been tested on Linux, Mac OSX, and, to a lesser extent, Windows systems. The expectation is that this short course should work on any of these systems, but there can always be challenges on individual systems, so please be patient. If you find bugs in the docker container or this material, please feel free to ask for help on the
`ATS user's group <mailto:ats-users@googlegroups.com>`_  or by submitting an Issue here.

.. |nbsp| unicode:: U+00A0 .. UNBREAKABLE SPACE 

1. Install external tools:
^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need **one from each** of the following categories:

* a container tool: one of Docker Desktop, Podman Desktop, or Rancher Desktop.  Docker Desktop is the original, but is not open source and may not be available to lab or large corporate institutional users.  Additionally, Docker Desktop may require "priveleged" or "root" access, while Podman does not.
* a 3D visualization tool: one of ParaView or VisIt.  VisIt is a little more intuitive to new users if you have never used either one and is sufficient for 90% of what we will do; ParaView is preferred for viewing complex 3D meshes.
* git
  

Docker
""""""

`Download Docker <https://www.docker.com/get-started>`_

.. admonition:: Windows

    Installation for Windows can be difficult since WSL 2 is required for the current version of Docker Desktop, so it is important to begin this process well before the short-course. If given the choice during installation, choose WSL 2 instead of Hyper-V.

    To manually update WSL 2:

    * Open a terminal or Powershell.
    * Update WSL ``wsl --update``
    * Install WSL ``wsl --install``  |nbsp| |nbsp| **Note: The process will take awhile and prompt you for an account creation**
    * Verify install using ``wsl --list``. You should see something like "Ubuntu".
    * Set default WSL ``wsl --set-default-version 2``

.. admonition:: OSX

    Download and install the .dmg file for your silicon type, whether Intel (older) or Apple (M1 and newer).

.. admonition:: Linux

    Docker provides instructions for adding DEB package repositories, then installing through apt-get for Ubuntu, Debian, and related distributions.  They also provide RPMs for RHEL8 & 9 and Fedora, and pacman for Arch.

.. seealso::

    * `WSL Installation <https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package>`_
    * `WSL Troublshooting Guide <https://learn.microsoft.com/en-us/windows/wsl/troubleshooting#installation-issues>`_


Podman
"""""""

`Download Podman <https://podman-desktop.io/>`_

.. admonition:: Windows

    Installation for Windows can be difficult since WSL 2 is required for the current version of Podman, so it is important to begin this process well before the short-course. If given the choice during installation, choose WSL 2 instead of Hyper-V.

    To manually update WSL 2:

    * Open a terminal or Powershell.
    * Update WSL ``wsl --update``
    * Install WSL ``wsl --install``  |nbsp| |nbsp| **Note: The process will take awhile and prompt you for an account creation**
    * Verify install using ``wsl --list``. You should see something like "Ubuntu".
    * Set default WSL ``wsl --set-default-version 2``

    Once installed, you will need to set up Podman and restart the application.

.. admonition:: OSX

    Download and install the "universal *.dmg" file.  Alternatively, `brew install --cask podman-desktop` if you use homebrew.

.. admonition:: Linux

    Podman Desktop is distributed via a flatpak, which does not require sudo access, but installing flatpak itself usually does.  `apt-get install flatpak` or similar will get flatpak, then either download the flatpak or add the flathub repo and install directly.
                
.. seealso::

    * `WSL for Podman Guide <https://podman-desktop.io/docs/installation/windows-install>`_
    * `WSL Installation <https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package>`_
    * `WSL Troublshooting Guide <https://learn.microsoft.com/en-us/windows/wsl/troubleshooting#installation-issues>`_

ParaView
""""""""

`Download Paraview <https://www.paraview.org/download/>`_  Paraview versions <INSERT VERSIONS HERE> will visualize our most complex meshes; other versions may crash on 3D, stream aligned watershed meshes.  Any version will work for most of the course.

Visit
"""""

`Download Visit <https://wci.llnl.gov/simulation/computer-codes/visit/executables>`_  VisIt does not visualize exo meshes correctly, and does not correctly deal with 3D, stream aligned meshes.  But it is simpler to get started with, and will work fine for most of the course.

Git
"""

* **Mac OSX**: git is included in the *command line tools*, installed via ``xcode-select --install``, or in XCode itself.
* **Linux**: git is included as a standard package under most package managers, e.g. ``sudo apt-get install git``.
* **Windows**: See `Git Downloads <https://github.com/git-guides/install-git>`_. Note that the GitHub Desktop is also an option for Windows users and provides a GUI.


2. Clone the ats-short-course demos repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Jupyter notebooks, as well as the corresponding input files and data, are provided in this git repository. To get started you need to clone this repository:

.. code-block:: sh

   git clone -b ats-short-course-20250908 https://github.com/amanzi/ats-short-course
   cd ats-short-course
  
3. Download the ATS Docker image and run the container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first container to be used is the container used for running ATS.  It is quite large; please download this prior to arriving at the short course.

.. code-block:: sh

   docker pull metsi/ats-short-course:2025-ats-latest


The next step is to run the container.  The container can either be used to launch Jupyter Lab -- most of the course will be run this way.  Occassionally it may be useful to directly access a terminal inside the container.


OSX or Linux
""""""""""""

To launch the Jupyter Lab container, mounting the current directory (which should be the ats-short-course repository you just cloned):

.. code-block:: sh

   docker run -it --init --mount type=bind,source=$(pwd),target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest


To launch a terminal:

.. code-block:: sh

   docker run -it --init --mount type=bind,source=$(pwd),target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest /bin/bash

Windows 10
""""""""""

If you are using Windows 10's Command Prompt or PowerShell, where the variable ``$(pwd)`` is not recognized, it may be easier to type the location of ats-short-course explicitly.  
For example, if ``C:\Users\USERNAME\ats-short-course`` is the top-level of the ``ats-short-course`` repository, then:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\Users\USERNAME\ats-short-course,target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest

If you are getting a Docker error that **the working directory is not valid** and you don't recognize the directory Docker returns, it is possible you are using (or installed as part of packages like Git for Windows) a command line interface that changes the paths you are passing to Docker.  

If so, try double slashes in your Docker command:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\\Users\\USERNAME\\ats-short-course,target=//home//ats_sc_user//work -w //home//ats_sc_user//work -p 8888:8888 metsi/ats-short-course:2025-ats-latest


Similarly, append `/bin/bash` to the end of the line to get a terminal inside the container.

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\Users\USERNAME\ats-short-course,target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest /bin/bash


3. Download the Watershed Workflow Docker image and run the container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Watershed Workflow container works in nearly an identical way.

.. code-block:: sh

   docker pull ecoon/watershed_workflow-ats:v2.0


The next step is to run the container.  Again, we will mount the local directory, and run jupyter lab.

OSX or Linux
""""""""""""

To launch the Jupyter Lab container, mounting the current directory (which should be the ats-short-course repository you just cloned):

.. code-block:: sh

   docker run -it --init --mount type=bind,source=$(pwd),target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 ecoon/watershed_workflow-ats:v2.0

Windows 10
""""""""""

If you are using Windows 10's Command Prompt or PowerShell, where the variable ``$(pwd)`` is not recognized, it may be easier to type the location of ats-short-course explicitly.  
For example, if ``C:\Users\USERNAME\ats-short-course`` is the top-level of the ``ats-short-course`` repository, then:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\Users\USERNAME\ats-short-course,target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 ecoon/watershed_watershed-ats:v2.0

If you are getting a Docker error that **the working directory is not valid** and you don't recognize the directory Docker returns, it is possible you are using (or installed as part of packages like Git for Windows) a command line interface that changes the paths you are passing to Docker.  

If so, try double slashes in your Docker command:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\\Users\\USERNAME\\ats-short-course,target=//home//joyvan//workdir -w //home//joyvan//workdir -p 9999:9999 ecoon/watershed_workflow-ats:v2.0



4. Connect to Jupyter
^^^^^^^^^^^^^^^^^^^^^

Follow the instructions on the screen, but if you launched Jupyter Lab, you should now be able to open a link in your browser pointed to the Jupyter Lab.  The link should be:

* http://127.0.0.1:8888/lab for the ATS container
* http://127.0.0.1:9999/lab for the Watershed Workflow container.

You should see JupyterLab and the files from this repository.


.. note::

   If the browser complains about tokens and refuses to connect, it may be because you have a local, non-container Jupyter lab instance running.  Please shut that down, then try again.

    
.. note::

   Some users see the message:

   .. code-block::

      No web browser found: could not locate runnable browser.

   This message is safe to ignore -- by manually copying and pasting the above address into your browser, you should see the Jupyter Lab instance.


5. Getting Help
^^^^^^^^^^^^^^^

If you have trouble with this at any point, please either:

* email the ATS users group at ats-users@googlegroups.com
* post an `issue <https://github.com/amanzi/ats-short-course/issues/>`_
  
  
