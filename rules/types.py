class PageRule:
    id = None

    domain: str
    owner: str

    forwarding_protocol: str = None
    forwarding_domain: str = None
    forwarding_code: int = None
    forwarding_path: bool = None

    parking_title: str = None
    parking_content: str = None
