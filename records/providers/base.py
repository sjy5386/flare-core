from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional

from domains.models import Domain


class BaseRecordProvider(metaclass=ABCMeta):
    @abstractmethod
    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs
                      ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        pass

    @abstractmethod
    def get_nameservers(self, domain: Domain) -> List[str]:
        pass
