# fuel-cells example

This is a working example of how to use the volttron/volttron docker image in a VOLTTRON deployment.  See https://github.com/VOLTTRON/volttron-docker for more information on the base image.

## Quick start

1. Clone this repository git clone https://github.com/VOLTTRON/volttron-fuel-cells
1. Modify platform_config.yml to adjust agents for installation
1. execute docker-compose up

## Platform configuration

```` yaml
# Properties to be added to the root config file
# the properties should be ingestable for volttron
# the values will be presented in the config file
# as key=value
config:
  vip-address: tcp://0.0.0.0:22916
  bind-web-address: http://0.0.0.0:8080
  # volttron-central-address: a different address
  # volttron-central-serverkey: a different key

# Agents dictionary to install.  The key must be a valid
# identity for the agent to be installed correctly.
agents:

  # Each agent identity.config file should be in the configs
  # directory and will be used to install the agent.
  listener:
    source: $VOLTTRON_ROOT/examples/ListenerAgent
    config: $CONFIG/listener.config

  platform.actuator:
    source: $VOLTTRON_ROOT/services/core/ActuatorAgent

  historian:
    source: $VOLTTRON_ROOT/services/core/SQLHistorian
    config: $CONFIG/historian.config

  weather:
    source: $VOLTTRON_ROOT/examples/DataPublisher
    config: $CONFIG/weather.config

  price:
    source: $VOLTTRON_ROOT/examples/DataPublisher
    config: $CONFIG/price.config

  platform.driver:
    source: $VOLTTRON_ROOT/services/core/MasterDriverAgent
    config_store:
      fake.csv:
        file: $VOLTTRON_ROOT/examples/configurations/drivers/fake.csv
        type: --csv
      devices/fake-campus/fake-building/fake-device:
        file: $VOLTTRON_ROOT/examples/configurations/drivers/fake.config
````
