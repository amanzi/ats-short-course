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
 * What containers do I have running?
 * What containers do I have on my system (running and stopped)?
   
 * Running a bash shell when you start the container
 * Executing a bash shell in a running container
 * Executing a privileged (root shell) in a running container

   
 * How do I just user the ATS container to run an ATS simulation on my system
   
 * How do I prevent stopped containers from being saved (--rm option)
 * How do I removed stopped containers (prune)

   
Jupyter Lab Tips
----------------

FAQs we are adding here:
^^^^^^^^^^^^^^^^^^^^^^^^

 * How do I figure out what process is using the port I want for Jupyter?
 * How would I start the ATS or Watershed Workflow container to use a different port?


