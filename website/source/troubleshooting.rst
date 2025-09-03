Troubleshooting
===============

The containers can be tricky to install.  Here are some common problems and their fixes.

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

   



                

