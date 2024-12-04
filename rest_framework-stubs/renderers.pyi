from _typeshed import Incomplete
from collections.abc import Iterable, Mapping, Sequence
from json import JSONEncoder
from typing import Any, ClassVar

from django import forms
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework.views import APIView

def zero_as_none(value: Any) -> Any | None: ...

class BaseRenderer:
    media_type: str | None
    format: str | None
    charset: str | None
    render_style: str
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> Any: ...

class JSONRenderer(BaseRenderer):
    encoder_class: ClassVar[type[JSONEncoder]]
    ensure_ascii: ClassVar[bool]
    compact: ClassVar[bool]
    strict: ClassVar[bool]
    def get_indent(self, accepted_media_type: str, renderer_context: Mapping[str, Any]) -> int | None: ...

class TemplateHTMLRenderer(BaseRenderer):
    template_name: str | None
    exception_template_names: Sequence[str]
    def resolve_template(self, template_names: Iterable[str]) -> Any: ...
    def get_template_context(self, data: Any, renderer_context: Mapping[str, Any]) -> Incomplete: ...
    def get_template_names(self, response: Response, view: APIView) -> list[str]: ...
    def get_exception_template(self, response: Response) -> Any: ...

class StaticHTMLRenderer(TemplateHTMLRenderer): ...

class HTMLFormRenderer(BaseRenderer):
    template_pack: str
    base_template: str

    default_style: ClassLookupDict
    def render_field(self, field: Incomplete, parent_style: Mapping[str, Any]) -> str: ...

class BrowsableAPIRenderer(BaseRenderer):
    """
    HTML renderer used to self-document the API.
    """

    template: str
    filter_template: str
    code_style: str
    form_renderer_class: type[BaseRenderer]
    def get_default_renderer(self, view: APIView) -> BaseRenderer: ...
    def get_content(
        self, renderer: BaseRenderer, data: Any, accepted_media_type: str, renderer_context: Mapping[str, Any]
    ) -> str: ...
    def show_form_for_method(self, view: APIView, method: str, request: Request, obj: Any) -> bool: ...
    def _get_serializer(
        self,
        serializer_class: type[BaseSerializer],
        view_instance: APIView,
        request: Request,
        *args: Incomplete,
        **kwargs: Incomplete,
    ) -> BaseSerializer: ...
    def get_rendered_html_form(self, data: Any, view: APIView, method: str, request: Request) -> Any: ...
    def render_form_for_serializer(self, serializer: BaseSerializer) -> Any: ...
    def get_raw_data_form(self, data: Any, view: APIView, method: str, request: Request) -> forms.Form | None: ...
    def get_name(self, view: APIView) -> str: ...
    def get_description(self, view: APIView, status_code: int) -> str: ...
    def get_breadcrumbs(self, request: Request) -> list[tuple[str, str]]: ...
    def get_extra_actions(self, view: APIView) -> dict[str, str] | None: ...
    def get_filter_form(self, data: Any, view: APIView, request: Request) -> Any | None: ...
    def get_context(
        self, data: Any, accepted_media_type: str | None, renderer_context: Mapping[str, Any]
    ) -> dict[str, Any]: ...

class AdminRenderer(BrowsableAPIRenderer):
    def get_result_url(self, result: Mapping[str, Any], view: APIView) -> str | None: ...

class DocumentationRenderer(BaseRenderer):
    template: str
    error_template: str
    code_style: str
    languages: Sequence[str]
    def get_context(self, data: Any, request: Request) -> dict[str, Any]: ...

class SchemaJSRenderer(BaseRenderer):
    template: str

class MultiPartRenderer(BaseRenderer):
    BOUNDARY: str

class CoreJSONRenderer(BaseRenderer): ...

class _BaseOpenAPIRenderer:
    media_type: str
    charset: Any
    format: str
    def __init__(self) -> None: ...
    def render(self, data: Any, media_type: Any | None = ..., renderer_context: Any | None = ...) -> Incomplete: ...
    def get_schema(self, instance: Any) -> dict[str, Any]: ...
    def get_parameters(self, link: Incomplete) -> dict[str, Any]: ...
    def get_operation(self, link: Incomplete, name: Incomplete, tag: Incomplete) -> dict[str, Any]: ...
    def get_paths(self, document: Incomplete) -> dict[str, Any]: ...
    def get_structure(self, data: Any) -> dict[str, Any]: ...

class JSONOpenAPIRenderer(_BaseOpenAPIRenderer):
    encoder_class: ClassVar[type[JSONEncoder]]
    ensure_ascii: ClassVar[bool]

class OpenAPIRenderer(_BaseOpenAPIRenderer): ...
class CoreAPIOpenAPIRenderer(_BaseOpenAPIRenderer): ...

class CoreAPIJSONOpenAPIRenderer(_BaseOpenAPIRenderer):
    ensure_ascii: ClassVar[bool]
