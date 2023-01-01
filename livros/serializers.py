
from rest_framework import serializers
from .models import Ebook


class LivroListSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Ebook 
        fields = ['id','Title', 'Average_Rating','Average_Count']
