"""Analysis tool for finding dependencies between microservices"""
import re
from typing import Dict, List, Set, Tuple
import pprint

from kubernetes import client, config # type: ignore
from scapy.sendrecv import sniff # type: ignore
from scapy.arch import get_if_list # type: ignore
from graphviz import Digraph # type: ignore

IMAGE_TYPES = {
    'database': re.compile(r'^(mongo|mysql|redis|mcr\.microsoft\.com/mssql).*$'),
    'broker': re.compile(r'^(rabbitmq|kafka).*$'),
}

PORT_TYPES = {
    'database': set((27017,3306)),
}

def _get_service_type(images : Set[str], ports : Set[int]):
    service_type = 'service'
    for image_name in images:
        # look for an image name match
        for key, regex in IMAGE_TYPES.items():
            if regex.match(image_name):
                service_type = key
    if service_type == 'service':
        # no image match found, try port #
        for key, value in PORT_TYPES.items():
            if value & ports:
                service_type = key
    return service_type


def get_k8s_services(namespace : str='default'):
    """Determine k8s services, service type, and IP mappings"""
    config.load_kube_config()
    k8s = client.CoreV1Api()
    ip_name = {}
    service_ip = set()
    service_types = {}
    # Populate Services e.g. ts-user-mongo
    ret = k8s.list_namespaced_service(namespace)
    for service in ret.items:
        if service.metadata.name == 'kubernetes':
            continue
        service_ip.add(service.spec.cluster_ip)
        ip_name[service.spec.cluster_ip] = service.metadata.name
        endpoints = k8s.read_namespaced_endpoints(service.metadata.name, namespace)
        ports = set({port.target_port for port in service.spec.ports})
        images = set()
        for address in endpoints.subsets[0].addresses:
            ip_name[address.ip] = service.metadata.name
            pod = k8s.read_namespaced_pod(address.target_ref.name, namespace)
            images |= {container.image for container in pod.spec.containers}
        service_types[service.metadata.name] = _get_service_type(images, ports)
    return ip_name, service_ip, service_types


def capture_traffic(ip_name : Dict, service_ip : Dict):
    """Capture traffic on network, return graph vertices & edges"""
    vertices = set()
    edges = set()
    def handle_frame(frame):
        packet = frame["IP"]
        source_name = ip_name.get(packet.src, 'Unknown')
        dest_name = ip_name.get(packet.dst, 'Unknown')
        if source_name not in ('Unknown', 'kubernetes') and \
            dest_name not in ('Unknown', 'kubernetes'):
            if packet.dst in service_ip:
                vertices.add(source_name)
                vertices.add(dest_name)
                edges.add((source_name, dest_name))
                print(packet.src, source_name, packet.dst, dest_name)
    # get calico interfaces
    ifaces = [i for i in get_if_list() if i.startswith('cali')]
    # monitor traffic
    try:
        sniff(filter="tcp", iface=ifaces, prn=handle_frame)
    except KeyboardInterrupt:
        print("Exiting...")
    return vertices, edges


def output_graph(edges : List[Tuple[str,str]]):
    """Use GraphViz to render the graph"""
    dot = Digraph(format='png', strict=True)
    for src,dst in edges:
        dot.edge(src,dst)
    dot.render()


def output_csv(vertices : List[str], edges : List[str], service_types : Dict[str,str]):
    """Dump the vertices & edges to CSV files"""
    print("id,type")
    for vertex in vertices:
        print(vertex+','+service_types[vertex])
    print("from,to")
    for edge in edges:
        print(edge[0]+','+edge[1])


def main():
    """Main Program"""
    ip_name, service_ip, service_types = get_k8s_services()
    print("\nServices:")
    pprint.pprint(ip_name)
    pprint.pprint(service_types)

    vertices, edges = capture_traffic(ip_name, service_ip)
    output_graph(edges)
    output_csv(vertices, edges, service_types)


if __name__ == "__main__":
    main()
