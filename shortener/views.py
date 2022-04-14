from shortener.models import Link
from shortener.serializers import LinkSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view


def redirect_to(request, pk):
    """ Redirect to page by the shortened link. """
    link = get_object_or_404(Link, pk=pk)
    link.visits_count += 1
    link.save()
    return HttpResponseRedirect(link.link, status=status.HTTP_308_PERMANENT_REDIRECT)


@api_view(['GET', 'POST'])
def shortener_links(request):
    """ List of all shortened links or add a new one. """
    if request.method == 'GET':
        link = Link.objects.all()
        serializer = LinkSerializer(link, many=True, context={'request': request, })
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LinkSerializer(data=data, context={'request': request, })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if the link already exists in the database, return information about it.
        elif "link with this link already exists." in serializer.errors['link']:
            link = Link.objects.get(link=serializer.data['link'])
            serializer = LinkSerializer(link, context={'request': request, })
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shortener_info(request, pk):
    """ Get info about shortened link. """
    try:
        link = Link.objects.get(pk=pk)
    except Link.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = LinkSerializer(link, context={'request': request, })
        return Response(serializer.data, status=status.HTTP_200_OK)
