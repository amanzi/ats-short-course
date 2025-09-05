Software Setup
==============

To follow along with the demonstrations, participants will perform simulations and visualize results within Jupyter notebooks running under JupyterLab within a Docker container.  All participants are expected to supply their own laptop; any relatively modern machine and operating system should be sufficient. There are two containers: one for ATS and one for Watershed Workflow.  **Please install these containers prior to joining the short course.**

.. contents::
   :local:
   :depth: 3

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
--------------------------

You will need **one from each** of the following categories:

* a container tool: one of Docker Desktop, Podman Desktop, or Rancher Desktop.  Docker Desktop is the original, but is not open source and may not be available to lab or large corporate institutional users.  Additionally, Docker Desktop may require "priveleged" or "root" access, while Podman does not. Podman provides the same API as Docker, thus the command lines given below to pull and run the container should work by replacing ``docker`` for ``podman``. 
* a 3D visualization tool: one of ParaView or VisIt.  VisIt is a little more intuitive to new users if you have never used either one and is sufficient for 90% of what we will do; ParaView is preferred for viewing complex 3D meshes.
* git
  

Docker
^^^^^^

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
^^^^^^

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

    Download and install the "universal \*.dmg" file.  Alternatively, `brew install --cask podman-desktop` if you use homebrew.

.. admonition:: Linux

    Podman Desktop is distributed via a flatpak, which does not require sudo access, but installing flatpak itself usually does.  `apt-get install flatpak` or similar will get flatpak, then either download the flatpak or add the flathub repo and install directly.
                
.. seealso::

    * `WSL for Podman Guide <https://podman-desktop.io/docs/installation/windows-install>`_
    * `WSL Installation <https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package>`_
    * `WSL Troublshooting Guide <https://learn.microsoft.com/en-us/windows/wsl/troubleshooting#installation-issues>`_

ParaView
^^^^^^^^

`Download Paraview <https://www.paraview.org/download/>`_  Paraview will visualize our most complex meshes.

Visit
^^^^^

`Download Visit <https://wci.llnl.gov/simulation/computer-codes/visit/executables>`_  VisIt does not correctly deal with 3D, stream aligned meshes.  But it is simpler to get started with, and will work fine for most of the course.

Git
^^^

* **Mac OSX**: git is included in the *command line tools*, installed via ``xcode-select --install``, or in XCode itself.
* **Linux**: git is included as a standard package under most package managers, e.g. ``sudo apt-get install git``.
* **Windows**: See `Git Downloads <https://github.com/git-guides/install-git>`_. Note that the GitHub Desktop is also an option for Windows users and provides a GUI.


2. Clone the ats-short-course repository
----------------------------------------

The Jupyter notebooks, as well as the corresponding input files and data, are provided in this git repository. To get started you need to clone this repository:

.. code-block:: sh
                
   git clone -b ats-short-course-20250908 https://github.com/amanzi/ats-short-course

which will create a subdirectory called ``ats-short-course``.  Now change into this directory
   
.. code-block:: sh
                
   cd ats-short-course
  

3. Working with the ATS
-----------------------

.. note:: If you are using Podman instead of docker, replace ``docker`` with ``podman`` in the commands that follow. 

Download the ATS Docker Image and run it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first container to be used is for running the ATS. The image for this container is quite large; please download this prior to arriving at the short course. Copy-and-paste the ``docker pull`` command shown below to download the ATS image:


.. code-block:: sh
                
   docker pull metsi/ats-short-course:2025-ats-latest

If this downloads successfully then run the ats in this container to check the version

.. code-block:: sh
                
   docker run -it --rm metsi/ats-short-course:2025-ats-latest ats --version

You should see the following output 
   
.. code-block:: console
                
   ATS version 1.6.0_8d11cb0c

The next step is running the container to launch Jupyter Lab -- most of the course will be run this way.

.. note:: Occassionally it may be useful to directly run ats in the container as we did here, or to access a terminal inside the container. See the :doc:`troubleshooting` page for tips on these options. 

Run JupyterLab in the ATS Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal is to enable JupyterLab to interact with the ats-short-course repository files on your local system. This is accomplished through the --mount option which shares your present working directory ($pwd) with the Docker container.

So make sure your $pwd is the top-level of the ats-short-course repository and copy-and-paste one of the following commands:


OSX or Linux
""""""""""""

To launch the Jupyter Lab container, mounting the current directory (which should be the ats-short-course repository you just cloned):

