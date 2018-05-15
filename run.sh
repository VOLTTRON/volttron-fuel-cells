#/usr/bin/env bash

CONTAINER_NAME="fuel"
VHOME=`pwd`
VHOME="$VHOME/vhome"

if [ ! -d "$VHOME" ]; then
    mkdir -p "$VHOME"
fi

CID="$(docker ps -q -a -f name=$CONTAINER_NAME)"

if [ -n $CID ]; then
    docker rm $CID
fi

docker run -v $VHOME:/home/volttron/.volttron -e LOCAL_USER_ID=$UID --name=$CONTAINER_NAME --net=host -it volttron/fuel-cells
