#!/bin/bash

function usage() {
    cat <<EOF
Usage: ./runtests.sh SUITE

Where SUITE is one of:

ut  - unit tests
sm  - smoke tests
ft  - functional tests
all - run all the tests

server - don't run the tests, just start the server
EOF
}

case $1 in
    "ft")
	export TESTCHOICE="ft"
	;;
    "ut")
	export TESTCHOICE="ut"
	;;
    "sm")
	export TESTCHOICE="sm"
	;;
    "server")
	export TESTCHOICE="server"
	;;
    "all")
	export TESTCHOICE="all"
	;;
    *)
        usage
        exit 1;
        ;;
esac


set RECREATEDB = "x"
while [ "${RECREATEDB}" != "Y" -a "${RECREATEDB}" != "y" -a "${RECREATEDB}" != "N" -a "${RECREATEDB}" != "n" ]
do
    read -s -n1 -p "Do you want to recreate db in couch (*** recommended y ***)? [Y/n]" RECREATEDB
    echo
    if [ -z ${RECREATEDB} ]; then
	break
    fi
done

cd src/datawinners

if [ "${RECREATEDB}" != "N" -a "${RECREATEDB}" != "n" ]; then
    python manage.py syncdb --noinput
    python manage.py migrate
    python manage.py recreatedb
fi

if [ "${TESTCHOICE}" != "ut" ]; then
    cp local_settings.py ../../func_tests/resources/local_settings.py
fi 

function start_server() {
    xterm -e "python manage.py runserver --settings=datawinners.settings_automated_testing" &
    sleep 2
}

case "${TESTCHOICE}" in
"ft")
     echo "-------- Funtional test execution Started --------"
     start_server
     cd ../../func_tests
     nosetests -a 'functional_test'
     ;;
"sm")
     echo "-------- Funtional test execution Started --------"
     start_server
     cd ../../func_tests
     nosetests -a 'smoke'
     ;;
"ut") echo "-------- Unit test execution Started --------"
     python manage.py test --with-xunit --xunit-file=../../xunit.xml
     cd ..
     cd mangrove && nosetests --with-xunit --xunit-file=../../xunit2.xml
     ;;
"server") echo "----- Starting the server ----"
     start_server
     ;;
"all") echo "-------- All test execution Started --------"
     xterm -e "python manage.py runserver" &
     nosetests --with-xunit --xunit-file=../../xunit.xml
     cd ..
     cd mangrove && nosetests --with-xunit --xunit-file=../../xunit2.xml
     cd ../..
     cd func_tests && nosetests --with-xunit --xunit-file=../xunit3.xml
     ;;
esac

exit 0
