from collections.abc import Callable, Sequence
from typing import Any, NamedTuple, TypeVar

from coreapi import Field as CoreAPIField  # type: ignore[import-untyped]
from django.core.paginator import Page, Paginator
from django.db.models import Model, QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from typing_extensions import TypedDict

def _positive_int(integer_string: str, strict: bool = ..., cutoff: int | None = ...) -> int: ...
def _divide_with_ceil(a: int, b: int) -> int: ...
def _get_displayed_page_numbers(current: int, final: int) -> list[int | None]: ...
def _get_page_links(
    page_numbers: Sequence[int | None], current: int, url_func: Callable[[int], str]
) -> list[PageLink]: ...
def _reverse_ordering(ordering_tuple: Sequence[str]) -> tuple[str, ...]: ...

class Cursor(NamedTuple):
    offset: int
    reverse: bool
    position: int | None

class PageLink(NamedTuple):
    url: str | None
    number: int | None
    is_active: bool
    is_break: bool

class HtmlContext(TypedDict):
    previous_url: str
    next_url: str

class HtmlContextWithPageLinks(HtmlContext):
    page_links: list[PageLink]

PAGE_BREAK: PageLink

_MT = TypeVar("_MT", bound=Model)

class BasePagination:
    display_page_controls: bool
    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]: ...
    def get_paginated_response(self, data: Any) -> Response: ...
    def get_results(self, data: dict[str, Any]) -> Any: ...
    def get_schema_fields(self, view: APIView) -> list[Any]: ...
    def get_schema_operation_parameters(self, view: APIView) -> list[Any]: ...
    def paginate_queryset(
        self, queryset: QuerySet[_MT], request: Request, view: APIView | None = ...
    ) -> list[_MT] | None: ...
    def to_html(self) -> str: ...

class PageNumberPagination(BasePagination):
    display_page_controls: bool
    django_paginator_class: type[Paginator]
    invalid_page_message: str
    last_page_strings: Sequence[str]
    max_page_size: int | None
    page_query_description: str
    page_query_param: str
    page_size_query_description: str
    page_size_query_param: str | None
    page_size: int | None
    page: Page | None
    request: Request | None
    template: str | None
    def paginate_queryset(
        self, queryset: QuerySet[_MT], request: Request, view: APIView | None = ...
    ) -> list[_MT] | None: ...
    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]: ...
    def get_schema_fields(self, view: APIView) -> list[CoreAPIField]: ...
    def get_schema_operation_parameters(self, view: APIView) -> list[dict[str, Any]]: ...
    def get_page_number(self, request: Request, paginator: Paginator) -> int | str: ...
    def get_page_size(self, request: Request) -> int | None: ...
    def get_next_link(self) -> str | None: ...
    def get_previous_link(self) -> str | None: ...
    def get_html_context(self) -> HtmlContextWithPageLinks: ...

class LimitOffsetPagination(BasePagination):
    count: int | None
    default_limit: int | None
    limit_query_description: str
    limit_query_param: str
    limit: int | None
    max_limit: int | None
    offset_query_description: str
    offset_query_param: str
    offset: int | None
    request: Request | None
    template: str | None
    def paginate_queryset(
        self, queryset: QuerySet[_MT], request: Request, view: APIView | None = ...
    ) -> list[_MT] | None: ...
    def get_limit(self, request: Request) -> int | None: ...
    def get_offset(self, request: Request) -> int: ...
    def get_next_link(self) -> str | None: ...
    def get_previous_link(self) -> str | None: ...
    def get_html_context(self) -> HtmlContextWithPageLinks: ...
    def get_count(self, queryset: QuerySet | Sequence) -> int: ...

class CursorPagination(BasePagination):
    base_url: str | None
    cursor_query_description: str
    cursor_query_param: str
    cursor: Cursor | None
    has_next: bool | None
    has_previous: bool | None
    invalid_cursor_message: str
    max_page_size: int | None
    next_position: str | None
    offset_cutoff: int
    ordering: str | list[str] | tuple[str, ...]
    page_size_query_description: str
    page_size_query_param: str | None
    page_size: int | None
    page: list[Any] | None
    previous_position: str | None
    template: str | None
    def paginate_queryset(
        self, queryset: QuerySet[_MT], request: Request, view: APIView | None = ...
    ) -> list[_MT] | None: ...
    def get_page_size(self, request: Request) -> int | None: ...
    def get_next_link(self) -> str | None: ...
    def get_previous_link(self) -> str | None: ...
    def get_html_context(self) -> HtmlContext: ...
    def get_ordering(self, request: Request, queryset: QuerySet, view: APIView) -> tuple[str, ...]: ...
    def decode_cursor(self, request: Request) -> Cursor | None: ...
    def encode_cursor(self, cursor: Cursor) -> str: ...
    def _get_position_from_instance(self, instance: Any, ordering: Sequence[str]) -> str: ...
