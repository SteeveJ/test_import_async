import json

from django.core import serializers
from django.http import JsonResponse
from django.views.generic import DetailView, ListView


def serialize_queryset(queryset, fields: list[str]) -> dict[str, any]:
    serializer = serializers.serialize(
        format="json",
        queryset=queryset,
        fields=fields,
        use_natural_primary_keys=True,
        use_natural_foreign_keys=True,
    )

    data_to_json = {}
    for obj in json.loads(serializer):
        data_to_json = obj["fields"]
        data_to_json["id"] = obj["pk"]

    return data_to_json


def get_related_objects(model, objects: list, data_to_json: dict[str, any]) -> dict:
    for related in model._meta.get_fields():
        if related.get_internal_type() == "ForeignKey":
            data_to_json[related.name] = []

            # get related model
            related_model = related.related_model

            # get related objects
            related_objects = related_model.objects.filter(
                **{related.field.name: objects[0]}
            )

            # serialize related objects
            related_serializer = serializers.serialize(
                format="json",
                queryset=related_objects,
                use_natural_primary_keys=True,
                use_natural_foreign_keys=True,
            )

            # add related objects to data_to_json
            for obj in json.loads(related_serializer):
                obj["fields"]["id"] = obj["pk"]
                data_to_json[related.name].append(obj["fields"])
    return data_to_json


class ExtendedDetailView(DetailView):
    fields: list[str] = list()

    """A base view for displaying a single object."""

    def get(self, request, *args, **kwargs):
        try:
            objects = self.get_queryset()
        except self.model.DoesNotExist:
            return JsonResponse(
                {
                    "error": "No %(verbose_name)s found matching the query"
                    % {"verbose_name": self.model._meta.verbose_name}
                },
                status=404,
            )

        data_to_json = serialize_queryset(objects, self.fields)
        data_to_json = get_related_objects(self.model, objects, data_to_json)

        return JsonResponse(data_to_json, safe=False)


class ExtendedListView(ListView):
    fields: list[str] = list()

    def _paginate(self, request, query, *args, **kwargs) -> dict[str, any]:
        page_size = int(request.GET.get("page_size", 100))
        page_num = int(request.GET.get("page_num", 0))
        start = page_num * page_size
        end = start + page_size
        data = query[start:end]
        total_size = query.count()
        return {
            data: data,
            total_size: total_size,
            page_num: page_num,
            page_size: page_size,
        }

    def get(self, request, *args, **kwargs):
        try:
            # get object using queryset and pagination
            objects = self.get_queryset()
        except self.model.DoesNotExist:
            return JsonResponse(
                {
                    "error": "No %(verbose_name)s found matching the query"
                    % {"verbose_name": self.model._meta.verbose_name}
                },
                status=404,
            )

        (data, total_size, page_num, page_size) = self._paginate(request, objects)

        data_to_json = []

        # serialize each objects
        for obj in data:
            data = serialize_queryset([obj], self.fields)
            data = get_related_objects(self.model, [obj], data)
            data_to_json.append(data)

        return JsonResponse(
            {
                "data": data_to_json,
                "total_size": total_size,
                "page_num": page_num,
                "page_size": page_size,
            },
            safe=False,
        )
