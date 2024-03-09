import json

from django.core import serializers
from django.http import JsonResponse
from django.views.generic import DetailView


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

        serializer = serializers.serialize(
            format="json",
            queryset=objects,
            fields=self.fields,
            use_natural_primary_keys=True,
            use_natural_foreign_keys=True,
        )

        data_to_json = {}
        for obj in json.loads(serializer):
            data_to_json = obj["fields"]
            data_to_json["id"] = obj["pk"]

        for related in self.model._meta.get_fields():
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

        return JsonResponse(data_to_json, safe=False)
