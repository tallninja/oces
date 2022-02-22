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

# Check for latest version here: https://nodejs.org/en
ENV NODE_VERSION 17.5.0

# Node.js and npm
RUN ARCH= && dpkgArch="$(dpkg --print-architecture)" \
    && case "${dpkgArch##*-}" in \
    amd64) ARCH='x64';; \
    ppc64el) ARCH='ppc64le';; \
    s390x) ARCH='s390x';; \
    arm64) ARCH='arm64';; \
    armhf) ARCH='armv7l';; \
    i386) ARCH='x86';; \
    *) echo "unsupported architecture"; exit 1 ;; \
    esac \
    # gpg keys listed at https://github.com/nodejs/node#release-keys
    && set -ex \
    && for key in \
    4ED778F539E3634C779C87C6D7062848A1AB005C \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    74F12602B6F1C4E913FAA37AD3A89613643B6201 \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
    C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    A48C2BEE680E841632CD4E44F07496B3EB3C1762 \
    108F52B48DB57BB0CC439B2997B01419BD92F80A \
    B9E2F5981AA6E0CD28160D9FF13993A75599653C \
    ; do \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$key" || \
    gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key" ; \
    done \
    && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
    && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
    && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
    && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs \
    # smoke tests
    && node --version \
    && npm --version


LABEL version="1.1.0" maintainer="Ernest Wambua <ernestwambua2@gmail.com>"














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