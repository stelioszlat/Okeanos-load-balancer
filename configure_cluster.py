from kamaki.clients.astakos import AstakosClient
from kamaki.clients.cyclades import CycladesComputeClient
from configure_nginx import *


def CONFIGURE_CLUSTER_REMOVE(hostname, config_file):
    remove_server(hostname, config_file)


def CONFIGURE_CLUSTER_ADD(hostname, config_file):
    add_server(hostname, config_file)


def ADD_VM(url, token, name, project):

    #  create a new vm

    astakos = AstakosClient(url, token, name)

    service_type = CycladesComputeClient.service_type
    endpoint = astakos.get_endpoint_url(service_type)
    compute = CycladesComputeClient(endpoint, token)

    vm_name = name
    flavor = '260'
    image = 'eca2f4ef-b428-4096-a47d-29ddf5ed68d9'

    # server = compute.create_server(name=vm_name, flavor_id=flavor, image_id=image)

    server = compute.create_server(name=vm_name, key_name='cluster key', flavor_id=flavor, image_id=image, project_id=project)
    print(server['status'])

    with open(vm_name+'.info', "w") as f:
        for s in server:
            f.write(s)

    active = compute.wait_server_until(server['id'], 'ACTIVE')
    if active != 'ACTIVE':
        print('Waiting for server to build...')


def REMOVE_VM(url, token, server):

    astakos = AstakosClient(url, token)
    service_type = CycladesComputeClient.service_type
    endpoint = astakos.get_endpoint_url(service_type)
    compute = CycladesComputeClient(endpoint, token)

    # find server id
    s = compute.list_servers(name=server)
    for i in s:
        if i['name'] == server:
            id = i['id']
            print(id)
            compute.delete_server(id)
