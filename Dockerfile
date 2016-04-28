# python 2.7 image
FROM python:2.7

# proxy config if necessary
#ENV http_proxy http://proxy:8080
#ENV https_proxy https://proxy:8080


# install linux packages
RUN apt-get update  \
    && apt-get install -y figlet cowsay fortune-mod fortunes fortunes-mario fortunes-off fortunes-bofh-excuses fortunes-de fortunes-debian-hints

# install python requirements
COPY requirements.txt /
RUN pip2 install -r /requirements.txt

# copy application files
COPY plugins /plugins
COPY bot.py /
COPY slackbot_settings.py /

# adjust the PATH variable for fortune and figlet
ENV PATH /usr/games:$PATH

# start bot
CMD python /bot.py
