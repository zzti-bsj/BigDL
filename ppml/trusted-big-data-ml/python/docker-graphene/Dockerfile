ARG BIGDL_VERSION=2.1.0-SNAPSHOT
ARG SPARK_VERSION=3.1.2
ARG TINI_VERSION=v0.18.0
ARG JDK_VERSION=8u192
ARG JDK_URL=your_jdk_url
ARG SPARK_JAR_REPO_URL=your_spark_jar_repo_url

# stage.1 graphene
FROM ubuntu:20.04 AS graphene

ARG HTTP_PROXY_HOST
ARG HTTP_PROXY_PORT
ARG HTTPS_PROXY_HOST
ARG HTTPS_PROXY_PORT

RUN env DEBIAN_FRONTEND=noninteractive apt-get update && \
    env DEBIAN_FRONTEND=noninteractive apt-get install -y autoconf bison build-essential coreutils gawk git libcurl4-openssl-dev libprotobuf-c-dev protobuf-c-compiler python3-protobuf wget
RUN git config --global http.proxy http://$HTTP_PROXY_HOST:$HTTP_PROXY_PORT && \
    git config --global https.proxy https://$HTTPS_PROXY_HOST:$HTTPS_PROXY_PORT && \
    git clone https://github.com/analytics-zoo/graphene.git /graphene
RUN cd /graphene && \
    git fetch origin branch-0.7 && \
    git checkout branch-0.7
