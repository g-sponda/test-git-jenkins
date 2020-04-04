# aws_dms_task_status_exporter

This is an exporter for monitor status of AWS DMS replication tasks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This project requires installed in your machine the Python 3.7 and pip.

With that packages, you will need to install some libs for the project, to install then, use the follow command:

```
pip install -r requirements.txt
```

Now you have all the dependencies :)

### Installing

To run locally, you need all prerequisites installed.

Before execute, create a yaml file, with all replication tasks id you want to monitor the status, you could modify or base your yaml in `example.yml`.

This project uses three environment variables, which you need to create, the envs are:
* AWS_ACCESS_KEY (access key with dms read permissions)
* AWS_SECRET_KEY (secret key)
* AWS_REGION (Optional/May be declared in yaml file as `region`)

Now to execute the exporter, just run:

```
python exporter.py --file example.yml
```

Case you prefer run in docker, build the image and run the container:

```
docker build -t aws_dms_task_status_exporter .
```

```
docker run -itd --name exporter -p 9213:9213 -e ACCESS_KEY="<ACCESS_KEY>" -e SECRET_KEY="<SECRET_KEY>" -e REGION="<REGION>" aws_dms_task_status_exporter:latest
```

To see the metrics, you can access: 
`localhost:9213/metrics`

<!-- ## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system -->

## Built With

* [Python 3.7](https://docs.python.org/3.7/index.html) - Programming Language
* [Pip](https://pip.pypa.io/en/stable/) - Dependency Management
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - SDK for AWS
* [prometheus_client](https://github.com/prometheus/client_python) - Prometheus instrumentation library for Python

<!-- ## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).  -->

## Authors

* **Guilherme Sponda** - *Initial work* - [g-sponda](https://github.com/g-sponda)

See also the list of [contributors](https://github.com/g-sponda/aws_dms_task_status_exporter/contributors) who participated in this project.

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc -->

