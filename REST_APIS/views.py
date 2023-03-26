from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from REST_APIS.models import Message
from REST_APIS.serializers import MessageSerializer
from REST_APIS.apps import RestApisConfig
import numpy as np


def predict_sentence_category(sentence, model_name):
    if model_name == 'sbert_cnn':
        pred_dict = {0: 'Hate', 1: "Offensive", 2: "Neither"}
        encoding = RestApisConfig.sentence_transformer.encode(sentence)
        new_encoding = np.array(list(encoding[:361]))
        new_encoding = new_encoding.reshape((19, 19,))
        new_encoding = new_encoding.reshape((-1, 19, 19, 1))
        predictions = RestApisConfig.cnn_model.predict(new_encoding)[0]
        num_prediction = np.argmax(predictions)
        return pred_dict[num_prediction]
    else:
        pass


# Create your views here.
@api_view(['GET', 'POST'])
def message_bulk_get_or_post(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializers = MessageSerializer(messages, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        request_data = request.data
        request_data['sentence_type'] = predict_sentence_category(request.data['sentence'],'sbert_cnn')
        serializer = MessageSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def message_detail(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except:
        resp = {"error" : "Message with this id doesn't exist."}
        return Response(resp,status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == 'PUT':
        request_data = request.data
        request_data['sentence_type'] = predict_sentence_category(request.data['sentence'], 'sbert_cnn')
        serializer = MessageSerializer(message, request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message.delete()
        resp = {"success": "Message Deleted"}
        return Response(resp,status=status.HTTP_204_NO_CONTENT)