RUN cd /graphene/Pal/src/host/Linux-SGX && \
    git clone https://github.com/intel/SGXDataCenterAttestationPrimitives.git linux-sgx-driver && \
    cd linux-sgx-driver && \
    git checkout DCAP_1.7 && \
    cp -r driver/linux/* .
RUN cd /graphene && \
    ISGX_DRIVER_PATH=/graphene/Pal/src/host/Linux-SGX/linux-sgx-driver make -s -j4 SGX=1 WERROR=1 && true
RUN for f in $(find /graphene/Runtime -type l); do cp --remove-destination $(realpath $f) $f; done

# stage.2 jdk & scala & spark & hadoop
FROM ubuntu:20.04 as spark
ARG HTTP_PROXY_HOST
ARG HTTP_PROXY_PORT
ARG HTTPS_PROXY_HOST
ARG HTTPS_PROXY_PORT
ARG SPARK_VERSION
ARG JDK_VERSION
ARG JDK_URL
ARG SPARK_JAR_REPO_URL
ENV SPARK_VERSION       ${SPARK_VERSION}
ENV JAVA_HOME           /opt/jdk$JDK_VERSION
ENV PATH                ${JAVA_HOME}/bin:${PATH}

RUN apt-get update --fix-missing && \
    env DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y tzdata apt-utils wget unzip patch zip git maven
ADD hadoop-common-shell.patch /opt/hadoop-common-shell.patch

# java
RUN wget $JDK_URL && \
    gunzip jdk-$JDK_VERSION-linux-x64.tar.gz && \
    tar -xf jdk-$JDK_VERSION-linux-x64.tar -C /opt && \
    rm jdk-$JDK_VERSION-linux-x64.tar && \
    mv /opt/jdk* /opt/jdk$JDK_VERSION && \
    ln -s /opt/jdk$JDK_VERSION /opt/jdk
# scala
RUN cd / && wget -c https://downloads.lightbend.com/scala/2.11.8/scala-2.11.8.tgz && \
    (cd / && gunzip < scala-2.11.8.tgz)|(cd /opt && tar -xvf -) && \
    rm /scala-2.11.8.tgz
# maven
RUN cd /opt && \
    wget https://archive.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz && \
    tar -zxvf apache-maven-3.6.3-bin.tar.gz
# spark
RUN cd /opt && \
    wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.2.tgz && \
    tar -zxvf spark-${SPARK_VERSION}-bin-hadoop3.2.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop3.2 spark-${SPARK_VERSION} && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.2.tgz && \
    cp spark-${SPARK_VERSION}/conf/log4j.properties.template spark-${SPARK_VERSION}/conf/log4j.properties && \
    echo $'\nlog4j.logger.io.netty=ERROR' >> spark-${SPARK_VERSION}/conf/log4j.properties && \
    rm spark-${SPARK_VERSION}/python/lib/pyspark.zip && \
    rm spark-${SPARK_VERSION}/jars/spark-core_2.12-$SPARK_VERSION.jar && \
    rm spark-${SPARK_VERSION}/jars/spark-launcher_2.12-$SPARK_VERSION.jar && \
    rm spark-${SPARK_VERSION}/jars/spark-kubernetes_2.12-$SPARK_VERSION.jar && \
    rm spark-${SPARK_VERSION}/jars/spark-network-common_2.12-$SPARK_VERSION.jar && \
    rm spark-${SPARK_VERSION}/examples/jars/spark-examples_2.12-$SPARK_VERSION.jar && \
    rm spark-${SPARK_VERSION}/jars/hadoop-common-3.2.0.jar && \
    rm spark-${SPARK_VERSION}/jars/hive-exec-2.3.7-core.jar
ADD ./log4j2.xml /opt/spark-${SPARK_VERSION}/conf/log4j2.xml
# spark modification
RUN cd /opt && \
    wget $SPARK_JAR_REPO_URL/spark-core_2.12-$SPARK_VERSION.jar && \
    wget $SPARK_JAR_REPO_URL/spark-kubernetes_2.12-$SPARK_VERSION.jar && \
    wget $SPARK_JAR_REPO_URL/spark-network-common_2.12-$SPARK_VERSION.jar && \
    wget $SPARK_JAR_REPO_URL/spark-examples_2.12-$SPARK_VERSION.jar && \
    wget $SPARK_JAR_REPO_URL/spark-launcher_2.12-$SPARK_VERSION.jar && \
    wget $SPARK_JAR_REPO_URL/pyspark.zip && \
    mv /opt/spark-core_2.12-$SPARK_VERSION.jar  /opt/spark-${SPARK_VERSION}/jars/spark-core_2.12-$SPARK_VERSION.jar && \
    mv /opt/spark-launcher_2.12-$SPARK_VERSION.jar /opt/spark-${SPARK_VERSION}/jars/spark-launcher_2.12-$SPARK_VERSION.jar && \
    mv /opt/spark-kubernetes_2.12-$SPARK_VERSION.jar /opt/spark-${SPARK_VERSION}/jars/spark-kubernetes_2.12-$SPARK_VERSION.jar && \
    mv /opt/spark-network-common_2.12-$SPARK_VERSION.jar /opt/spark-${SPARK_VERSION}/jars/spark-network-common_2.12-$SPARK_VERSION.jar && \
    mv /opt/spark-examples_2.12-$SPARK_VERSION.jar /opt/spark-${SPARK_VERSION}/examples/jars/spark-examples_2.12-$SPARK_VERSION.jar && \
    mv /opt/pyspark.zip /opt/spark-${SPARK_VERSION}/python/lib/pyspark.zip && \
    sed -i 's/\#\!\/usr\/bin\/env bash/\#\!\/usr\/bin\/env bash\nset \-x/' /opt/spark-${SPARK_VERSION}/bin/spark-class && \
    rm -f /opt/spark-${SPARK_VERSION}/jars/log4j-1.2.17.jar && \
    rm -f /opt/spark-${SPARK_VERSION}/jars/slf4j-log4j12-1.7.16.jar && \
    rm -f /opt/spark-${SPARK_VERSION}/jars/apache-log4j-extras-1.2.17.jar && \
    rm -r /opt/spark-${SPARK_VERSION}/jars/slf4j-log4j12-1.7.30.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/slf4j/slf4j-reload4j/1.7.35/slf4j-reload4j-1.7.35.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.1/log4j-slf4j-impl-2.17.1.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/wildfly/openssl/wildfly-openssl/1.0.7.Final/wildfly-openssl-1.0.7.Final.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure/3.2.0/hadoop-azure-3.2.0.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure-datalake/3.2.0/hadoop-azure-datalake-3.2.0.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/com/microsoft/azure/azure-storage/7.0.0/azure-storage-7.0.0.jar && \
    wget -P /opt/spark-${SPARK_VERSION}/jars/ https://repo1.maven.org/maven2/com/microsoft/azure/azure-data-lake-store-sdk/2.2.9/azure-data-lake-store-sdk-2.2.9.jar


ADD spark-example-sql-e2e.jar /opt/spark-${SPARK_VERSION}/examples/jars/spark-example-sql-e2e.jar

# hadoop
RUN cd /opt && \
    apt-get install -y build-essential && \
    wget https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.bz2 && \
    tar jxvf protobuf-2.5.0.tar.bz2 && \
    cd protobuf-2.5.0 && \
    ./configure && \
    make && \
    make check && \
    export LD_LIBRARY_PATH=/usr/local/lib && \
    make install && \
    protoc --version && \
    cd /opt && \
    git config --global http.proxy http://$HTTP_PROXY_HOST:$HTTP_PROXY_PORT && \
    git config --global https.proxy https://$HTTPS_PROXY_HOST:$HTTPS_PROXY_PORT && \    
    git clone https://github.com/analytics-zoo/hadoop.git && \
    cd hadoop && \
    git checkout branch-3.2.0-ppml && \
    cd hadoop-common-project/hadoop-common && \
    export MAVEN_OPTS="-Xmx2g -XX:ReservedCodeCacheSize=512m \
        -Dhttp.proxyHost=$HTTP_PROXY_HOST \
        -Dhttp.proxyPort=$HTTP_PROXY_PORT \
        -Dhttps.proxyHost=$HTTPS_PROXY_HOST \
        -Dhttps.proxyPort=$HTTPS_PROXY_PORT" && \
    /opt/apache-maven-3.6.3/bin/mvn -T 16 -DskipTests=true clean package && \
    mv /opt/hadoop/hadoop-common-project/hadoop-common/target/hadoop-common-3.2.0.jar /opt/spark-${SPARK_VERSION}/jars/hadoop-common-3.2.0.jar
# hive
RUN cd /opt && \
    git clone https://github.com/analytics-zoo/hive.git && \
    cd hive && \
    git checkout branch-2.3.7-ppml && \
    cd ql && \
    export MAVEN_OPTS="-Xmx2g -XX:ReservedCodeCacheSize=512m \
        -Dhttp.proxyHost=$HTTP_PROXY_HOST \
        -Dhttp.proxyPort=$HTTP_PROXY_PORT \
        -Dhttps.proxyHost=$HTTPS_PROXY_HOST \
        -Dhttps.proxyPort=$HTTPS_PROXY_PORT" && \
    /opt/apache-maven-3.6.3/bin/mvn -T 16 -DskipTests=true clean package && \
    mv /opt/hive/ql/target/hive-exec-2.3.7-core.jar /opt/spark-${SPARK_VERSION}/jars/hive-exec-2.3.7-core.jar

# stage.3 bigdl
FROM ubuntu:20.04 as bigdl
ARG BIGDL_VERSION
ARG SPARK_VERSION
ENV SPARK_VERSION               ${SPARK_VERSION}
ENV BIGDL_VERSION               ${BIGDL_VERSION}
ENV BIGDL_HOME                  /bigdl-${BIGDL_VERSION}
RUN apt-get update --fix-missing && \
    apt-get install -y apt-utils curl wget unzip git
RUN wget https://raw.githubusercontent.com/intel-analytics/analytics-zoo/bigdl-2.0/docker/hyperzoo/download-bigdl.sh && \
    chmod a+x ./download-bigdl.sh
RUN ./download-bigdl.sh && \
    rm bigdl*.zip

# stage.4 ppml
FROM ubuntu:20.04
ARG BIGDL_VERSION
ARG SPARK_VERSION
ARG TINI_VERSION
ENV BIGDL_VERSION                       ${BIGDL_VERSION}
ENV SPARK_VERSION                       ${SPARK_VERSION}
ENV SPARK_HOME                          /ppml/trusted-big-data-ml/work/spark-${SPARK_VERSION}
ENV BIGDL_HOME                          /ppml/trusted-big-data-ml/work/bigdl-${BIGDL_VERSION}
ENV JAVA_HOME                           /opt/jdk8
ENV PATH                                /graphene/meson_build_output/bin:${JAVA_HOME}/bin:${PATH}
ENV LOCAL_IP                            127.0.0.1
ENV SGX_MEM_SIZE                        32G
ENV SGX_LOG_LEVEL                       error
ENV SPARK_MASTER_IP                     127.0.0.1
ENV SPARK_MASTER_PORT                   7077
ENV SPARK_MASTER_WEBUI_PORT             8080
ENV SPARK_MASTER                        spark://$SPARK_MASTER_IP:$SPARK_MASTER_PORT
ENV SPARK_WORKER_PORT                   8082
ENV SPARK_WORKER_WEBUI_PORT             8081
ENV SPARK_DRIVER_PORT                   10027
ENV SPARK_DRIVER_BLOCK_MANAGER_PORT     10026
ENV SPARK_DRIVER_IP                     $LOCAL_IP
ENV SPARK_BLOCK_MANAGER_PORT            10025
ENV TINI_VERSION                        $TINI_VERSION
ENV PYTHONPATH                          /usr/lib/python3.6:/usr/lib/python3.6/lib-dynload:/usr/local/lib/python3.6/dist-packages:/usr/lib/python3/dist-packages
ENV LC_ALL                              C.UTF-8
ENV LANG                                C.UTF-8

RUN mkdir -p /graphene && \
    mkdir -p /graphene/Runtime && \
    mkdir -p /graphene/python && \
    mkdir -p /graphene/Tools && \
    mkdir -p /graphene/Pal/src && \
    mkdir -p /graphene/meson_build_output && \
    mkdir -p /ppml/trusted-big-data-ml/work && \
    mkdir -p /ppml/trusted-big-data-ml/work/lib && \
    mkdir -p /ppml/trusted-big-data-ml/work/keys && \
    mkdir -p /ppml/trusted-big-data-ml/work/password && \
    mkdir -p /ppml/trusted-big-data-ml/work/data && \
    mkdir -p /ppml/trusted-big-data-ml/work/models && \
    mkdir -p /ppml/trusted-big-data-ml/work/apps && \
    mkdir -p /ppml/trusted-big-data-ml/work/examples/bigdl && \
    mkdir -p /ppml/trusted-big-data-ml/examples/src/main && \
    mkdir -p /root/.keras/datasets && \
    mkdir -p /root/.zinc && \
    mkdir -p /root/.m2 && \
    mkdir -p /root/.kube/ && \
    mkdir -p /graphene/Pal/src/host/Linux-SGX/signer

COPY --from=graphene /graphene/Scripts /graphene/Scripts
COPY --from=graphene /graphene/Runtime/ /graphene/Runtime
COPY --from=graphene /graphene/python /graphene/python
COPY --from=graphene /graphene/Pal /graphene/Pal
COPY --from=graphene /graphene/Pal/src/host/Linux-SGX/generated_offsets.py /graphene/python/
COPY --from=graphene /graphene/Tools/argv_serializer /graphene/Tools
COPY --from=spark /opt/jdk  /opt/jdk8
COPY --from=spark /opt/scala-2.11.8  /opt/scala-2.11.8
COPY --from=spark /opt/spark-${SPARK_VERSION} /ppml/trusted-big-data-ml/work/spark-${SPARK_VERSION}
COPY --from=spark /opt/spark-${SPARK_VERSION}/examples/src/main/resources /ppml/trusted-big-data-ml/examples/src/main/resources
COPY --from=bigdl /bigdl-${BIGDL_VERSION} ${BIGDL_HOME}

RUN apt-get update --fix-missing && \
    env DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y tzdata && \
    apt-get install -y apt-utils vim curl nano wget unzip git tree zip && \
    apt-get install -y libsm6 make build-essential && \
    apt-get install -y autoconf gawk bison libcurl4-openssl-dev python3-protobuf libprotobuf-c-dev protobuf-c-compiler && \
    apt-get install -y netcat net-tools && \
    mkdir -p /ppml/trusted-big-data-ml/fl

COPY --from=bigdl /bigdl-${BIGDL_VERSION}/python/start-fl-server.py /ppml/trusted-big-data-ml/fl

#python
RUN apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install -y python3-minimal build-essential python3.7-distutils python3-apt python3.7 python3-setuptools python3-dev python3-pip libpython3.7 && \
    rm /usr/bin/python3 && \
    ln -s /usr/bin/python3.7 /usr/bin/python3 && \
    pip3 install --upgrade pip && \
    pip install setuptools==58.4.0 && \
    pip install --no-cache-dir numpy scipy && \
    pip install --no-cache-dir pandas && \
    pip install --no-cache-dir scikit-learn matplotlib seaborn jupyter wordcloud moviepy requests h5py opencv-python tensorflow==1.15 protobuf==3.19.0 && \
    pip install --no-cache-dir torch==1.8.1 torchvision==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    #Fix tornado await process
    pip uninstall -y -q tornado && \
    pip install --no-cache-dir tornado && \
    pip install --no-cache-dir filelock && \
    pip install --no-cache-dir tensorflow_datasets h5py==2.10.0 && \
    pip install --no-cache-dir pyarrow && \
    pip install --no-cache-dir ninja meson && \
    pip install --no-cache-dir psutil && \
    pip install --no-cache-dir dill==0.3.4 && \
    python3 -m pip install toml==0.10.2 click jinja2 && \
    python3 -m ipykernel.kernelspec && \
    rm -rf /usr/lib/python3/dist-packages/protobuf-3.6.1.egg-info && \
    rm -rf /usr/lib/python3/dist-packages/google/protobuf && \
    ln -s /usr/lib/x86_64-linux-gnu/libtinfo.so.6 /usr/lib/x86_64-linux-gnu/libtinfo.so.5 && \
    pip install --no-cache-dir pyyaml

ADD ./bash.manifest.template /ppml/trusted-big-data-ml/bash.manifest.template
ADD ./Makefile /ppml/trusted-big-data-ml/Makefile
ADD ./init.sh /ppml/trusted-big-data-ml/init.sh
ADD ./clean.sh /ppml/trusted-big-data-ml/clean.sh
ADD ./examples /ppml/trusted-big-data-ml/work/examples
ADD ./standalone/check-status.sh /ppml/trusted-big-data-ml/standalone/check-status.sh
ADD ./standalone/start-spark-standalone-master-sgx.sh /ppml/trusted-big-data-ml/standalone/start-spark-standalone-master-sgx.sh
ADD ./standalone/start-spark-standalone-worker-sgx.sh /ppml/trusted-big-data-ml/standalone/start-spark-standalone-worker-sgx.sh
ADD ./standalone/start-spark-standalone-driver-sgx.sh /ppml/trusted-big-data-ml/standalone/start-spark-standalone-driver-sgx.sh
ADD ./bigdl-ppml-submit.sh /ppml/trusted-big-data-ml/bigdl-ppml-submit.sh
ADD ./tracker.py ./tracker.py
ADD ./start-scripts /ppml/trusted-big-data-ml/work/start-scripts
ADD ./test-suites /ppml/trusted-big-data-ml/work/test-suites
ADD ./_dill.py.patch ./_dill.py.patch
ADD ./python-uuid.patch ./python-uuid.patch
ADD ./python-pslinux.patch ./python-pslinux.patch

RUN zip -u ${BIGDL_HOME}/jars/xgboost4j_2.12-1.1.2.jar ./tracker.py && \
    patch /usr/local/lib/python3.7/dist-packages/dill/_dill.py ./_dill.py.patch && \
    patch /usr/lib/python3.7/uuid.py ./python-uuid.patch && \
    patch /usr/local/lib/python3.7/dist-packages/psutil/_pslinux.py ./python-pslinux.patch && \
    wget -P /ppml/trusted-big-data-ml/work/lib https://sourceforge.net/projects/analytics-zoo/files/analytics-zoo-data/libhadoop.so && \
    cp /usr/lib/x86_64-linux-gnu/libpython3.7m.so.1 /usr/lib/libpython3.7m.so.1 && \
    sed -i 's/examples/\/ppml\/trusted-big-data-ml\/work\/spark-3.1.2\/examples/' /ppml/trusted-big-data-ml/work/spark-3.1.2/examples/src/main/python/sql/basic.py && \
    sed -i 's/examples/\/ppml\/trusted-big-data-ml\/work\/spark-3.1.2\/examples/' /ppml/trusted-big-data-ml/work/spark-3.1.2/examples/src/main/python/sql/hive.py && \
    sed -i 's/spark-warehouse/\/ppml\/trusted-big-data-ml\/work\/spark-warehouse/' /ppml/trusted-big-data-ml/work/spark-3.1.2/examples/src/main/python/sql/hive.py && \
    chmod a+x /ppml/trusted-big-data-ml/init.sh && \
    chmod a+x /ppml/trusted-big-data-ml/clean.sh && \
    chmod a+x /ppml/trusted-big-data-ml/standalone/* && \
    chmod a+x /ppml/trusted-big-data-ml/bigdl-ppml-submit.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/start-scripts/* && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/pyspark-e2e-example.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/pyspark-simple-examples.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/pyspark-sql-api-examples.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/pyspark-sql-examples.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/start-tpch.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/spark-examples.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/spark-sql-examples.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/spark-e2e-example.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/k8s-spark-pi.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/k8s-spark-sql-examples.sh && \
    chmod a+x /ppml/trusted-big-data-ml/work/test-suites/k8s-pyspark-sql-examples.sh

# kuberenetes support
ADD ./spark-executor-template.yaml /ppml/trusted-big-data-ml/spark-executor-template.yaml
ADD ./spark-driver-template.yaml /ppml/trusted-big-data-ml/spark-driver-template.yaml
ADD ./entrypoint.sh /opt/entrypoint.sh
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /sbin/tini
RUN rm $SPARK_HOME/jars/okhttp-*.jar && \
    wget -P $SPARK_HOME/jars https://repo1.maven.org/maven2/com/squareup/okhttp3/okhttp/3.8.0/okhttp-3.8.0.jar && \
    wget -P $SPARK_HOME/jars https://github.com/xerial/sqlite-jdbc/releases/download/3.36.0.1/sqlite-jdbc-3.36.0.1.jar && \
    chmod +x /opt/entrypoint.sh && \
    chmod +x /sbin/tini && \
    cp /sbin/tini /usr/bin/tini

# Azure support
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
ADD azure /ppml/trusted-big-data-ml/azure

WORKDIR /ppml/trusted-big-data-ml

ENTRYPOINT [ "/opt/entrypoint.sh" ]

