from django.core.management.base import BaseCommand
from song_models.models import Song, SongUser
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate the database with simple data'

    def handle(self, *args, **kwargs):
        # Se eliminan registros previos para evitar duplicados
        self.stdout.write('Deleting existing data...')
        SongUser.objects.all().delete()
        Song.objects.all().delete()
        User.objects.all().delete()

        # Crear usuarios
        self.stdout.write('Creating users...')
        user1 = User.objects.create_user(
            username='student1',
            password='student1pass',
            email='student1@example.com'
        )
        user2 = User.objects.create_user(
            username='student2',
            password='student2pass',
            email='student2@example.com'
        )
        User.objects.create_superuser(
            username='alumnodb',
            password='alumnodb',
            email='alumnodb@example.com'
        )
        self.stdout.write('Users created.')

        # Crear canciones
        self.stdout.write('Creating songs...')
        song1 = Song.objects.create(
            title='Here in the real world',
            artist='Alan Jackson',
            language='EN',
            audio_file='media/here_in_the_real_world.mp3',
            lrc_file='media/here_in_the_real_world.lrc',
            background_image='media/here_in_the_real_world.jpg',
            category='COUNTRY',
        )
        song2 = Song.objects.create(
            title='Super Trouper',
            artist='ABBA',
            language='EN',
            audio_file='media/ABBA - Super Trouper.mp3',
            lrc_file='media/ABBA - Super Trouper.lrc',
            background_image='media/ABBA - Super Trouper.jpg',
            category='POP',
        )
        song3 = Song.objects.create(
            title="Don't Forget to Remember",
            artist='Beegees',
            language='EN',
            audio_file="media/Beegees - Don't Forget to Remember.mp3",
            lrc_file="media/Beegees - Don't Forget to Remember.lrc",
            background_image='media/Beegees - Dont Forget to Remember.jpg',
            category='POP',
        )
        self.stdout.write('Songs created.')

        # rellenar SongUser
        self.stdout.write('Creating SongUser entries...')
        SongUser.objects.create(
            song=song1, user=user1, correct_guesses=5, wrong_guesses=2
        )
        SongUser.objects.create(
            song=song2, user=user1, correct_guesses=8, wrong_guesses=1
        )
        SongUser.objects.create(
            song=song3, user=user2, correct_guesses=3, wrong_guesses=4
        )
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))