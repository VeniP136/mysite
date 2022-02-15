from django.db import models
# cd /var/www/mysite
# python3 manage.py makemigrations
# python3 manage.py migrate


class Категория(models.Model):
    Имя = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Категория"

    def __str__(Категория):
        return Категория.Имя


class Подкатегория(models.Model):
    Категория = models.ForeignKey(Категория, on_delete=models.CASCADE)
    Имя = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Подкатегория"

    def __str__(Подкатегория):
        return Подкатегория.Имя


class Продукт(models.Model):
    Подкатегория = models.ForeignKey(Подкатегория, null=True, blank=True, default=None, on_delete=models.CASCADE)
    Категория = models.ForeignKey(Категория, null=True, blank=True, default=None, on_delete=models.CASCADE)
    Имя = models.CharField(max_length=40)
    Описание = models.CharField(max_length=400)
    Цена = models.CharField(max_length=40)
    Фото = models.ImageField(upload_to='images/')
    Отключить_продукт = models.BooleanField()

    class Meta:
        verbose_name_plural = "Продукт"

    def __str__(Продукт):
        return Продукт.Имя


class Акции(models.Model):
    # Подкатегория = models.ForeignKey(Подкатегория, null=True, blank=True, default=None, on_delete=models.CASCADE)
    # Категория = models.ForeignKey(Категория, null=True, blank=True, default=None, on_delete=models.CASCADE)
    Имя = models.CharField(max_length=40)
    Описание = models.CharField(max_length=400)
    Цена = models.CharField(max_length=40)
    Фото = models.ImageField(upload_to='images/')
    Дата_начала = models.DateTimeField(null=True, blank=True, default=None)
    Дата_окончания = models.DateTimeField(null=True, blank=True, default=None)
    Отключить_акцию = models.BooleanField()
    class Meta:
        verbose_name_plural = "Акции"

    def __str__(Акции):
        return Акции.Имя



class UseCategory(models.Model):
    chatid = models.CharField(max_length=40)
    category = models.CharField(max_length=40)
    subcategory = models.CharField(max_length=40)
    globall = models.CharField(max_length=40)
    address = models.CharField(max_length=400, null=True, blank=True, default=None)
    name = models.CharField(max_length=40, null=True, blank=True, default=None)
    telephone = models.CharField(max_length=40, null=True, blank=True, default=None)
    handler = models.CharField(max_length=40, null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "UseCategory"


class basket(models.Model):
    chatid = models.CharField(max_length=40)
    productid = models.CharField(max_length=40)
    quantity = models.CharField(max_length=40)
    action = models.BooleanField()

    class Meta:
        verbose_name_plural = "basket"



class addresses(models.Model):
    chatid = models.CharField(max_length=40)
    address = models.CharField(max_length=400, null=True, blank=True, default=None)
    name = models.CharField(max_length=40, null=True, blank=True, default=None)
    telephone = models.CharField(max_length=40, null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "addresses"


class orders(models.Model):
    # по дате определяется к какому заказу относится позиция
    date = models.DateTimeField(null=True, blank=True, default=None)
    chatid = models.CharField(max_length=40)
    faze = models.CharField(max_length=40)
    address_id = models.CharField(max_length=40)
    CRM = models.CharField(max_length=40)
    youMoneyId = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = "orders"

class buket_arhiv(models.Model):
    # по дате определяется к какому заказу относится позиция
    date = models.DateTimeField(null=True, blank=True, default=None)
    chatid = models.CharField(max_length=40)
    productid = models.CharField(max_length=40)
    quantity = models.CharField(max_length=40)
    action = models.BooleanField()

    class Meta:
        verbose_name_plural = "buket_arhiv"