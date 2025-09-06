Troubleshooting
===============

The external software can be challenging to install and containers can be a tricky to run.  Here we are some common problems and their fixes. 

Watershed Workflow
------------------

SSL Certificates
^^^^^^^^^^^^^^^^

If your computer is operated by an institution (e.g. ORNL), you may
find errors about self-signed certificates when running the
test_ww.ipynb notebook.  You will have to install the certificate file
used by your institution.  If you have a Mac, you can export the
certificates, then point the SSL in the container to this certificates
file through environment variables:

.. code-block:: sh

   cd /path/to/your/ats-short-course
   security find-certificate -a -p /Library/Keychains/System.keychain > system-certs.pem
   docker run -it --init --mount type=bind,source=$(pwd),target=/home/joyvan/workdir -w /home/joyvan/workdir -p 9999:9999 -e SSL_CERT_FILE=/home/joyvan/workdir/system-certs.pem -e REQUESTS_CA_BUNDLE=/home/joyvan/workdir/system-certs.pem ecoon/watershed_workflow-ats:v2.0


Docker Tips
-----------

.. admonition:: Key Terminology

  As with any technology there is some jargon that we need to keep
  straight otherwise things that are relatively simple will seem very
  confusing.  First, it is important to define the terms **image** and
  **container**:
  
  - **Image** : A docker image is a static file that includes everything
    that is needed to run an application in a docker container, such
    as, code, libraries, environment variables, etc.  Note images are
    what we build and share with you through docker hub, such as the
    metsi/ats-short-course:2025-ats-latest image you pulled down to
    your system.
    
  - **Container** : A docker container is a runtime instance of a docker
    image.  So when you run jupyterlab it is running in a container
    that is an instance of the docker image
    metsi/ats-short-course:2025-ats-latest.  So you could have many
    containers started from the same image, and you can run multiple
    shells within a container.

    
Examples we are adding here:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Docker (or PodMan) Desktop GUIs make it easy to find some of this information, but eventually you will likely end up on the command line again, particularly for some of the ``run`` and ``exec`` commands.  In addition, seeing it on the command line will help promote a clearer understanding of what is happening under the hood.  So here we focus on the command line, 

* What images do I have downloaded?

  Much like listing files in a unix shell we'll use ``ls``

  .. code-block:: sh

     docker image ls 
 
* What containers do I have running?

  Same as above but note the ``ls`` is an option to the ``container`` command
  
  .. code-block:: sh

     docker container ls 
   
* What containers do I have on my system (running and stopped)?

  .. note:: If we include the ``--rm`` option when we run an image the resulting container will be removed when is finishes execuation (i.e., is stopped).  However, without this option the stopped container is saved for possible use in the future (i.e., it can be restarted).  That's great except that a lot of stopped containers may build up on our system without us realizing it, potentially consuming quite a bit of space.  To check the ``-a`` option is handy.

  .. code-block:: sh

    docker container ls -a 
  
  You can remove unwanted stopped containers one at a time (or select and manage them in the GUI).  But if you want to remove all of the stopped containers you can use `prune`. 

  .. code-block:: sh
   
    docker container prune

* How do I get a bash shell when you first create the container?

  When you run an image to create the container if will execute the default command that we set when the image was built.  For the two containers we are using here the default command runs Juyter Lab.  However, you can override this and run execute you would like. For example, in the setup instructions we ran  ``ats --version`` to get check the version of ATS we had downloaded.  Similarly you could run a bash shell,

  .. code-block:: sh

     docker run -it --rm metsi/ats-short-course:2025-ats-latest /bin/bash

  where there options specify

  * **-it** which gives an *interactive* session with a *tty* (terminal) device. 
  * **--rm** indicates that docker can remove the container when you exit the bash shell

  giving a prompt that looks like
  
  .. code-block:: console

     (base) ats_sc_user@3d3b2698214a:~/amanzi

  Here the prompt shows

  *  **(base)** - the active conda environment
  *  **ats_sc_user** - your username
  *  **3d3b2698214a** - the container ID (which is also the hostname)
  
  .. note:: This particular container has not mounted any of the host directories, or mapped any ports, as we do when we run it for the lessons.  However, if you wanted those things you could cut-and-paste the command from the installation instructions and append /bin/bash on the end. 
            
