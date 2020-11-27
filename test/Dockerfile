FROM debian:10-slim

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential git libasound2-dev libssl-dev libv4l-dev  \
    libsdl2-dev libsdl2-gfx-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-net-dev libsdl2-ttf-dev libx264-dev \
    libavformat-dev libavcodec-dev libavdevice-dev libavfilter-dev libavresample-dev libavutil-dev              \
    libavcodec-extra libopus-dev libopencore-amrwb-dev libopencore-amrnb-dev libvo-amrwbenc-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils iputils-ping net-tools python python-pip   \
    python-dev tcpdump

RUN groupadd -g 1000 behave
RUN useradd -m -g behave -u 1000 behave
USER behave

WORKDIR /home/behave
RUN pip install --user behave
RUN pip install --user PyHamcrest

RUN git clone https://github.com/pjsip/pjproject.git /home/behave/src/pjproject

WORKDIR /home/behave/src/pjproject
RUN ./configure --prefix=/home/behave --enable-shared
RUN make dep
RUN make
RUN make install

WORKDIR /home/behave/src/pjproject/pjsip-apps/src/python
RUN python setup.py build
RUN python setup.py install --home=/home/behave

WORKDIR /home/behave

ENV LD_LIBRARY_PATH /home/behave/lib
ENV PYTHONPATH /home/behave/lib/python
ENV PATH /home/behave/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

VOLUME /home/behave/features
CMD behave features/
