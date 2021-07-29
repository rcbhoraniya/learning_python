# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CatalogAuthor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_author'


class CatalogBook(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    isbn = models.CharField(max_length=13)
    author = models.ForeignKey(CatalogAuthor, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_book'


class CatalogBookGenre(models.Model):
    book = models.ForeignKey(CatalogBook, models.DO_NOTHING)
    genre = models.ForeignKey('CatalogGenre', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'catalog_book_genre'
        unique_together = (('book', 'genre'),)


class CatalogBookinstance(models.Model):
    id = models.UUIDField(primary_key=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1)
    book = models.ForeignKey(CatalogBook, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_bookinstance'


class CatalogGenre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'catalog_genre'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Nifty500(models.Model):
    company_name = models.CharField(max_length=80, blank=True, null=True)
    industry = models.CharField(max_length=30, blank=True, null=True)
    symbol = models.CharField(max_length=20, blank=True, null=True)
    series = models.CharField(max_length=5, blank=True, null=True)
    isin_code = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nifty500'


class NseMap(models.Model):
    company_name = models.TextField(blank=True, null=True)
    nse_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nse_map'


class PollsChoice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField()
    question = models.ForeignKey('PollsQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'polls_choice'


class PollsQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'polls_question'


class Stock(models.Model):
    symbol = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    nse_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'stock'


class StockData(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    trade_num = models.IntegerField(blank=True, null=True)
    side = models.TextField(blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_data'


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, models.DO_NOTHING)
    date = models.DateField()
    prev_close = models.DecimalField(max_digits=65535, decimal_places=65535)
    open = models.DecimalField(max_digits=65535, decimal_places=65535)
    high = models.DecimalField(max_digits=65535, decimal_places=65535)
    low = models.DecimalField(max_digits=65535, decimal_places=65535)
    close = models.DecimalField(max_digits=65535, decimal_places=65535)
    volume = models.IntegerField()
    deliverable_volume = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_price'


class StockStock(models.Model):
    date = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=140, blank=True, null=True)
    trade_num = models.IntegerField(blank=True, null=True)
    side = models.CharField(max_length=1, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_stock'


class StockappStockdata(models.Model):
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=40)
    symbol = models.CharField(max_length=25)
    isin_code = models.CharField(max_length=14)
    nse_groups = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'stockapp_stockdata'
