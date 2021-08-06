import pathlib
from typing import Dict

from beer.consensus.constants import ConsensusConstants
from beer.consensus.default_constants import DEFAULT_CONSTANTS
from beer.harvester.harvester import Harvester
from beer.harvester.harvester_api import HarvesterAPI
from beer.rpc.harvester_rpc_api import HarvesterRpcApi
from beer.server.outbound_message import NodeType
from beer.server.start_service import run_service
from beer.types.peer_info import PeerInfo
from beer.util.config import load_config_cli
from beer.util.default_root import DEFAULT_ROOT_PATH

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "harvester"


def service_kwargs_for_harvester(
    root_path: pathlib.Path,
    config: Dict,
    consensus_constants: ConsensusConstants,
) -> Dict:
    connect_peers = [PeerInfo(config["farmer_peer"]["host"], config["farmer_peer"]["port"])]
    overrides = config["network_overrides"]["constants"][config["selected_network"]]
    updated_constants = consensus_constants.replace_str_to_bytes(**overrides)

    harvester = Harvester(root_path, config, updated_constants)
    peer_api = HarvesterAPI(harvester)
    network_id = config["selected_network"]
    kwargs = dict(
        root_path=root_path,
        node=harvester,
        peer_api=peer_api,
        node_type=NodeType.HARVESTER,
        advertised_port=config["port"],
        service_name=SERVICE_NAME,
        server_listen_ports=[config["port"]],
        connect_peers=connect_peers,
        auth_connect_peers=True,
        network_id=network_id,
    )
    if config["start_rpc_server"]:
        kwargs["rpc_info"] = (HarvesterRpcApi, config["rpc_port"])
    return kwargs


def main() -> None:
    config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    kwargs = service_kwargs_for_harvester(DEFAULT_ROOT_PATH, config, DEFAULT_CONSTANTS)
    return run_service(**kwargs)


if __name__ == "__main__":
    main()
