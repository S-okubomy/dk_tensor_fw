FROM ubuntu:18.04

WORKDIR /dk_tensor_fw/app_tensor
COPY requirements.txt /dk_tensor_fw/app_tensor

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends locales curl python3-distutils vim ca-certificates \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt --no-cache-dir

ENV LANG en_US.utf8

CMD ["gunicorn", "webQueApiRunServer:app", "-b", "0.0.0.0:7010"]
