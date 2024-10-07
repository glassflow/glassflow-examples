

def handler(data, log):
    return {
        "timestamp": data["Timestamp"],
        "name": data["Name"],
        "severity": data["SeverityText"],
        "message": data["Body"],
        "service_name": data["Resource"]["service.name"],
        "http_method": data["Attributes"]["http.method"],
        "status_code": data["Attributes"]["http.status_code"],
        "user_id": data["Attributes"]["user.id"],
        "trace_id": data["TraceId"],
        "span_id": data["SpanId"],
    }
