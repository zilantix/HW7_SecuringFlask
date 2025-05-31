import json
from ruamel.yaml import YAML

# -----------------------
# Step 1: Generate local daemon.json
# -----------------------
daemon_config = {
    "live-restore": True,
    "userns-remap": "default",
    "no-new-privileges": True,
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    },
    "userland-proxy": False
}

daemon_path = "daemon.json"
with open(daemon_path, "w") as f:
    json.dump(daemon_config, f, indent=4)
print(f"[+] Local {daemon_path} created with hardening config.")

# -----------------------
# Step 2: Update Dockerfile
# -----------------------
dockerfile_path = "Dockerfile"
with open(dockerfile_path, "r") as f:
    lines = f.readlines()

updated = False
if not any("HEALTHCHECK" in line for line in lines):
    lines.append('\nHEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1\n')
    print("[+] HEALTHCHECK added to Dockerfile.")
    updated = True

if not any("USER appuser" in line for line in lines):
    lines.append("USER appuser\n")
    print("[+] USER appuser added to Dockerfile.")
    updated = True

if updated:
    with open(dockerfile_path, "w") as f:
        f.writelines(lines)

# -----------------------
# Step 3: Inject limits in docker-compose.yml
# -----------------------
compose_path = "docker-compose.yml"
yaml = YAML()
yaml.preserve_quotes = True

with open(compose_path, "r") as f:
    compose_data = yaml.load(f)

# Target the 'web' service
web = compose_data['services'].get('web', {})
deploy = web.setdefault('deploy', {})
resources = deploy.setdefault('resources', {})
limits = resources.setdefault('limits', {})

# Apply limits
limits['memory'] = '512m'
limits['cpus'] = '0.5'

# Apply restart policy if desired
web.setdefault('restart', 'on-failure:5')

with open(compose_path, "w") as f:
    yaml.dump(compose_data, f)

print("[+] docker-compose.yml updated with resource limits and restart policy.")

print("\n Local Docker hardening completed. To apply daemon.json to Docker daemon, manually copy it to /etc/docker with sudo if desired.")

