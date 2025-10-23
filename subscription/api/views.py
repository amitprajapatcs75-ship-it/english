from subscription.models.subscriptions import Plan
from subscription.serializers.plan_serializers import PlanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

class SubscriptionPlanApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = Plan.objects.all()
        serializer = PlanSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = PlanSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            data.save(user=request.user)
            return Response({'message': 'Plan create successfully', 'status': True}, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        plan_id = request.query_params.get('id')
        if not plan_id:
            return Response({'plan_id': 'Plan id is required', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(id = plan_id)
        except Plan.DoesNotExist:
            return Response({"message": "Plan not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Plan update successfully', 'status': True},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
