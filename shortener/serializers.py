from rest_framework import serializers
from shortener.models import Link


class LinkSerializer(serializers.ModelSerializer):
    shortened_link = serializers.SerializerMethodField('create_link')

    def create_link(self, link):
        """ Create a url link based on the domain it is currently using and a unique id assigned to redirect. """
        return 'http://' + self.context['request'].get_host() + '/' + link.shortened_link

    class Meta:
        model = Link
        fields = ('shortened_link', 'link', 'visits_count', 'user_ip', 'user_agent')
        read_only_fields = ('shortened_link', 'visits_count', 'user_ip', 'user_agent')

    def create(self, validated_data):
        request = self.context['request']
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        validated_data['user_ip'] = ip
        validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT')
        return Link.objects.create(**validated_data)