.. code-block:: sh

   docker run -it --init --mount type=bind,source=$(pwd),target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest

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

An alternative to providing the path explicitly, you can try the Windows equivalent to ``$(pwd)`` in the Command Prompt ``%cd:\=/%``

.. code-block:: sh

    docker run -it --init --mount type=bind,source=%cd:\=/%,target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest

or if you are using the Windowns PowerShell simply use ``$PWD``

.. code-block:: sh

    docker run -it --init --mount type=bind,source=$PWD,target=/home/ats_sc_user/work -w /home/ats_sc_user/work -p 8888:8888 metsi/ats-short-course:2025-ats-latest


Connect to the ATS JupyterLab Session from your local Web Browser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Independent of the OS you’re using, the Docker run command described above will output several status messages to the screen, one of which is about the Jupyter server that it started.

.. code-block:: console
                
   ...                
   [I 2025-09-04 04:43:47.167 ServerApp] Jupyter Server 2.17.0 is running at:
   [I 2025-09-04 04:43:47.167 ServerApp] http://ee87e000539c:8888/lab
   [I 2025-09-04 04:43:47.167 ServerApp]     http://127.0.0.1:8888/lab
   [I 2025-09-04 04:43:47.167 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
   ...
                
Just cut-and-paste the link shown, or click http://127.0.0.1:8888/lab.

.. note::

   If the browser complains about tokens and/or refuses to connect, it may be because you have a local, non-container Jupyter lab instance running.  Please shut that down, then try again.

   
4. Working with Watershed Workflow
---------------------------------

Download the Watershed Workflow Docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Watershed Workflow container works in nearly an identical way.  Download the Watershed WorkFlow image, 

.. code-block:: sh

   docker pull ecoon/watershed_workflow-ats:v2.0

Run JupyterLab in the Watershed Workflow Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
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

    docker run -it --init --mount type=bind,source=C:\Users\USERNAME\ats-short-course,target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 ecoon/watershed_workflow-ats:v2.0

If you are getting a Docker error that **the working directory is not valid** and you don't recognize the directory Docker returns, it is possible you are using (or installed as part of packages like Git for Windows) a command line interface that changes the paths you are passing to Docker.  

If so, try double slashes in your Docker command:

.. code-block:: sh

    docker run -it --init --mount type=bind,source=C:\\Users\\USERNAME\\ats-short-course,target=//home//joyvan//workdir -w //home//joyvan//workdir -p 9999:9999 ecoon/watershed_workflow-ats:v2.0

An alternative to providing the path explicitly, you can try the Windows equivalent to ``$(pwd)`` in the Command Prompt ``%cd:\=/%``
    
.. code-block:: sh

    docker run -it --init --mount type=bind,source=%cd:\=/%,target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 ecoon/watershed_workflow-ats:v2.0

or if you are using the Windowns PowerShell simply use ``$PWD``

.. code-block:: sh

    docker run -it --init --mount type=bind,source=$PWD,target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 ecoon/watershed_workflow-ats:v2.0

Connect to the Watershed Workflow JupyterLab Session from your local Web Browser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Independent of the OS you’re using, the Docker run command described above will output several status messages to the screen, one of which is about the Jupyter server that it started.

.. code-block:: console
                
   ...
   [I 2025-09-04 16:17:14.300 ServerApp] Jupyter Server 2.17.0 is running at:
   [I 2025-09-04 16:17:14.300 ServerApp] http://localhost:9999/lab
   [I 2025-09-04 16:17:14.300 ServerApp]     http://127.0.0.1:9999/lab
   [I 2025-09-04 16:17:14.300 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
   [C 2025-09-04 16:17:14.301 ServerApp]

Now, simply copy-and-paste the link shown into your local web browser, or click http://127.0.0.1:9999/lab.
   
.. note:: We have deliberately assigned the default port to 9999 for Watershed Workflow so that it won't conflict with the ATS session you have running over port 8888.  

Confirm the Watershed Workflow container is working
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From the jupyter lab instance you just started, open and run the notebook `00_intro/test_ww.ipynb`.  If this successfully completes, this container is successfully installed.
    

5. Getting Help
---------------

If you have trouble with this at any point, please:

* Check the :doc:`troubleshooting` page to see if your issue has been addressed.
* Email the ATS users group at ats-users@googlegroups.com OR
* Post an `issue <https://github.com/amanzi/ats-short-course/issues/>`_
  
  
