# FoamAgent - Qt6 OpenFOAM GUI Container
# Use official OpenCFD OpenFOAM image as base
FROM opencfd/openfoam-default:latest

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Set display for GUI applications
ENV DISPLAY=:1
ENV VNC_PORT=5901
ENV NOVNC_PORT=6080
ENV VNC_RESOLUTION=1920x1080

# Install Qt6 and GUI dependencies on top of OpenFOAM image
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    cmake \
    git \
    wget \
    curl \
    pkg-config \
    ca-certificates \
    # Qt6 dependencies
    qt6-base-dev \
    qt6-base-dev-tools \
    qt6-tools-dev \
    qt6-tools-dev-tools \
    libqt6opengl6-dev \
    libqt6svg6-dev \
    libqt6charts6-dev \
    qml6-module-qtquick \
    qml6-module-qtquick-controls \
    # VNC and X11
    x11vnc \
    xvfb \
    xfce4 \
    xfce4-goodies \
    dbus-x11 \
    x11-xserver-utils \
    # noVNC for web access
    novnc \
    websockify \
    # Python for automation
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    # CAD and 3D visualization dependencies
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libxrender1 \
    libxcursor1 \
    libxft2 \
    libxinerama1 \
    # VTK dependencies for 3D visualization
    libvtk9-dev \
    python3-vtk9 \
    # OpenCASCADE dependencies for STEP/IGES support
    libocct-foundation-dev \
    libocct-modeling-data-dev \
    libocct-modeling-algorithms-dev \
    libocct-data-exchange-dev \
    libocct-visualization-dev \
    # libfive dependencies for F-Rep solid modeling
    libeigen3-dev \
    libpng-dev \
    libboost-all-dev \
    # STL and mesh processing
    meshlab \
    # Utilities
    supervisor \
    vim \
    nano \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# OpenFOAM is already installed in the base image

# Build and install libfive from source for F-Rep solid modeling
# libfive provides functional representations (F-Rep) as an alternative to boundary-reps
RUN cd /opt && \
    git clone https://github.com/libfive/libfive.git && \
    cd libfive && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local \
          -DCMAKE_BUILD_TYPE=Release \
          .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd /opt && \
    rm -rf libfive

# Set libfive environment
ENV LIBFIVE_INSTALL=/usr/local
ENV PATH=${LIBFIVE_INSTALL}/bin:${PATH}
ENV LD_LIBRARY_PATH=${LIBFIVE_INSTALL}/lib:${LD_LIBRARY_PATH}
ENV PYTHONPATH=${LIBFIVE_INSTALL}/lib/python3/dist-packages:${PYTHONPATH}

# TODO: Newton Dynamics - temporarily disabled due to build issues
# Will be re-enabled once build configuration is resolved
# For now, focusing on OpenFOAM only for initial testing

# TODO: Geant4 - temporarily disabled to speed up initial build/testing
# Will be re-enabled after OpenFOAM core is verified
# Install Geant4 v11.4.1
# RUN cd /opt && \
#     wget https://gitlab.cern.ch/geant4/geant4/-/archive/v11.4.1/geant4-v11.4.1.tar.gz && \
#     tar -xzf geant4-v11.4.1.tar.gz && \
#     rm geant4-v11.4.1.tar.gz && \
#     mkdir -p geant4-v11.4.1-build && \
#     cd geant4-v11.4.1-build && \
#     cmake -DCMAKE_INSTALL_PREFIX=/opt/geant4 \
#           -DGEANT4_INSTALL_DATA=ON \
#           -DGEANT4_USE_GDML=ON \
#           -DGEANT4_USE_OPENGL_X11=ON \
#           -DGEANT4_USE_QT=ON \
#           -DGEANT4_USE_XM=OFF \
#           -DGEANT4_USE_SYSTEM_EXPAT=ON \
#           -DGEANT4_BUILD_MULTITHREADED=ON \
#           ../geant4-v11.4.1 && \
#     make -j$(nproc) && \
#     make install && \
#     cd /opt && rm -rf geant4-v11.4.1 geant4-v11.4.1-build

# TODO: openEMS - temporarily disabled due to CSXCAD build issues
# Will be re-enabled once build configuration is resolved

# TODO: OpenSim - temporarily disabled to speed up initial build
# Will be re-enabled after core system is verified

# TODO: Geant4 environment - disabled until Geant4 is re-enabled
# Set Geant4 environment
# ENV G4INSTALL=/opt/geant4
# ENV PATH=${G4INSTALL}/bin:${PATH}
# ENV LD_LIBRARY_PATH=${G4INSTALL}/lib:${LD_LIBRARY_PATH}

# Source Geant4 environment in bashrc
# RUN echo "source /opt/geant4/bin/geant4.sh" >> /root/.bashrc

# Install Python dependencies for CAD, AI, and visualization
COPY docker/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Create Python utilities directory
RUN mkdir -p /app/python

# Create application directory
WORKDIR /app

# Copy application source
COPY src/ /app/src/
COPY ui/ /app/ui/
COPY resources/ /app/resources/
COPY python/ /app/python/
COPY CMakeLists.txt /app/

# Build Qt6 application
RUN mkdir -p /app/build && cd /app/build && \
    cmake .. && \
    make -j$(nproc)

# Setup XFCE for the desktop environment
RUN mkdir -p /root/.vnc

# Create xstartup for the desktop session
RUN echo '#!/bin/bash\n\
unset SESSION_MANAGER\n\
unset DBUS_SESSION_BUS_ADDRESS\n\
startxfce4 &\n\
' > /root/.vnc/xstartup && chmod +x /root/.vnc/xstartup

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy startup scripts
COPY docker/scripts/ /usr/local/bin/

# Expose ports
EXPOSE 5901 6080

# Create volume mount points
VOLUME ["/work"]

# Start supervisor to manage all services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
