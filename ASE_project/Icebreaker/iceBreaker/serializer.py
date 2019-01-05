from rest_framework import serializers
from django.contrib.auth.models import User
from register.models import Temp,Profile
from community.models import GroupTable,MemberTable,CommentTable

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('github_link','facebook_link','linkedIn_link')






class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTable
        fields = ('founder','title','type','lat','lon','date','number','address')

class MemberSerializer(serializers.ModelSerializer):
    group = CommunitySerializer()
    class Meta:
        model = MemberTable
        fields = ('group','user')

    def create(self, validated_data):
        userlog_data = validated_data.pop('group')
        group = GroupTable.objects.create(**userlog_data)
        user = validated_data['user']


        p = MemberTable.objects.create(user=user,group=group,)
        return p


class CommentSerializer(serializers.ModelSerializer):
    group = CommunitySerializer()

    class Meta:
        model = CommentTable
        fields = ('group', 'user','comment')

    def create(self, validated_data):
        userlog_data = validated_data.pop('group')
        group = CommentTable.objects.create(**userlog_data)
        user = validated_data['user']
        comment = validated_data['comment']


        q = CommentTable.objects.create(user=user,comment=comment,group=group,)
        return q