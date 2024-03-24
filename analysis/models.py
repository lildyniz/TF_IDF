from django.db import models

from .utils import get_text_content


# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=255, verbose_name='Word')
    count_of_documents = models.IntegerField(default=1, verbose_name='Count of documents with the word')

    class Meta:
        ordering = ['word']
        indexes = [
            models.Index(fields=["word"]),
            ]
        verbose_name = 'Word'
        verbose_name_plural = 'Words'

    def __str__(self):
        return self.word


class File(models.Model):
    file = models.FileField(upload_to='media/%Y/%m/%d', verbose_name='File')
    uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded')

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['-uploaded']

    def save(self, *args, **kwargs):
        instance = super(File, self).save(*args, **kwargs)
        self.update_words()
        return instance
    
    def update_words(self):
        text_content = get_text_content(self)
        words = set(text_content.split())
        for word in words:
            try:
                saved_word = Word.objects.get(word=word)
                saved_word.count_of_documents += 1
                saved_word.save()
            except:
                new_word = Word(word=word, count_of_documents=1)
                new_word.save()

    def delete(self):

        self.file.delete()
        super().delete()