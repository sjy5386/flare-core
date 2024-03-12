import os
from typing import Any

import geoip2.webservice


class MaxMindGeoIpWebServicesClient:
    host = 'geolite.info'
    account_id = int(os.environ.get('MAXMIND_ACCOUNT_ID', 0))
    license_key = os.environ.get('MAXMIND_LICENSE_KEY')

    def lookup(self, ip_address: str) -> dict[str, Any]:
        with geoip2.webservice.Client(self.account_id, self.license_key, self.host) as client:
            response = client.city(ip_address)
            return {
                'ip_address': response.traits.ip_address or ip_address,
                'continent': response.continent.name,
                'country': response.country.name,
                'region': ', '.join(map(lambda x: x.name, response.subdivisions)),
                'city': response.city.name,
                'isp': response.traits.isp or response.traits.autonomous_system_organization,
            }
