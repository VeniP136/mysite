from django.contrib import admin

from .models import buket_arhiv
admin.site.register(buket_arhiv)

from .models import orders
admin.site.register(orders)

from .models import addresses
admin.site.register(addresses)

from .models import UseCategory
admin.site.register(UseCategory)

from .models import basket
admin.site.register(basket)

from .models import Категория
admin.site.register(Категория)

from .models import Подкатегория
admin.site.register(Подкатегория)

from .models import Акции
admin.site.register(Акции)

from .models import Продукт
admin.site.register(Продукт)
