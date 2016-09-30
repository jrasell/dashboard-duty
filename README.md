Dashboard Duty
==============

Dashboard Duty is a simple PagerDuty dashboard designed to allow teams to keep a track of their alerts and who is currently first line on-call for their service.

![Dashboard Duty UI](https://lh3.googleusercontent.com/2PZk-5oqVdL-J22I2Aco2dCSQXKlg_d3eYa4GAa8jqflswUIfR1g6NqEpqcipEBVxCyu20G5=w1280-h699-rw)

Environment Variables
---------------------

Dashboard Duty needs two environment variables set in order to run. The first is `DASHBOARD_DUTY_SERVICE` which is the name of the PD service which you wish to display. The second is `DASHBOARD_DUTY_KEY` which needs to be a V2, Read-Only PagerDuty API key. 

Running With Docker
-------------------

You can either build the docker image yourself or simply pull the pre-built image which is available from Docker Hub.

Pulling from Docker Hub:
```sh
$ docker pull jrasell/dashboard-duty
```

Building from source:
```sh
$ git clone https://github.com/jrasell/dashboard-duty.git
$ cd dashboard-duty
$ docker build .
```

Running a container:
```sh
$ docker run --rm -p 5000:5000 -e DASHBOARD_DUTY_SERVICE='<PD_Service_Name>' -e DASHBOARD_DUTY_KEY='<PD_API_Key>' <docker_image>
```

Running without Docker
----------------------

Firstly you will need to have a local clone of this repository. Then use virtualenv to run the application and install the requirements. If you do not have virtualenv installed:
```sh
$ pip install virtualenv
```

From here you can setup your virtulenv and install the requirements:
```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install requirements.txt
```

In order to run the application, the environment variables must be set:
```sh
$ export DASHBOARD_DUTY_SERVICE='<PD_Service_Name>'
$ export DASHBOARD_DUTY_KEY='<PD_API_Key>'
$ python dashboard_duty/app.py
```

Known Limitations
-----------------

 * The escalation policy linked to the service currently needs to be a schedule and doesn't handle being an individual user.

Contributing
------------

Any contributions are much appreciated. If you would like to contribute please open a pull-request.
