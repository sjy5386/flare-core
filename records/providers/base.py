from abc import ABCMeta, abstractmethod
from typing import Any

from domains.models import Domain


class BaseDnsRecordProvider(metaclass=ABCMeta):
    @abstractmethod
    def list_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        pass

    @abstractmethod
    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        pass

    @abstractmethod
    def get_nameservers(self, domain: Domain = None) -> list[str]:
        pass
