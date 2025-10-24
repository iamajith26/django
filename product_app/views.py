from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Catergory, ProductNew  # Import models here
from .serializers import ProductSerializer, CategorySerializer  # Create serializer below
from rest_framework.pagination import PageNumberPagination
from django.http import Http404

# Create your views here.
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:
            try:
                product = ProductNew.objects.select_related('category').get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ProductNew.DoesNotExist:
                raise Http404
        paginator = PageNumberPagination()
        paginator.page_size = 10
        products = ProductNew.objects.filter(is_active=True).select_related('category').order_by('name')
        results = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, pk=None, format=None):
        if 'activate_product' in request.path:  # Check if the request is for activation
            return self.activate(request, pk)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            custom_response = {
                "message": "Product created successfully",
            }    
            return Response(custom_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        product = ProductNew.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            custom_response = {
                "message": "Product updated successfully",
            }
            return Response(custom_response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            product = ProductNew.objects.get(id=pk)
            product.is_active = False  # Set is_active to False
            product.save()  # Save the changes
            return Response({'message': 'Product successfully marked as inactive!'}, status=status.HTTP_200_OK)
        except ProductNew.DoesNotExist:
            return Response({'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    def activate(self, request, pk, format=None):
        try:
            product = ProductNew.objects.get(id=pk)
            product.is_active = True  # Set is_active to True
            product.save()  # Save the changes
            return Response({'message': 'Product successfully reactivated!'}, status=status.HTTP_200_OK)
        except ProductNew.DoesNotExist:
            return Response({'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    
        # # Execute raw SQL query
        #     with connection.cursor() as cursor:
        #         cursor.execute("""
        #             SELECT id, name, description, price, stock, created_at, updated_at
        #             FROM product_app_product
        #             ORDER BY name
        #         """)
        #         # Fetch all rows
        #         rows = cursor.fetchall()
        #         # Get column names from cursor description
        #         columns = [col[0] for col in cursor.description]
        #         # Convert rows to list of dictionaries
        #         products = [dict(zip(columns, row)) for row in rows]

        #     return Response(products, status=status.HTTP_200_OK)
        
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:
            try:
                category = Catergory.objects.get(pk=pk)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Catergory.DoesNotExist:
                raise Http404
        categories = Catergory.objects.filter(is_active=True).order_by('name') # Fetch only active categories
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None, format=None):
        if 'activate_category' in request.path:  # Check if the request is for activation
            return self.activate(request, pk)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()  # Save the category to the database
            custom_response = {
                "message": "Category created successfully",
            }
            return Response(custom_response, status=status.HTTP_201_CREATED)  # Return the custom response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors
    
    def put(self, request, pk, format=None):
        category = Catergory.objects.get(id=pk)
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            custom_response = {
                "message": "Category updated successfully",
            }
            return Response(custom_response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            category = Catergory.objects.get(id=pk)  # Corrected to fetch category
            category.is_active = False  # Set is_active to False
            category.save()  # Save the changes
            return Response({'message': 'Category successfully marked as inactive!'}, status=status.HTTP_200_OK)
        except Catergory.DoesNotExist:
            return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    def activate(self, request, pk, format=None):
        try:
            category = Catergory.objects.get(id=pk)  # Corrected to fetch category
            category.is_active = True  # Set is_active to True
            category.save()  # Save the changes
            return Response({'message': 'Category successfully reactivated!'}, status=status.HTTP_200_OK)
        except Catergory.DoesNotExist:
            return Response({'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    
        # # Execute raw SQL query
        # with connection.cursor() as cursor:
        #     cursor.execute("""
        #         SELECT id, name, description
        #         FROM product_app_category
        #         ORDER BY name
        #     """)
        #     rows = cursor.fetchall()
        #     columns = [col[0] for col in cursor.description]
        #     categories = [dict(zip(columns, row)) for row in rows]

        # return Response(categories, status=status.HTTP_200_OK)