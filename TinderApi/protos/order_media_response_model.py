# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: order_media_response_model.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass
class OrderMediaResponseModel(betterproto.Message):
    succeeded: bool = betterproto.bool_field(1)
