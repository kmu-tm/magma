# Copyright 2023 The Magma Authors.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
ARG CPU_ARCH=x86_64
ARG DEB_PORT=amd64
ARG OS_DIST=ubuntu
ARG OS_RELEASE=focal

FROM $OS_DIST:$OS_RELEASE as base
ARG CPU_ARCH
ARG DEB_PORT
ARG OS_DIST
ARG OS_RELEASE

# Add the magma apt repo
RUN apt-get update && \
    apt-get install -y apt-utils software-properties-common apt-transport-https

# Add the magma apt repo
COPY keys/linux_foundation_registry_key.asc /etc/apt/trusted.gpg.d/magma.asc
RUN add-apt-repository "deb https://linuxfoundation.jfrog.io/artifactory/magma-packages-test focal-ci main"

# Install the runtime deps.
RUN apt-get update && apt-get install -y \
    bzr \
    curl \
    daemontools \
    gcc \
    git \
    libc-ares-dev \
    libev-dev \
    libevent-dev \
    libffi-dev \
    libjansson-dev \
    libjemalloc-dev \
    libssl-dev \
    libsystemd-dev \
    nghttp2 \
    make \
    net-tools \
    pkg-config \
    python-cffi \
    python3-pip \
    redis-server \
    rsyslog \
    sudo \
    unzip \
    vim \
    virtualenv \
    protobuf-compiler \
    libprotoc-dev

# Golang
WORKDIR /usr/local
ARG GOLANG_VERSION="1.21.1"
RUN GO_TARBALL="go${GOLANG_VERSION}.linux-${DEB_PORT}.tar.gz" \
 && curl https://go.dev/dl/${GO_TARBALL} --remote-name --location \
 && tar -xzf ${GO_TARBALL} \
 && ln -s /usr/local/go/bin/go /usr/local/bin/go \
 && rm ${GO_TARBALL}

ENV GOBIN /var/opt/magma/bin
ENV MAGMA_ROOT /magma
ENV PIP_CACHE_HOME ~/.pipcache
ENV PYTHON_BUILD /build/python
ENV PATH ${PYTHON_BUILD}/bin:${PATH}:${GOBIN}
ENV GO111MODULE on
# Use public go modules proxy
ENV GOPROXY https://proxy.golang.org

RUN printenv > /etc/environment


# Copy just the go.mod and go.sum files to download the golang deps.
# This step allows us to cache the downloads, and prevents reaching out to
# the internet unless any of the go.mod or go.sum files are changed.
COPY cwf/cloud/go/go.* $MAGMA_ROOT/cwf/cloud/go/
COPY cwf/gateway/go.* $MAGMA_ROOT/cwf/gateway/
COPY lte/cloud/go/go.* $MAGMA_ROOT/lte/cloud/go/
COPY feg/cloud/go/go.* $MAGMA_ROOT/feg/cloud/go/
COPY feg/cloud/go/protos/go.* $MAGMA_ROOT/feg/cloud/go/protos/
COPY feg/radius/lib/go/ $MAGMA_ROOT/feg/radius/lib/go/
COPY feg/radius/src/go.* $MAGMA_ROOT/feg/radius/src/
COPY feg/gateway/go.* $MAGMA_ROOT/feg/gateway/
COPY orc8r/lib/go/go.* $MAGMA_ROOT/orc8r/lib/go/
COPY orc8r/lib/go/protos/go.* $MAGMA_ROOT/orc8r/lib/go/protos/
COPY orc8r/cloud/go/go.* $MAGMA_ROOT/orc8r/cloud/go/
COPY orc8r/gateway/go/go.* $MAGMA_ROOT/orc8r/gateway/go/
WORKDIR $MAGMA_ROOT/cwf/gateway
RUN go mod download
# Install protoc-gen-go
RUN go install github.com/golang/protobuf/protoc-gen-go

# Symlink python scripts.
RUN ln -s /build/python/bin/generate_service_config.py /usr/local/bin/generate_service_config.py
RUN ln -s /build/python/bin/generate_nghttpx_config.py /usr/local/bin/generate_nghttpx_config.py

# -----------------------------------------------------------------------------
# Builder image with binary
# -----------------------------------------------------------------------------
FROM base as builder

# Build the code.
COPY cwf $MAGMA_ROOT/cwf
COPY feg $MAGMA_ROOT/feg
COPY lte/cloud $MAGMA_ROOT/lte/cloud
COPY orc8r/lib/go $MAGMA_ROOT/orc8r/lib/go
COPY orc8r/cloud $MAGMA_ROOT/orc8r/cloud
COPY orc8r/gateway/go $MAGMA_ROOT/orc8r/gateway/go

# Enable make gen if proto gen is required
# RUN make -C $MAGMA_ROOT/cwf/gateway gen
RUN make -C $MAGMA_ROOT/cwf/gateway build

# -----------------------------------------------------------------------------
# Production image
# -----------------------------------------------------------------------------
FROM $OS_DIST:$OS_RELEASE AS cwag_go
ARG CPU_ARCH
ARG DEB_PORT
ARG OS_DIST
ARG OS_RELEASE

# Install envdir.
RUN apt-get -y update && apt-get -y install daemontools curl arping

# Copy the build artifacts.
COPY --from=builder /var/opt/magma/bin /var/opt/magma/bin

# Copy the configs.
COPY cwf/gateway/configs /etc/magma

# Create empty envdir directory
RUN mkdir -p /var/opt/magma/envdir

RUN mkdir -p /var/opt/magma/configs
