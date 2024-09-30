from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated
from rest_framework.authentication import TokenAuthentication  # Import TokenAuthentication


class ItemViewAPI(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]
    # Retrieve (GET) a specific item by id or all items if no id is provided
    def get(self, request):
        try:
            item_id = request.query_params.get('item_id', None)
            if item_id:
                try:
                    item = Item.objects.get(id=item_id)
                except Item.DoesNotExist:
                    return Response(
                        {"message": "Item not found", "data": {}},
                        status=status.HTTP_404_NOT_FOUND
                    )
                serializer = ItemSerializer(item)
                return Response(
                    {"message": "Item retrieved successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                items = Item.objects.all()
                serializer = ItemSerializer(items, many=True)
                return Response(
                    {"message": "Items retrieved successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"message": "Something went wrong: " + str(e), "data": {}},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Create (POST) a new item
    def post(self, request):
        try:
            print(f"Request data: {request.data}")  # Debugging output
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Item created successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": f"Something went wrong: {str(e)}", "data": {}},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Update (PUT) an existing item
    def put(self, request):
        try:
            item_id = request.data.get('item_id', None)
            print(item_id)
            if not item_id:
                return Response(
                    {"message": "Item ID is required", "data": {}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                item = Item.objects.get(id=item_id)
                print(item)
            except Item.DoesNotExist:
                return Response(
                    {"message": "Item not found", "data": {}},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ItemSerializer(item, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Item updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Something went wrong: " + str(e), "data": {}},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Partially update (PATCH) an existing item
    def patch(self, request):
        try:
            item_id = request.data.get('item_id', None)
            if not item_id:
                return Response(
                    {"message": "Item ID is required", "data": {}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                return Response(
                    {"message": "Item not found", "data": {}},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Item partially updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Something went wrong: " + str(e), "data": {}},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Delete (DELETE) an existing item
    def delete(self, request):
        try:
            item_id = request.query_params.get('item_id', None)
            if not item_id:
                return Response(
                    {"message": "Item ID is required", "data": {}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                item = Item.objects.get(id=item_id)
                item.delete()
                return Response(
                    {"message": "Item deleted successfully", "data": {}},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Item.DoesNotExist:
                return Response(
                    {"message": "Item not found", "data": {}},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"message": "Something went wrong: " + str(e), "data": {}},
                status=status.HTTP_400_BAD_REQUEST
            )
