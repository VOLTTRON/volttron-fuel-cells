import subprocess
import os
import sys
import yaml
from time import sleep

sys.stdout.write(str(os.environ))

VOLTTRON_HOME = os.environ.get('VOLTTRON_HOME', "/home/volttron/.volttron")
KEYSTORES = os.path.join(VOLTTRON_HOME, "keystores")

with open("agents.yml") as cin:
    agents = yaml.safe_load(cin)

need_to_install = {}
for identity, specs in agents.items():
    path_to_keystore = os.path.join(KEYSTORES, identity)
    if not os.path.exists(path_to_keystore):
        need_to_install[identity] = specs

# if we need to do installs then we haven't setup this at all.
if need_to_install:
    proc = subprocess.Popen(["volttron", "-vv"])
    assert proc is not None
    sleep(5)
    with open(os.path.join(VOLTTRON_HOME, "config"), "w") as fout:
        fout.write("[volttron]\n")
        fout.write("vip-address=tcp://0.0.0.0:22916\n")

    config_dir = os.path.join("configs")
    for identity, spec in need_to_install.items():
        agent_cfg = os.path.join(config_dir, spec["config"])

        assert os.path.exists(agent_cfg)
        install_cmd = ["python", "scripts/install-agent.py"]
        install_cmd.extend(["--agent-source", spec["source"]])
        install_cmd.extend(["--vip-identity", identity])
        install_cmd.extend(["--start", "--priority", "50"])
        install_cmd.extend(["--agent-start-time", "2"])
        install_cmd.extend(["--config", agent_cfg])

        subprocess.check_call(install_cmd)

    subprocess.call(["vctl", "shutdown", "--platform"])

    sleep(5)
    sys.exit(0)
