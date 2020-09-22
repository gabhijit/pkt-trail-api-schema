from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError

OS_AGENT_INIT_MESSAGE = 'pkttrail.agent.os.init'
OS_AGENT_KEEPALIVE_MESSAGE = 'pkttrail.agent.os.keepalive'
JSON_RPC_VERSION_2 = "2.0"

class PktTrailSchemaValidationError(ValidationError):
    pass


class JSONRPCBaseSchema(Schema):
    jsonrpc = fields.Str(required=True, validate=lambda v: v == JSON_RPC_VERSION_2)
    method = fields.Str(required=True)

class JSONRPCRequestSchema(JSONRPCBaseSchema):
    """JSON RPC Request Class for JSON RPC 2.0 ."""
    id = fields.Str(required=True)

class JSONRPCResponseSchema(JSONRPCBaseSchema):
    """JSON RPC Response Class for JSON RPC 2.0 ."""
    id = fields.Str(required=True)

class JSONRPCNotificationSchema(JSONRPCBaseSchema):
    pass


class PktTrailInitRequestParamsSchema(Schema):
    """Params for Init Request Message."""

    schemaVersion = fields.Str(required=True, validate=lambda v: v == "1.0")
    agentSWVersion = fields.Str(required=True)
    agentUUID = fields.UUID(required=True)

class PktTrailInitRequestSchema(JSONRPCRequestSchema):
    """Init Request Message."""
    params = fields.Nested(PktTrailInitRequestParamsSchema)
    method = fields.Str(required=True,
            validate=lambda v: v == OS_AGENT_INIT_MESSAGE)


class PktTrailInitResponseResultsSchema(Schema):
    """Result Schema."""
    status = fields.Str(required=True, validate=lambda v:v == "ok")


class PktTrailInitResponseSchema(JSONRPCResponseSchema):
    """Init Response Message."""
    result = fields.Nested(PktTrailInitResponseResultsSchema)
    method = fields.Str(required=True,
            validate=lambda v: v == OS_AGENT_INIT_MESSAGE)


class PktTrailServiceSchema(Schema):
    """Schema for a 'service'."""
    interface = fields.Str(required=True)
    port = fields.Integer(required=True, validate=lambda v: v > 0 and v < 65536)
    proto = fields.Str(require=True)
    name = fields.Str()

class PktTrailKeepAliveRequestParamsSchema(Schema):
    agentUUID = fields.UUID(required=True)
    services = fields.Nested(PktTrailServiceSchema, many=True)

class PktTrailKeepAliveResponseResultsSchema(Schema):
    status = fields.Str(required=True, validate=lambda v:v == "ok")


class PktTrailKeepAliveRequestSchema(JSONRPCRequestSchema):
    """Keep Alive Request Message."""
    params = fields.Nested(PktTrailKeepAliveRequestParamsSchema)
    method = fields.Str(required=True,
            validate=lambda v: v == OS_AGENT_KEEPALIVE_MESSAGE)


class PktTrailKeepAliveResponseSchema(JSONRPCResponseSchema):
    """Keep Alive Response Message."""
    result = fields.Nested(PktTrailKeepAliveResponseResultsSchema)
    method = fields.Str(required=True,
            validate=lambda v: v == OS_AGENT_KEEPALIVE_MESSAGE)


class PktTrailStatus(JSONRPCNotificationSchema):
    """Status Message."""
    pass


if __name__ == '__main__':

    import uuid

    agent_uuid = str(uuid.uuid1())

    init_req_json = """ {{
        "jsonrpc": "2.0",
        "method": "pkttrail.agent.os.init",
        "id" : "1",
        "params": {{
            "agentUUID": "{}",
            "schemaVersion" : "1.0",
            "agentSWVersion" : "0.0.1"
        }}
    }}""".format(agent_uuid)

    init_req = PktTrailInitRequestSchema().loads(init_req_json)
    print(init_req)

    keepalive_req_json = """ {{
        "jsonrpc": "2.0",
        "method": "pkttrail.agent.os.keepalive",
        "id" : "1",
        "params": {{
            "agentUUID": "{}"
        }}
    }}""".format(agent_uuid)

    keepalive_req = PktTrailKeepAliveRequestSchema().loads(keepalive_req_json)
    print(keepalive_req)
