import osgconf

VERSION = "0.0.1"
AUTHOR  = "Jeremy Moles, Cedric Pinson"
EMAIL   = "jeremy@emperorlinux.com, mornifle@plopbyte.net"
URL     = "http://www.plopbyte.net, http://hg.plopbyte.net/osgexport"

DOC = """
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

NOTE:

This code is inherited from the project I did (Jeremy) w/ Palle Raabjerg
for a Google SOC project in Cal3D. There may still be some remnants of that
project here, but most of this is SUPERBLY modified.
"""

# A decorator to catch any exception semi-gracefully. Sometime later
# this will create a Blender panel to show the exception, since errors to the console
# are pretty damn useless.
def exception(function):
	def exceptionDecorator(*args, **kargs):
		try:
			return function(*args, **kargs)

		except Exception, e:
			print "Exception in", function.func_name, "- error was:", e

	return exceptionDecorator

# A function that will parse the passed-in sequences and set the appropriate
# values in atkconf.
@exception
def ParseArgs(parse):
	args     = []
	strip    = lambda s: s.rstrip().lstrip().replace("\t", "").replace("\n", "")
	str2bool = lambda s: s.lower() == "true" or s == "1"

	for arg in parse:
		arg = strip(arg)
	
		# Check and maks sure we're formatted correctly.
		if "--animtk" in arg:
			if len(arg) >= 9 and arg[8] == "=":
				args = arg[9 : ].split(";")

			else:
				print "ERROR: OpenSceneGraph format is: --osg=\"filename=foo;\""

	for arg in args:
		if "=" in arg:
			a, v = arg.split("=")
			a    = strip(a).upper()
			v    = strip(v)

			print "OSG Option [", a, "] =", v

			{
				"FILENAME":   lambda: setattr(atkconf, a, v),
				"AUTHOR":     lambda: setattr(atkconf, a, v),
				"LOG":        lambda: setattr(atkconf, a, str2bool(v)),
				"SELECTED":   lambda: setattr(atkconf, a, str2bool(v))
			}[a]()

	# Return args; since this will be False by default, we'll use this
	# to determine if the user passed a --osg argument.
	return args
