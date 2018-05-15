import subprocess
import os
import sys
import yaml
from time import sleep

sys.stdout.write(str(os.environ))

# The environment variables must be set or we ahve big issues
VOLTTRON_ROOT = os.environ['VOLTTRON_ROOT']
VOLTTRON_HOME = os.environ['VOLTTRON_HOME']
VOLTTRON_PATH = "{}/env/bin/volttron".format(VOLTTRON_ROOT)
VOLTTRON_CTL = "{}/env/bin/volttron-ctl".format(VOLTTRON_ROOT)
INSTALL_PATH = "{}/scripts/install-agent.py".format(VOLTTRON_ROOT)
KEYSTORES = os.path.join(VOLTTRON_HOME, "keystores")

with open("platform_config.yml") as cin:
    config = yaml.safe_load(cin)
    agents = config['agents']

need_to_install = {}
for identity, specs in agents.items():
    path_to_keystore = os.path.join(KEYSTORES, identity)
    if not os.path.exists(path_to_keystore):
        need_to_install[identity] = specs

# if we need to do installs then we haven't setup this at all.
if need_to_install:
    assert os.path.exists(VOLTTRON_PATH)
    proc = subprocess.Popen([VOLTTRON_PATH, "-vv"])
    assert proc is not None
    sleep(5)
    with open(os.path.join(VOLTTRON_HOME, "config"), "w") as fout:
        fout.write("[volttron]\n")
        fout.write("vip-address=tcp://0.0.0.0:22916\n")

    config_dir = os.path.join("configs")
    for identity, spec in need_to_install.items():
        agent_cfg = None
        if "config" in spec:
            agent_cfg = os.path.join(config_dir, spec["config"])

        agent_source = os.path.expandvars(os.path.expanduser(spec['source']))

        install_cmd = ["python", INSTALL_PATH]
        install_cmd.extend(["--agent-source", agent_source])
        install_cmd.extend(["--vip-identity", identity])
        install_cmd.extend(["--start", "--priority", "50"])
        install_cmd.extend(["--agent-start-time", "2"])
        if agent_cfg:
            install_cmd.extend(["--config", agent_cfg])

        subprocess.check_call(install_cmd)

        if "config_store" in spec:
            for key, entry in spec['config_store'].items():
                entry_file = os.path.expandvars(os.path.expanduser(entry['file']))
                entry_cmd = [VOLTTRON_CTL, "config", "store", identity, key, entry_file]
                if "type" in entry:
                    entry_cmd.append(entry['type'])

                subprocess.check_call(entry_cmd)

# _cmd(['volttron-ctl', 'config', 'store', PLATFORM_DRIVER,
#               'fake.csv', 'examples/configurations/drivers/fake.csv', '--csv'])
#         _cmd(['volttron-ctl', 'config', 'store', PLATFORM_DRIVER,
#               'devices/fake-campus/fake-building/fake-device',
#               'examples/configurations/drivers/fake.config'])






    subprocess.call(["vctl", "shutdown", "--platform"])

    sleep(5)
    sys.exit(0)
