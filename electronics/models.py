from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наизменование продукта')
    model = models.CharField(max_length=50, verbose_name='модель продукта')
    release_date = models.DateField(verbose_name='дата выхода продукта')
    supplier = models.ForeignKey('NetworkNode', on_delete=models.CASCADE, null=True, verbose_name='поставщик')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class NetworkNode(models.Model):
    NODE_FACTORY = 'factory'
    NODE_IE = 'ie'  # individual entrepreneur
    NODE_RETAIL_NETWORK = 'retail_network'

    NODE_TYPES = (
        (NODE_FACTORY, 'Завод'),
        (NODE_IE, 'ИП'),
        (NODE_RETAIL_NETWORK, 'Розничная сеть')
    )

    name = models.CharField(max_length=50, verbose_name='название')
    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=50, verbose_name='страна')
    city = models.CharField(max_length=50, verbose_name='город')
    street = models.CharField(max_length=50, verbose_name='улица')
    house_number = models.PositiveSmallIntegerField(verbose_name='номер дома')
    products = models.ManyToManyField(Product, blank=True, verbose_name='продукты')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='долг перед поставщиком')
    hierarchy_level = models.PositiveSmallIntegerField(blank=True, verbose_name='уровень в иерархии')
    node_type = models.CharField(max_length=20, choices=NODE_TYPES, verbose_name='тип элемента сети')

    supplier = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='suppliers')

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем уровень иерархии
        if self.node_type == self.NODE_FACTORY:
            self.hierarchy_level = 0
        elif self.supplier.hierarchy_level == 0:
            self.hierarchy_level = 1
        else:
            self.hierarchy_level = 2
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
