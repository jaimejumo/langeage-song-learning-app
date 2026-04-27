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
            title='Here In The Real World',
            artist='Alan Jackson',
            language='EN',
            audio_file='Alan Jackson - Here In The Real World.mp3',
            lrc_file='Alan Jackson - Here In The Real World.lrc',
            background_image='Alan Jackson - Here In The Real World.jpg',
            category='COUNTRY',
        )
        song2 = Song.objects.create(
            title='Super Trouper',
            artist='ABBA',
            language='EN',
            audio_file='ABBA - Super Trouper.mp3',
            lrc_file='ABBA - Super Trouper.lrc',
            background_image='ABBA - Super Trouper.jpg',
            category='POP',
        )
        song3 = Song.objects.create(
            title="Don't Forget to Remember",
            artist='Beegees',
            language='EN',
            audio_file="Beegees - Don't Forget to Remember.mp3",
            lrc_file="Beegees - Don't Forget to Remember.lrc",
            background_image='Beegees - Dont Forget to Remember.jpg',
            category='POP',
        )
        Song.objects.create(
            title='Egoist',
            artist='Falco',
            language='DE',
            audio_file='Falco - Egoist.mp3',
            lrc_file='Falco - Egoist.lrc',
            background_image='Falco - Egoist.jpg',
            category='POP',
        )
        Song.objects.create(
            title='Me Gustas Tu',
            artist='Manu Chao',
            language='ES',
            audio_file='Manu Chao - Me Gustas Tu.mp3',
            lrc_file='Manu Chao - Me Gustas Tu.lrc',
            background_image='Manu Chao - Me Gustas Tu.jpg',
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