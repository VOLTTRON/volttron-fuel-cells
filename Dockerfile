FROM volttron/volttron
# /volttron

ENV CONFIG ${VOLTTRON_USER_HOME}/configs
COPY ./platform_config.yml /platform_config.yml
RUN pwd

# There are three env variables set in volttron_base image
# VOLTTRON_ROOT (the cloned directory of volttron [/code])
# VOLTTRON_USER (the user the volttron instance is running under)
# VOLTTRON_USER_HOME (defaults to /home/volttron)
# VOLTTRON_HOME (the home of volttron)

# now we need to setup so we are always in the volttron python context
RUN echo "source /code/volttron/env/bin/activate">/home/${VOLTTRON_USER}/.bashrc

WORKDIR ${VOLTTRON_USER_HOME}

COPY ./configs ${CONFIG}

EXPOSE 22916
