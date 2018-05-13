FROM volttron/volttron

# There are three env variables set in volttron_base image
# VOLTTRON_ROOT (the cloned directory of volttron)
# VOLTTRON_USER (the user the volttron instance is running under)
# VOLTTRON_HOME (the home of volttron)

# now we need to setup so we are always in the volttron python context
RUN echo "source /code/volttron/env/bin/activate">/home/${VOLTTRON_USER}/.bashrc
COPY --chown=volttron . $VOLTTRON_ROOT
RUN chmod +x bootstart.sh

RUN mkdir -p /home/${VOLTTRON_USER}
RUN chown volttron.volttron -R /home/volttron
WORKDIR /home/volttron
# COPY Prices.csv $HOME/Prices.csv
# COPY Weather.csv $HOME/Weather.csv
# COPY setup-platform.py $HOME/setup-platform.py
# COPY agents.yml $HOME/agents.yml
#ENTRYPOINT [ "python", "setup-platform.py" ]
EXPOSE 22916

CMD ["/bin/bash"]
#CMD ["./bootstart.sh"] 


