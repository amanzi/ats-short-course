# Docker Tips

Docker has become a very popular tool for packaging software, and there are numerous tutorials on using Docker. But before you spend a lot of time reviewing tutorials, note that in most cases there are only a few simple commands that you'll be using we summarize those here.

## Key Terminology

As with any technology there is some jargon that we need to keep straight otherwise things that are relatively simple will seem very confusing.  First, it is important to define the terms image and container:

  * _Image_: A docker image includes everything that is needed to run an application in a docker container, such as, code, libraries, environment variables, etc.  Note images are what we build and share with you through docker hub, such as the metsi/ats-short-course:latest image you pulled down to  your system. 
  
  * _Container_: A docker container is a runtime instance of a docker image.  So when you run jupyterlab it is running in a container that is an instance of the docker image metsi/ats-short-course:latest.  So you could have many containers started from the same image, you can run multiple shells 

Since images and containers are different entities, it's important to understand which docker commands interact with which entity.  

## Common Commands

### Downloading Docker Images (DockerHub)

Images are downloaded from dockerhub automatically when used in a _docker run_ command, but can also be downloaded manually using _docker pull_.  For example, you pulled the docker image for this short course with the command

```sh
docker pull metsi/ats-short-course:latest 
```

Here it's useful to breakdown the name of the image a little to explain how docker keeps track of versions:

* _metsi_: is the username on DockerHub.  Metsi is water in Sesotho, a South African language (since Amanzi, which is water in Zulu was already taken).
* _ats-short-sourse_: is the name of the repository of images
* _latest_: is the tag, a convenient mutable tag that we use to point to the latest build

It's important to note that each image has a full sha1 hash similar to what you would see with commits on git.  This unique identifer is important as it gives you a way to confirm the _latest_ on your system is in fact the _latest_.

### What Images do I have?

```sh
docker image ls -a
```

Here is sample output from my system

```sh
moulton@pn2003009 ats-short-course % docker image ls -a
REPOSITORY               TAG                  IMAGE ID       CREATED          SIZE
metsi/ats-short-course   latest-linux         64d5147af800   37 minutes ago   7.07GB
metsi/ats-short-course   latest               f4244e446b24   22 hours ago     7.07GB
```

Note the IMAGE ID shows the leading entry in the unique sha1 for the image.

### What Containers do I have?

It's easy to start multiple containers from a single image, and so sometimes we end up with bunch of these taking up storage and resources without realizing it.

```sh
docker container ls -a
```    

This command reports the status, container ID, and container NAME of any active containers.  The _-a_ option ensure you get all the containers, including those that are stopped.

If a container is already stopped we can remove it.

```sh
docker container rm <ID>
```

```sh
docker container rm <NAME>
```

# Troubleshooting

## Download from DockerHub failed?

A common problem is the storage that you have allocated for Docker images and containers has been exhausted. To check your storage enter,

``` sh
docker system df
```

And compare the usage ("SIZE") with what you have allocated for space in your Docker "Preferences".  You may see significant space is "RECLAIMABLE".  As a start consider pruning the image layers that aren't connected to images that are being used:

``` sh
docker system prune -f 
```

If you need more space, consider purging all unused images with "-a".

Note also that OSX machines can blank the screen or sleep, both of which can pause the download and not recover.  Setting the battery settings to never blank the screen (preferably when plugged in) and potentially running the ``caffeinate`` command to stop OSX from sleeping may be helpful on slow internet connections.


## Tutorials

For example, here are a few links to tutorials you may want to look at:

<ADD LINKS HERE>



