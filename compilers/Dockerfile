FROM buildpack-deps:jammy

# C, C++, FORTRAN
ENV GCC_VERSION 10.3.0
RUN set -xe && \
    curl -fsSL "https://ftpmirror.gnu.org/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.gz" -o /tmp/gcc.tar.gz && \
    mkdir /tmp/gcc && \
    tar -xf /tmp/gcc.tar.gz -C /tmp/gcc --strip-components=1 && \
    rm /tmp/gcc.tar.gz && \
    cd /tmp/gcc && \
    ./contrib/download_prerequisites && \
    { rm *.tar.* || true; } && \
    cd $(mktemp -d) && \
    /tmp/gcc/configure -q --disable-multilib --enable-languages=c,c++,fortran --prefix=/usr/local/gcc && \
    make -j$(nproc) && \
    make -j$(nproc) install-strip && \
    rm -rf /tmp/*

LABEL version="1.0.0" maintainer="Ernest Wambua <ernestwambua2@gmail.com>"