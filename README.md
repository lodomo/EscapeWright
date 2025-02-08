# Escape Wright

## Description

Escape Wright is a way to create escape rooms quickly, and have an entire network
of raspberry pis available at your finger tips. Setting up each raspberry pi 
is not a trivial task, but this makes it much easier. Originally planned
as a Python Library, Escape Wright is more of a framework for putting files
where they need to go, and preparing all the services needed to run each pi.

## Installation

It's easiest to let the installer do the work for you, download a little too much
and then clean up the junk you don't need.

////// TODO

## Server Types

### Control Panel
The control panel runs two servers. A frontend and a backend. The frontend
is purely to talk to the backend, and backend will be in communication with
the raspberry pis throughout the room. The sub-pis are called "Modules"

### Modules
These modules are what actually are functioning in the room. They could be
a puzzle, they could just be a screen somewhere. Most of them should need to
"start, stop, and reset" and have a series of commands that do things directly.


