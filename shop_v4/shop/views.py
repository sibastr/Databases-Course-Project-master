from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, Category, Feature, FeatureVariant, FeatureSet, Color
from cart.models import Cart, Order, OrderItem
from functools import reduce


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 18

    def get_queryset(self):
        return Product.objects.filter(displayed=True).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.order_by('name')
        if not self.request.user.is_anonymous:
            context['products_in_cart'] = Cart.objects.filter(user=self.request.user).first().cartitem_set.all().values_list('product', flat=True)

        return context


def is_valid_queryparam(param):
    return param != '' and param is not None


class ProductCategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/productcategory_list.html'
    context_object_name = 'category'
    paginate_by = 18

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Список товаров в корзине
        if not self.request.user.is_anonymous:
            context['products_in_cart'] = Cart.objects.filter(
                user=self.request.user).first().cartitem_set.all().values_list('product', flat=True)

        # Список цветов
        context['colors'] = Color.objects.all()

        # ФИЛЬТРЫ
        filtered_q = FeatureSet.objects.filter(product__category=self.get_object(), product__displayed=True)
        marked_filters = []
        marked_colors = []
        marked_stock = 'all'
        marked_sale = 'all'
        marked_sort = '1'

        # radiobutton Наличие
        var = self.request.GET.get('rb_st')
        if is_valid_queryparam(var):
            if var == 'yes':
                marked_stock = 'yes'
                filtered_q = filtered_q & FeatureSet.objects.filter(product__in_stock=True)
            elif var == 'no':
                marked_stock = 'no'
                filtered_q = filtered_q & FeatureSet.objects.filter(product__in_stock=False)

        var = self.request.GET.get('rb_sl')
        if is_valid_queryparam(var):
            if var == 'yes':
                marked_sale = 'yes'
                filtered_q = filtered_q & FeatureSet.objects.filter(product__on_sale=True)
            elif var == 'no':
                marked_sale = 'no'
                filtered_q = filtered_q & FeatureSet.objects.filter(product__on_sale=False)

        # Если категория имеет features
        if len(filtered_q) != 0:

            # CHECKBOX
            used = []
            for f in self.get_object().get_features().filter(type='checkbox'):
                cur_filtered = FeatureSet.objects.none()
                used.append([])
                for v in f.get_variants():
                    var = self.request.GET.get('ch_' + str(v.id))

                    if is_valid_queryparam(var):
                        marked_filters.append(v.id)
                        used[-1].append(1)
                        for line in FeatureSet.objects.filter(feature_variant=v.id):
                            cur_filtered = cur_filtered | FeatureSet.objects.filter(product=line.product)
                    else:
                        used[-1].append(0)
                # Если хотя бы один чекбокс в фильтре был отмечен, используем AND с прошлым результатом
                if 1 in used[-1]:
                    filtered_q = filtered_q & cur_filtered

            # RADIOBUTTON
            for f in self.get_object().get_features().filter(type='radiobutton'):
                var = self.request.GET.get('rb_' + str(f.id))

                if is_valid_queryparam(var) and var != 'no':
                    cur_filtered = FeatureSet.objects.none()
                    marked_filters.append(int(var))

                    for line in FeatureSet.objects.filter(feature_variant=int(var)):
                        cur_filtered = cur_filtered | FeatureSet.objects.filter(product=line.product)

                    filtered_q = filtered_q & cur_filtered

            # COLOR
            cur_filtered = FeatureSet.objects.none()
            used = []
            for clr in Color.objects.all():
                var = self.request.GET.get('clr_' + str(clr.id))

                if is_valid_queryparam(var):
                    used.append(1)
                    marked_colors.append(clr.id)
                    for line in FeatureSet.objects.filter(product__color=clr.id):
                        cur_filtered = cur_filtered | FeatureSet.objects.filter(product=line.product)
                else:
                    used.append(0)

            if 1 in used:
                filtered_q = filtered_q & cur_filtered

            # FeatureSet -> Product
            ok_products = []
            for p in filtered_q.values('product'):
                ok_products.append(p['product'])
            ok_products = set(ok_products)

            final_products = Product.objects.none()
            for i in ok_products:
                if i in filtered_q.values('product'):
                    print(i, 'ok')
                final_products = final_products | Product.objects.filter(id=i)

            context['filtered_products'] = final_products
        # Если продукт не имеет features
        else:
            used = []
            cur_products = Product.objects.none()

            for clr in Color.objects.all():
                var = self.request.GET.get('clr_' + str(clr.id))

                if is_valid_queryparam(var):
                    used.append(1)
                    marked_colors.append(clr.id)
                    cur_products = cur_products | Product.objects.filter(color=clr.id)
                else:
                    used.append(0)

            if 1 in used:
                context['filtered_products'] = cur_products
            else:
                context['filtered_products'] = self.get_object().get_products()

        var = self.request.GET.get('sort')
        if is_valid_queryparam(var):
            if var == '1':
                marked_sort = '1'
                context['filtered_products'] = context['filtered_products'].order_by('name')
            elif var == '2':
                marked_sort = '2'
                context['filtered_products'] = context['filtered_products'].order_by('-in_stock', 'cost')
            elif var == '3':
                marked_sort = '3'
                context['filtered_products'] = context['filtered_products'].order_by('-in_stock', '-cost')

        context['marked_filters'] = marked_filters
        context['marked_colors'] = marked_colors
        context['marked_stock'] = marked_stock
        context['marked_sale'] = marked_sale
        context['marked_sort'] = marked_sort

        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for i in self.get_object().get_reviews().values_list('user', flat=True):
            print(i)

        if self.request.user.id in self.get_object().get_reviews().values_list('user', flat=True):
            context['review_id'] = self.get_object().get_reviews().get(user=self.request.user)
        else:
            context['review_id'] = None
        if not self.request.user.is_anonymous:
            context['products_in_cart'] = Cart.objects.filter(user=self.request.user).first().cartitem_set.all().values_list('product',
                                                                                                             flat=True)
        context['product_features'] = FeatureSet.objects.filter(product=self.get_object())
        return context
