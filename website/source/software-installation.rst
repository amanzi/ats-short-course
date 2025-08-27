Step-by-Step Software Installation and Use
==========================================

Installing the Required Software
---------------------------------

As a first step you need to install the following tools on your system

Docker
^^^^^^

.. |nbsp| unicode:: U+00A0 .. UNBREAKABLE SPACE 

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


PodMan
^^^^^^

`Download Podman <https://podman.io/>`_ 

ParaView
^^^^^^^^

`Download Paraview <https://www.paraview.org/download/>`_

Visit
^^^^^

`Download Visit <https://wci.llnl.gov/simulation/computer-codes/visit/executables>`_

git (so you can clone this repo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Mac OSX**: git is included in the *command line tools*, installed via ``xcode-select --install``, or in XCode itself.
* **Linux**: git is included as a standard package under most package managers, e.g. ``sudo apt-get install git``.
* **Windows**: See `Git Downloads <https://github.com/git-guides/install-git>`_. Note that the GitHub Desktop is also an option for Windows users and provides a GUI.



