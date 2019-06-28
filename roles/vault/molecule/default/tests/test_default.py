import pytest
import os
import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleDefaults():
    with open("../../defaults/main.yml", 'r') as stream:
        return yaml.load(stream)


@pytest.mark.parametrize("dirs", [
    "/etc/vault.d",
    "/usr/local/lib/vault/plugins",
    "/var/vault",
    "/var/log/vault",
    "/var/run/vault",
    "/home/vault"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/vault.d/vault_main.hcl",
    "/lib/systemd/system/vault.service",
    "/usr/local/bin/vault"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_user(host):
    # assert host.group("vault").exists
    assert host.user("vault").exists


def test_service(host):
    s = host.service("vault")
    assert s.is_enabled
    assert s.is_running


def test_socket(host, AnsibleDefaults):
    vault_port = AnsibleDefaults['vault_port']
    s = host.socket("tcp://0.0.0.0:" + str(vault_port))
    assert s.is_listening


def test_version(host, AnsibleDefaults):
    version = os.getenv('VAULT', AnsibleDefaults['vault_version'])
    out = host.run("/usr/local/bin/vault --version").stdout
    assert "Vault v" + version in out
