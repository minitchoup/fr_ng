#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

INSTALL=true

if [ "$1" = "-u" ]; then
    INSTALL=false
fi
    
INSTALL_BASE_DIR=/usr/share/X11/xkb
INSTALL_SYMBOLS_DIR="$INSTALL_BASE_DIR/symbols"
if $INSTALL; then
    ./mkxkb.py -i fr_ng -o fr_ng_new
    if [ -f "$INSTALL_SYMBOLS_DIR"/fr_ng-previous ]; then
        mv -v "$INSTALL_SYMBOLS_DIR"/fr_ng-previous "$INSTALL_SYMBOLS_DIR"/fr_ng-$(date +"%Y%m%d-%H%M%S")
    fi
    mv -v "$INSTALL_SYMBOLS_DIR"/fr_ng "$INSTALL_SYMBOLS_DIR"/fr_ng-previous &&
        cp -v fr_ng_new "$INSTALL_SYMBOLS_DIR"/fr_ng
else
    cp -v "$INSTALL_SYMBOLS_DIR"/fr_ng-previous "$INSTALL_SYMBOLS_DIR"/fr_ng
fi
chmod a+r "$INSTALL_SYMBOLS_DIR"/fr_ng
