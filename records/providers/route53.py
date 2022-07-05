from typing import List

import boto3

from subdomains.models import Subdomain
from .base import BaseProvider
from ..types import Record


class Route53Provider(BaseProvider):
    def __init__(self):
        self.client = boto3.client('route53')

    def list_records(self, subdomain: Subdomain) -> List[Record]:
        response = self.client.list_resource_record_sets(
            HostedZoneId=subdomain.domain.records_provider_id,
        )
        resource_record_sets = response['ResourceRecordSets']
        return sum(list(map(lambda x: self.provider_record_object_to_record_objects(x),
                            filter(lambda x: str(x['Name']).endswith(subdomain.name), resource_record_sets))), [])

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        response = self.client.change_resource_record_sets(
            HostedZoneId=subdomain.domain.records_provider_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': self.record_object_to_provider_record_object(record)
                    },
                ]
            }
        )
        return record

    def retrieve_record(self, subdomain: Subdomain, id) -> Record:
        pass

    def update_record(self, subdomain: Subdomain, id, record: Record) -> Record:
        response = self.client.change_resource_record_sets(
            HostedZoneId=subdomain.domain.records_provider_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': self.record_object_to_provider_record_object(record)
                    },
                ]
            }
        )
        return record

    def delete_record(self, subdomain: Subdomain, id):
        pass

    def provider_record_object_to_record_objects(self, provider_record_object) -> List[Record]:
        name = provider_record_object['Name']
        ttl = provider_record_object['TTL']
        type = provider_record_object['Type']
        values = list(map(lambda x: x['Value'], provider_record_object['ResourceRecords']))
        records = []
        for value in values:
            records.append(Record(name, ttl, type, value))
        return records

    def record_object_to_provider_record_object(self, record_object: Record):
        return {
            'Name': record_object.name,
            'Type': record_object.type,
            'TTL': record_object.ttl,
            'ResourceRecords': [
                {
                    'Value': record_object.data
                },
            ],
        }
