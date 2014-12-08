Author: Stephen Rosen

sns-notify
==========

This is designed to be the simplest possible script for sending SNS
notifications without compromising flexibility.


Why Are Notifications Objects
-----------------------------

Although it makes the code more complicated, representing notifications as
objects makes this code more extensible if someone wanted to use it as a
package in another project.
To maintain simplicity, the SNSMessage objects are little more than containers
wrapped around their attributes.
