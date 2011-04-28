#!/bin/bash

input="wso2-wsf-cpp-src-$1.tar.gz"

if [ ! -f $input ] ; then
   echo "$0: $input is not a regular file";
   exit 1;
fi

echo "Processing $input"

echo "...extracting $input"
tar xzf $input

cd wso2-wsf-cpp-src-$1

for f in \
    wsf_c/axis2c/util/src/minizip \
    wsf_c/sandesha2c/src/storage/sqlite/sqlite3.h \
    wsf_c/sandesha2c/src/storage/sqlite/sqlite3.c \
    wsf_c/savanc/include/sqlite3.h \
    wsf_c/savanc/src/subs_mgrs/sqlite/sqlite3.c \
    wsf_c/docs/savanc/api/sqlite3_8h-source.html;
do
    echo "...removing $f";
    rm -rf $f;
done;

patch -p1 < ../wso2-nobuild-minizip.patch
patch -p1 < ../wso2-nobuild-sqlite3.patch

echo "...creating wso2-wsf-cpp-src-$1-trimmed.tar.gz"
cd ..
tar czfsp wso2-wsf-cpp-src-$1-trimmed.tar.gz wso2-wsf-cpp-src-$1

echo "...cleaning up"
rm -rf wso2-wsf-cpp-src-$1

