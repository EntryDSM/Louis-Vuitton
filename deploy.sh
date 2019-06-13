#! /bin/bash
version=`python -c "import lv; print(lv.__version__)"`

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "$1" == "dev" ]];then
    echo "Build on dev"

    docker build -t registry.entrydsm.hs.kr/lv:dev .

    docker push registry.entrydsm.hs.kr/lv:dev
elif [[ "$1" == "master" ]];then
    echo "Build on master"

    docker build -t registry.entrydsm.hs.kr/lv:${version} .

    docker tag registry.entrydsm.hs.kr/lv:${version} registry.entrydsm.hs.kr/lv:latest

    docker push registry.entrydsm.hs.kr/lv:${version}
    docker push registry.entrydsm.hs.kr/lv:latest

fi

exit