from typing import Any, Dict, List, Optional


class BaseRecordProvider:
    def list_records(self, subdomain_name: str) -> List[Dict[str, Any]]:
        pass

    def create_record(self, subdomain_name: str, **kwargs) -> Dict[str, Any]:
        pass

    def retrieve_record(self, subdomain_name: str, provider_id: str) -> Optional[Dict[str, Any]]:
        pass

    def update_record(self, subdomain_name: str, provider_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        pass

    def delete_record(self, subdomain_name: str, provider_id: str) -> None:
        pass