* What do all the extra options to ``docker run`` that we used in the installation instructions do?

  Here's the command we use for the short course:

  .. code-block:: sh

     docker run -it \
       --init  \
       --mount type=bind,source=$(pwd),target=/home/ats_sc_user/work \
       -w /home/ats_sc_user/work \
       -p 8888:8888 \
       metsi/ats-short-course:2025-ats-latest                  

  Each option really does have a purpose:

  * **-it** as noted above give us an interactive session
  * **--mount** connects a directory on the container system with a directory on your laptop (the host system)
    
    * source=$(pwd)  - sets the host file system directory to your present working directory
    * target=/home/ats_sc_user/work  -sets the container directory to the ``work`` subdirectory of our ats_sc_user
      
  * **-w** -sets the current working directory for the jupyter session
  * **-p 8888:8888**  - maps port 8888 on the host to port 8888 on the container, hence the URL ``http://127.0.0.1:8888/lab``

* How do I execute a bash shell in a running container?

  This can be handy thing to do, as it doesn't impact what you're already doing in the container. It just gives you another shell to possibly check on or update something (e.g., install a missing python package).   To demonstrate it let's start the container running the jupyer session as described above (load it into your browser a quick check to see its running as expected).

  Next I need to figure out what the ID or name of the container is.  I could use the container ID from the prompt (as noted earlier).  But for this lets just use

  .. code-block:: sh

     docker ls -a

  which on my laptop shows

  .. code-block:: console
  
    moulton@pn2401338 website % docker container ls
    CONTAINER ID   IMAGE                                    COMMAND                  CREATED         STATUS                  PORTS                                         NAMES
    52cf4c018e70   metsi/ats-short-course:2025-ats-latest   "jupyter lab --port=…"   4 minutes ago   Up 4 minutes            0.0.0.0:8888->8888/tcp, [::]:8888->8888/tcp   stoic_chaplygin
    06b97288758e   ecoon/watershed_workflow-ats:v2.0        "tini -g -- start.sh…"   32 hours ago    Up 32 hours (healthy)   0.0.0.0:9999->9999/tcp, [::]:9999->9999/tcp   clever_engelbart

  So we can see there is a container ID **52cf4c018e70**, and a funky human readable name **stoic_chaplygin** that docker created (scroll to the far right to see the name).  I can user either when I execute a bash shell in ths container

  .. code-block:: sh

    docker exec -it stoic_chaplygin /bin/bash

  which gives a prompt similar to above

  .. code-block:: console
      
    (base) ats_sc_user@52cf4c018e70:~/work$

  but note the minor differences:

  * the hostname is now **52cf4c018e70**, reflecting the ID of this container
  * the present working directory is **~/work**, the default prescribed when the container was created

  From here you could check what jobs are running, install a conda package etc. But you are limited to what the ats_sc_user is allowed to do.

* How do I execute a privileged (root) shell in a running container

  What if you need to fix something in a running container and you need administrative access to do it (i.e., root). Like install missing tools using apt-get. To do this you simply add the user option to the command we demonstrated in the last example,

  .. code-block:: sh
                   
     docker exec -it -u root stoic_chaplygin /bin/bash

  which gives a prompt showing the user is **root**

  .. code-block:: sh

      (base) root@52cf4c018e70:~/work#
   
   
Jupyter Lab Tips
----------------

FAQs we are adding here:
^^^^^^^^^^^^^^^^^^^^^^^^

 * How do I figure out what process is using the port I want for Jupyter?
 * How would I start the ATS or Watershed Workflow container to use a different port?


ParaView Tips
-------------

FAQs we are adding here:
^^^^^^^^^^^^^^^^^^^^^^^^

 * how to load and use the LegacyExodus Reader in ParaView so that you can view mixed-element meshes generated by Watershed Workflow
 * how to convert an Exodus mesh output from Watershed Workflow to one that can be viewed fully in Paraview

