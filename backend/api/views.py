import json
from django.http import JsonResponse

from .models import delete_task_recursively, Project, Task


def create_task(request):
    try:
        payload = _get_payload(
            request,
            {
                "description": str,
                "order": int,
                "parent_pk": (int, type(None)),
                "project_pk": int,
            },
        )
    except ApiError as e:
        return _error_response(e.args[0])

    try:
        project = Project.objects.get(pk=payload["project_pk"])
    except Project.DoesNotExist:
        return _error_response("project not found")

    if payload["parent_pk"] is not None:
        try:
            parent = Task.objects.get(pk=payload["parent_pk"])
        except Task.DoesNotExist:
            return _error_response("parent task not found")

        if parent.project != project:
            return _error_response("project is not the same as parent's project")
    else:
        parent = None

    try:
        order = int(payload["order"])
    except ValueError:
        return _error_response("order field must be an integer")

    short, long = _parse_description(payload["description"])
    task = Task.objects.create(
        short_description=short,
        long_description=long,
        project=project,
        parent=parent,
        order=order,
    )
    return _success_response({"pk": task.pk})


def update_task_description(request):
    try:
        payload = _get_payload(request, required_keys={"pk": int, "description": str})
    except ApiError as e:
        return _error_response(e.args[0])

    try:
        task = Task.objects.get(pk=payload["pk"])
    except Task.DoesNotExist:
        return _error_response("task not found")

    short, long = _parse_description(payload["description"])
    task.short_description = short
    task.long_description = long
    task.save()
    return _success_response({"pk": task.pk})


def update_task_status(request):
    try:
        payload = _get_payload(request, required_keys={"pk": int, "status": str})
    except ApiError as e:
        return _error_response(e.args[0])

    if not any(choice == payload["status"] for choice, _ in Task.STATUS_CHOICES):
        return _error_response("unknown value for status field")

    try:
        task = Task.objects.get(pk=payload["pk"])
    except Task.DoesNotExist:
        return _error_response("task not found")

    task.status = payload["status"]
    task.save()
    return _success_response({"pk": task.pk})


def delete_task(request):
    try:
        payload = _get_payload(request, required_keys={"pk": int})
    except ApiError as e:
        return _error_response(e.args[0])

    pk = payload["pk"]
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return _error_response("task not found")

    delete_task_recursively(task)
    return _success_response({"pk": pk})


def get_project(request):
    if "pk" not in request.GET:
        return _error_response("request missing keys: pk")

    try:
        pk = int(request.GET["pk"])
    except ValueError:
        return _error_response("pk should have type int")

    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return _error_response("project not found")

    return _success_response(project.json())


def create_project(request):
    try:
        payload = _get_payload(request, required_keys={"name": str, "description": str})
    except ApiError as e:
        return _error_response(e.args[0])

    project = Project.objects.create(
        name=payload["name"], description=payload["description"]
    )
    return _success_response({"pk": project.pk})


def update_project_description(request):
    try:
        payload = _get_payload(request, required_keys={"pk": int, "description": str})
    except ApiError as e:
        return _error_response(e.args[0])

    try:
        project = Project.objects.get(pk=payload["pk"])
    except Project.DoesNotExist:
        return _error_response("project not found")

    project.description = payload["description"]
    project.save()
    return _success_response({"pk": project.pk})


def delete_project(request):
    try:
        payload = _get_payload(request, required_keys={"pk": int})
    except ApiError as e:
        return _error_response(e.args[0])

    pk = payload["pk"]
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return _error_response("project not found")

    project.delete()
    return _success_response({"pk": pk})


def _success_response(jsonobj=None):
    """Creates an HTTP response for a successful action."""
    return JsonResponse(jsonobj or {})


def _error_response(message):
    """Creates an HTTP response for an error."""
    return JsonResponse({"error": message}, status=400)


def _get_payload(request, required_keys):
    """Parses the payload as JSON and verifies that it matches `required_keys`.

    `required_keys` is the map of keys that the JSON payload must contain. It maps from
    key names to types, e.g. `int` or `str`. If the payload doesn't contain all the
    keys, or if it contains keys not in `required_keys`, or if the values in payload
    have the wrong type, an exception is raised.

    The values in `required_keys` may also be tuples, if a key can have multiple types.
    """
    try:
        payload = json.loads(request.body, encoding="utf8")
    except UnicodeDecodeError:
        raise ApiError("request is not valid UTF-8")
    except json.decoder.JSONDecodeError:
        raise ApiError("request is not valid JSON")

    required_keys_as_set = set(required_keys.keys())
    keyset = set(payload.keys())
    missing_keys = required_keys_as_set - keyset
    if missing_keys:
        raise ApiError("request missing keys: " + ", ".join(sorted(missing_keys)))

    unknown_keys = keyset - required_keys_as_set
    if unknown_keys:
        raise ApiError("request has unknown keys: " + ", ".join(sorted(unknown_keys)))

    for key, value in required_keys.items():
        if isinstance(value, tuple):
            if all(not isinstance(payload[key], v) for v in value):
                types_as_str = " or ".join(v.__name__ for v in value)
                raise ApiError(f"{key} should have type {types_as_str}")
        else:
            if not isinstance(payload[key], value):
                raise ApiError(f"{key} should have type {value.__name__}")

    return payload


def _parse_description(description):
    """Parses a multi-line description into a short and long description.

    Returns a tuple `(short_description, long_description)`, where `long_decription`
    may be the empty string.

    The short description is the first line of the description and the long description
    is the rest of it.

    Leading and trailing whitespace is stripped from both descriptions.
    """
    description = description.strip()
    if "\n" in description:
        first, rest = description.split("\n", maxsplit=1)
        return (first.strip(), rest.strip())
    else:
        return (description, "")


class ApiError(Exception):
    pass
