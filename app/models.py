from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField('Категория аты', max_length=150)
    slug = models.SlugField('Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категориялар'


class Contest(models.Model):
    title = models.CharField('Байқау аты', max_length=255)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    image = models.ImageField('Банер', upload_to='contest_images/')
    description = models.TextField('Байқау сипаттамасы')
    slug = models.SlugField('Слаг(адресс)')
    created = models.DateTimeField('Жарияланған күні', auto_now_add=True)
    date = models.DateTimeField('Байқау болатын уақыт')
    status = models.BooleanField('Белсенді/Белсенді емес', default=True)
    open_close = models.BooleanField('Жабық байқау ма?', default=False)

    def __str__(self):
        return f"{self.title} {self.category.name}"

    class Meta:
        verbose_name = 'Байқау'
        verbose_name_plural = 'Байқаулар'
        ordering = ['-created']


class Participant(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField('Есімі', max_length=150)
    last_name = models.CharField('Тегі', max_length=150)
    phone = models.CharField('Телефон номері', max_length=16)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Қатысушы/Тіркелуші'
        verbose_name_plural = 'Қатысушылар/Тіркелушілер'


class Jury(models.Model):
    user = models.ForeignKey(User, verbose_name='Қолданушы', null=True, blank=True, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, verbose_name='Байқау', on_delete=models.CASCADE)
    status_jury = models.BooleanField('Әділ-қазы статусы', default=False)

    def __str__(self):
        return f"{self.user} {self.contest}"

    class Meta:
        verbose_name = 'Әділ қазы'
        verbose_name_plural = 'Әділ қазылар'


class Result(models.Model):
    participant = models.ForeignKey(Participant, verbose_name='Қатысушы', on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, verbose_name='Байқау', on_delete=models.CASCADE)
    file = models.FileField('Файл', upload_to='files/', blank=True, null=True)
    score = models.IntegerField('Ұпай', default=0)

    def __str__(self):
        return f"{self.participant.first_name} {self.participant.last_name} {self.score}"

    class Meta:
        verbose_name = 'Нәтиже'
        verbose_name_plural = 'Нәтижелер'


class Vote(models.Model):
    user = models.ForeignKey(User, verbose_name='Тіркелуші', null=True, blank=True, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, verbose_name='Байқау', on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, verbose_name='Қатысушы', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Дауыс беру'
        verbose_name_plural = 'Дауыс берулер'


class Question(models.Model):
    name = models.CharField('Есімі', max_length=150)
    phone = models.CharField('Телефон номері', max_length=16)
    message = models.TextField('Хабарлама')
    created = models.DateTimeField("Хабарлама келген уақыт", auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.phone}"

    class Meta:
        verbose_name = 'Сұрақ'
        verbose_name_plural = 'Сұрақтар'
