FROM debian:latest

RUN apt-get -y -q update; \
    apt-get -y -q install apache2 mercurial

RUN echo "[ui]" > /root/.hgrc \
    && echo "username = Podalirius" >> /root/.hgrc

# https://www.mercurial-scm.org/
RUN cd /var/www/html/; hg init
RUN cd /var/www/html/; echo "Init" > README.md && hg add README.md && hg commit -m 'Init'
RUN cd /var/www/html/; mkdir poc; echo "Lorem ipsum" > poc/ThisIsATest.md && hg add poc/ThisIsATest.md && hg commit -m 'Added poc/ThisIsATest.md'
RUN cd /var/www/html/; tar czvf archive.tar.gz poc/ && hg add archive.tar.gz && hg commit -m 'Added archive.tar.gz'
RUN cd /var/www/html/; rm poc/ThisIsATest.md && hg rm poc/ThisIsATest.md && hg commit -m 'Removed poc/ThisIsATest.md'
RUN cd /var/www/html/; echo "Changed" > README.md && hg add README.md && hg commit -m 'Changed'

RUN chown www-data: -R /var/www/

RUN echo "#!/bin/bash" > /entrypoint.sh ;\
    echo "apachectl -D FOREGROUND" >> /entrypoint.sh ;\
    chmod +x /entrypoint.sh

EXPOSE 80

CMD /entrypoint.sh
