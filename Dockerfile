FROM lidejia/ubuntu:16.04

ENV WORK_DIR="/home/${RUNTIME_ACCOUNT}"/psn-discount \
    GIT_USERNAME="Dejia Li" \
    GIT_EMAIL="lidejiasw@gmail.com"

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    # locale
    locale-gen zh_HK.UTF-8 && \
    locale-gen ja_JP.UTF-8 && \
    # python
    apt-get install -y python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev && \
    su -l ${RUNTIME_ACCOUNT} -c "pip3 install scrapy jinja2" && \
    # git
    apt-get install -y git && \
    su -l ${RUNTIME_ACCOUNT} -c "git config --global user.name '${GIT_USERNAME}' && \
                                 git config --global user.email '${GIT_EMAIL}' && \
                                 git config --global push.default simple" && \
    # crontab
    apt-get install -y cron && \
    # cleanup
    apt-get clean


ADD ./ ${WORK_DIR}
RUN chown -R ${RUNTIME_ACCOUNT}: ${WORK_DIR} && \
    crontab -u ${RUNTIME_ACCOUNT} ${WORK_DIR}/Crontab/psn.crontab

WORKDIR ${WORK_DIR}
ENTRYPOINT ["/usr/sbin/cron", "-f"]
