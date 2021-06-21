# HumanLoop-Debugger

A web-app based debugger for HumanLoop


## Installation

After cloning/downloading the repository, simply install HumanLoop-Debugger as a package into your target virtual environment:

    $ pip install PATH_TO_humanloop_debugger

During development you will likely want to perform an editable install so that
changes to the source code take immediate effect on the installed package.

    $ pip install -e PATH_TO_humanloop_debugger


## Running Your App

This project comes with two convenience scripts for running your project in
development and production environments, or you can use your own WSGI server to
run the app.


### Run Dev App 

Installing this package into your virtualenv will result into the development
executable being installed into your path when the virtualenv is activated. This
command invokes your Dash app's `run_server` method, which in turn uses the
Flask development server to run your app. The command is invoked as follows

    $ run-humanloop_debugger-dev

The script takes a couple of arguments optional parameters, which you can
discover with the `--help` flag. You may need to set the port using the `--port`
parameter. If you need to expose your app outside your local machine, you will
want to set `--host 0.0.0.0`.


### Run Prod App

While convenient, the development webserver should *not* be used in
production. Installing this package will also result in a production executable
being installed in your virtualenv. This is a wrapper around the
`mod_wsgi-express` command, which streamlines use of the [mod_wsgi Apache
module](https://pypi.org/project/mod_wsgi/) to run your your app. In addition to
installing the `mod_wsgi` Python package, you will need to have installed
Apache. See installation instructions in the [mod_wsgi
documentation](https://pypi.org/project/mod_wsgi/). This script also takes a
range of command line arguments, which can be discovered with the `--help` flag.

    $ run-humanloop_debugger-prod
    
This script will also apply settings found in the module `humanloop_debugger.prod_settings` (or a custom Python file supplied
with the `--settings` flag) and which takes precedence over the same settings
found in `humanloop_debugger.settings`.

### Screenshots

![](debugger_gif.gif)

![](screenshot_1.png)

![](screenshot_2.png)
