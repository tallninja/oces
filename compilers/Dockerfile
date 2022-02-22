FROM buildpack-deps:jammy

# C, C++, FORTRAN
ENV GCC_VERSION 10.3.0

# update apt repository
RUN apt-get update

# C
RUN apt-get install -y gcc

# C++
RUN apt-get install -y g++

# Fortran
RUN apt-get install -y gfortran

# isolate - create sandbox in order to run untrusted user programs
RUN set -xe && \
    apt-get install -y --no-install-recommends git libcap-dev && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/tallninja/isolate.git /tmp/isolate && \
    cd /tmp/isolate && \
    git checkout b30dad4f967952bc9fa144b8b05aadf29f3411dc && \
    make -j$(nproc) install && \
    rm -rf /tmp/*
ENV BOX_ROOT /var/local/lib/isolate

LABEL version="1.0.0" maintainer="Ernest Wambua <ernestwambua2@gmail.com>"














# RUN set -xe && \
#     curl -fsSL "https://ftpmirror.gnu.org/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.gz" -o /tmp/gcc.tar.gz && \
#     mkdir /tmp/gcc && \
#     tar -xf /tmp/gcc.tar.gz -C /tmp/gcc --strip-components=1 && \
#     rm /tmp/gcc.tar.gz && \
#     cd /tmp/gcc && \
#     ./contrib/download_prerequisites && \
#     { rm *.tar.* || true; } && \
#     cd $(mktemp -d) && \
#     /tmp/gcc/configure -q --disable-multilib --enable-languages=c,c++,fortran --prefix=/usr/local/gcc && \
#     make -j$(nproc) && \
#     make -j$(nproc) install-strip && \
#     rm -rf /tmp/*