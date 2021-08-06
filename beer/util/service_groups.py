from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "beer_harvester beer_timelord_launcher beer_timelord beer_farmer beer_full_node beer_wallet".split(),
    "node": "beer_full_node".split(),
    "harvester": "beer_harvester".split(),
    "farmer": "beer_harvester beer_farmer beer_full_node beer_wallet".split(),
    "farmer-no-wallet": "beer_harvester beer_farmer beer_full_node".split(),
    "farmer-only": "beer_farmer".split(),
    "timelord": "beer_timelord_launcher beer_timelord beer_full_node".split(),
    "timelord-only": "beer_timelord".split(),
    "timelord-launcher-only": "beer_timelord_launcher".split(),
    "wallet": "beer_wallet beer_full_node".split(),
    "wallet-only": "beer_wallet".split(),
    "introducer": "beer_introducer".split(),
    "simulator": "beer_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
