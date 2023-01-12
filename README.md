---
title: Homework 6
due: 11:59PM, April 22, 2022
---


# Homework 6: Reliable Communication II

In this homework, you will improve upon the stop and wait implementation of
homework 5.  Please see the description of Homework 5 for the basics. Everything is
the same about this assignment except for the file sizes, buffer sizes, and
throughput cutoffs. You are welcome to use and extend your implementation of the stop and wait in the previous homework.


### Writing Your Solution

This repo contains several tools that will help you simulate and test your
solution.  **You should not make changes to any file other than `hw6.py`.**
All other files contain code used to either simulate the unreliable connection,
or code to help you test your your solution.

Your solution / `hw6.py` file will be tested against stock versions of all the
other files in the repo, so any changes you make will not be present at
grading time.

Your solution must be contained in the `send` and `recv` functions in `hw6.py`.
You should not change the signatures of these functions, only their bodies.
These functions will be called by the grading script, with parameters
controlled by the grading script.  Your solution must be general, and should
work for any file, so make sure to test your code with different file types, text, jpg, gif, executables, etc.

Your task is to modify the bodies of these functions so that they communicate
using a protocol that ensures that the data sent by the `send` function
can be reliably and quickly reconstructed by the `recv` function.  You should
do so through a combination of setting timeouts on socket reads (e.x.
`socket.settimeout(float)`) and developing a system through which each side can
acknowledge if / when they receive a packet.


### Testing Your Solution

You can use the provided `tester.py` script when testing your solution.  This
script uses the `receiver.py`, `sender.py`, and `server.py` scripts to
simulate an unreliable connection, and to test your solution.

The `tester.py` script contains many parameters you can use to test your
solution under different conditions, and to receive different amounts
of debugging information to better understand the network.  These
parameters and options can be viewed by calling `tester.py --help`, and are
also reproduced below.


    usage: tester.py [-h] [-p PORT] [-l LOSS] [-d DELAY] [-b BUFFER] -f FILE
                    [-r RECEIVE] [-s] [-v]

    Utility script for testing hw6 solutions under user set conditions.

    optional arguments:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  The port to simulate the lossy wire on (defaults to
                            9999).
    -l LOSS, --loss LOSS  The percentage of packets to drop.
    -d DELAY, --delay DELAY
                            The number of seconds, as a float, to wait before
                            forwarding a packet on.
    -b BUFFER, --buffer BUFFER
                            The size of the buffer to simulate.
    -f FILE, --file FILE  The file to send over the wire.
    -r RECEIVE, --receive RECEIVE
                            The path to write the received file to. If not
                            provided, the results will be written to a temp file.
    -s, --summary         Print a one line summary of whether the transaction
                            was successful, instead of a more verbose description
                            of the result.
    -v, --verbose         Enable extra verbose mode.


For example, to see how your solution performs when transmitting a text file,
with a 5% loss rate, and with a latency of 100ms, you could use the following:
`python3 tester.py --file test_data.txt --loss .05 --delay 0.1`.


### Hints and Suggestions

 * Use the included `--verbose` option to include very detailed information
   about what your code is sending over the network, and how the network
   is handling that data.

 * Use the included `--receive` option to see the results of your file transfer.
   By default, the testing script will store the results of your code to a
   temporary location.  This option may be useful if you're not sure how or
   why the received file does not match the sent file.

 * Make sure you try your solution under many different loss ratios and
   latencies by changing the parameters in the `tester.py` script. In the next
  section, we have also provided you with the test cases and latencies for
  evaluating the performance of your implementation.

 * Keep your packets smaller than or equal to `homework6.MAX_PACKET` (1400
   bytes).


### Grading

You solution will be graded by using it to transfer six different files,
each under different simulated test conditions.  For each test case, there is a
minimum throughput requirement and a timeout for your program to exit.

The table below provides the test case parameters for `tester.py` along with
the upper bounds of the fast and slow transmissions.

|Case # |File Size  |Loss |Delay  | Buffer  |Fast (sec)|Slow (sec)  |
|-------|-----------|-----|-------|---------|----------|------------|
|1      |10KB	      |0    |0.5    |10       |10.5      |14          |
|2      |100KB      |0    |0.1    |20       |7.5       |10          |
|3      |2MB        |0    |0.01   |30       |9         |12          |
|4      |30KB       |0.1  |0.1    |40       |9         |12          |
|5      |4MB        |0.1  |0.01   |50       |48        |64          |
|6      |5MB        |0    |0.01   |60       |18        |24          |


Each test case will be scored accordingly:

| Case                                           | Points Earned |
| ---------------------------------------------- | ------------- |
| File is not transmitted correctly              |             0 |
| Transmission takes longer than the max time    |             0 |
| Successful transmission, but low throughput    |             1 |
| Successful transmission, fast throughput       |             2 |


If your program exits normally before the timeout, but the content of the
received file is invalid, then **zero points** are awarded.

If your program doesn’t exit before the timeout, it will be terminated
before completion, resulting in incorrect file content, and so **0 points**.

If the program exits normally before the timeout and the received file’s content
is valid *but* the throughput obtained is lower than the required minimum
throughput then you receive **1 point**.

If your program correctly transmits the file below the timeout, and with the
required throughput, it will receive **2 points**.

Code that earns at least 5 of the above points, and which is both "pep 8 (pycodestyle)" and
"pylint" compatible will earn an additional **1 point**.

There are 13 points possible on this assignment.  Your solution will be graded
out of 12 possible points.

This assignment is due **April 22 at 11:59pm**.
