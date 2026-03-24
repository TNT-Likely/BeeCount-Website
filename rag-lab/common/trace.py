from contextvars import ContextVar


_trace_id_var: ContextVar[str] = ContextVar('trace_id', default='-')


def set_trace_id(trace_id: str) -> None:
    _trace_id_var.set(trace_id)


def get_trace_id() -> str:
    return _trace_id_var.get()
