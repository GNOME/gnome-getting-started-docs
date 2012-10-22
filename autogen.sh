#!/bin/sh
# Run this to generate all the initial makefiles, etc.

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.

PKG_NAME="gnome-getting-started-docs"

(test -f $srcdir/configure.in \
  && test -d $srcdir/getting-started) || {
    echo -n "**Error**: Directory "\`$srcdir\'" does not look like the"
    echo " top-level $PKG_NAME directory"
    exit 1
}

which gnome-autogen.sh || {
    echo "You need to install gnome-common from the GNOME Git"
    exit 1
}

REQUIRED_AUTOMAKE_VERSION=1.6
export REQUIRED_AUTOMAKE_VERSION

USE_GNOME2_MACROS=1 . gnome-autogen.sh