# Arcimoto Lambda Global Dependencies

This repo contains the package and dependencies to build the Arcimoto Global Dependencies Lambda Layer that is attached to each lambda during deployment. It also builds a dev and staging version of the layer. The layer automatically builds in the attached BitBucket pipeline.

## Contributors

- Cord Slatton - Repo Man (Authorizes changes to master branch)
- Keith Anderson
- Gary Malcolm

## Contributing

### Git commit formatting

We use the `Angular git commit` style

Full (long) version:

```git commit template
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

Short version

```git commit template
<type>(<scope>): <subject>
```

See https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format more details

VS Code extension that helps you to make the commit msg, no need to remember your scope, etc.:
https://marketplace.visualstudio.com/items?itemName=Jhecht.git-angular

We use the allowed `types` from https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format

We use custom `scopes` per repository, see `scopes` below. If you need to add a scope that is allowed.

#### Scopes

- args
- db
- dependencies
- exceptions
- note
- pipeline
- runtime
- tests
- user
- vehicle

### Prerequisites

The majority of the AWSLambda repo code is written in Python and meant to be executed by [AWS Lambda](https://aws.amazon.com/lambda/) in a Python 3 runtime environment. The currently used version of Python is 3.8, to maintain compatibility with the `psycopg2` package. Many of the functions rely on the AWS SKD for Python, [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

Install `boto3` using pip:

```sh
pip install boto3
```

Additionally, in order to run Lambda functions which interact with AWS services, use the AWS [Command Line Interface (CLI)](https://aws.amazon.com/cli/).  
Install `CLI` using pip:

```sh
pip install awscli
```

In order to use the CLI, you will also need the proper AWS credentials, managed by the AWS [Identity and Access Management (IAM)](https://console.aws.amazon.com/iam/home?#/home) service.  Have the Arcimoto AWS administrator create CLI credentials for you, or give you IAM permission to create them yourself.  Then on the command line run:

```sh
aws configure
```

and enter the Access Key ID and Secret Access Key that you just created.

### Installing

#### For development

To get the AWSLmbda Lambda functions running locally, first obtain a local copy by cloning the repository.  From the directory that you want to install your local copy, use git on the command line:

```sh
git clone https://<username>@bitbucket.org/arcimotocode1/arcimoto-lambda-global-dependencies.git
```

Where `<username>` is your bitbucket user name.

#### To Run unit tests

You must set up a python virtual env

```cli
python -m venv venv
```

and then install the package dependencies

```cli
pip install boto3 cerberus psycopg2 xmlrunner
```

at which point you should be able to run the tests

```cli
python -m unittest discover
```

#### For usage (installation via pip)

Setup a bitbucket app password with read access to your account's repositories and substitute the username into the command:

```sh
pip install git+https://{{BITBUCKET_USERNAME}}@bitbucket.org/arcimotocode1/arcimoto-lambda-global-dependencies.git
```

## Directory Layout

### dependencies.json

Used to identify resources and their configuration.

### dependencies

Global dependencies and corresponding layer configuration.

#### cerberus

From the [cerberus package](https://pypi.org/project/Cerberus/) extracted.

#### certifi

From the [certifi package](https://pypi.org/project/certifi/#files) using the wheel file type, extracted.

## Python versions and psycopg2

The `global_dependencies` layer builds for a specific python3 minor (3.8) version due to compatibility with psycopg2 (postgres db interaction package).

### Upgrading lambda python3 runtimes

The compatibility with psycopg2 requires a build for a specific runtime of python3 for our `global_dependencies` layer. Rather than compile `psycopg2` for the AWS Lambda environment ourselves we can use [awslambda-psycopg2](https://github.com/jkehler/awslambda-psycopg2) an open source repository that maintains compiled versions of psycopg2 for each version of python.

- Copy the `psycopg2-3.x` directory from the [awslambda-psycopg2](https://github.com/jkehler/awslambda-psycopg2) repository matching your intended minor version of python3 into your AWS Lambda project `dependencies` folder and rename the folder to `psycopg2` before zipping it into a file called `psycopg2.zip`. This will then be used in any subsequent lambda creation or updates by the lambda-utility commands in this repository ONLY if they directly use the `psycopg2` module as a `common_dependency`. However, newer, upgraded lambdas rely on our `global_dependencies` layer.
- Create a new layer version for the `global_dependencies` with a compatible runtime set to match the minor version of python3 you are upgrading to using the lambda-utility. After the layer is created via the lamda-utility it will return a version number: in `dependencies.json` set the `layers.global_dependencies.version` property to the new layer version number. This will cause subsequent `create` and `update` lambda-utility commands to use the new layer (and the upgraded version of python and psycopg2).

## BitBucket Pipelines

The BitBucket pipelines file [bitbucket-pipelines.yml] implements the Continuous Integration (CI)/Continuous Deployment (CD) for the AWSLambda repository.

### Pipelines

#### Run Tests (PR to dev)

The tests are run automatically on Pull Request (PR) creation/update from a feature branch beginning with the prefix `TEL-` to the `dev` branch.

These tests include:

- testing the `dependencies.json` file JSON validity
- unit tests

Any failed tests will result in a failure of the pipeline, which will prevent merging the PR to `dev` until the PR is updated to fix the issue(s) and the pipeline is re-run successfully for the PR.

#### Merge to dev branch

- Upon merge to `dev` from a feature branch prefixed with `TEL-` the pipeline creates a new global dependencies dev layer version.

#### Merge to staging branch

- Upon merge to `staging` branch the pipeline creates a new global dependencies staging layer version.

#### Merge to master branch

Upon merge to `master` branch the pipeline:

- publishes a new version using semantic versioning
- creates a new global dependencies production layer version
- creates a pull request in the dependent repository `awslambda` for the change in hash for this repo
