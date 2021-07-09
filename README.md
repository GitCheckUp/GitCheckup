# Welcome to GitCheckup!

We know Git can be hard to understand and become proficient at. GitCheckup analyzes your GitHub repository to detect errors and poor practices to help you and your team work more efficiently and accurately.


Installation and Deployment
===========================

There are several options to install and deploy GitCheckup. We make sure
that everybody can reach this tool easily.

GitCheckup Web Service
----------------------

If you would like to directly get to the results, just visit
<https://gitcheckup.github.io>.

Deploying with Docker
---------------------

You need to have a machine Docker(<https://docs.docker.com/get-docker/>)
and\
DockerCompose(<https://docs.docker.com/compose/>) installed. Clone the
source code from <https://github.com/gitcheckup/gitcheckup>:

    #Get the source code
    git clone https://github.com/gitcheckup/gitcheckup
    #Get into the folder
    cd gitcheckup

Run the following command:

    #Run docker-compose script
    docker-compose up -d

This will build the docker image with all the dependencies. After
initialization process finishes, GitCheckup will be reachable at
<http://localhost:8008>.

Running From the Source Code
----------------------------

To use this option, make sure that you have all the dependencies on your
machine.\
\
1 .You need to install Python 3.9 or higher.
<https://www.python.org/downloads/>.\

​2. Clone the source code, you can skip this if you have already
installed the software package locally, in which case use the ’cd’
command to go to the folder and continue from step 3:

    #Get the source code
    git clone https://github.com/gitcheckup/gitcheckup

​3. Go to the gitcheckup folder within the installation:

    #Go to the folder
    cd gitcheckup

​4. Install the necessary packages with pip. Run the following command:

    #Installing python dependencies
    pip install -r requirements.txt

​5. Run the Django server using following command:

    #Running Django's web server.
    python manage.py runserver 0.0.0.0:8008

After the initialization process finishes, GitCheckup will be reachable
at <http://localhost:8008>.
