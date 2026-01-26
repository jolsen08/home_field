from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from leagues.models import Sport, Region, Season, AgeGroup, League


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create Sports
        sports_data = [
            ('Basketball', 'fa-solid fa-basketball'),
            ('Soccer', 'fa-solid fa-futbol'),
            ('Baseball', 'fa-solid fa-baseball'),
            ('Football', 'fa-solid fa-football'),
            ('Tennis', 'fa-solid fa-baseball-bat-ball'),
        ]

        sports = {}
        for name, icon in sports_data:
            sport, created = Sport.objects.get_or_create(
                name=name,
                defaults={'icon': icon, 'is_active': True}
            )
            sports[name] = sport
            if created:
                self.stdout.write(f'  Created sport: {name}')

        # Create Regions
        regions_data = [
            ('North Dallas', 'Dallas', 'TX', '75001,75002,75006,75007'),
            ('South Dallas', 'Dallas', 'TX', '75201,75202,75203,75204'),
            ('Austin Central', 'Austin', 'TX', '78701,78702,78703,78704'),
            ('Houston Heights', 'Houston', 'TX', '77008,77009,77018,77022'),
            ('Denver Metro', 'Denver', 'CO', '80202,80203,80204,80205'),
            ('Phoenix East', 'Phoenix', 'AZ', '85004,85006,85008,85009'),
        ]

        regions = {}
        for name, city, state, zips in regions_data:
            region, created = Region.objects.get_or_create(
                city=city,
                state=state,
                defaults={'name': name, 'zip_codes': zips, 'is_active': True}
            )
            regions[name] = region
            if created:
                self.stdout.write(f'  Created region: {name}')

        # Create Age Groups
        age_groups_data = [
            ('Tiny Tots', 4, 6, 'Introduction to sports fundamentals'),
            ('Junior', 7, 9, 'Basic skills and teamwork'),
            ('Intermediate', 10, 12, 'Developing skills and strategy'),
            ('Teen', 13, 15, 'Advanced skills and competition'),
            ('High School', 16, 18, 'Competitive play'),
        ]

        age_groups = {}
        for name, min_age, max_age, desc in age_groups_data:
            ag, created = AgeGroup.objects.get_or_create(
                name=name,
                defaults={'min_age': min_age, 'max_age': max_age, 'description': desc}
            )
            age_groups[name] = ag
            if created:
                self.stdout.write(f'  Created age group: {name}')

        # Create Seasons
        today = date.today()
        year = today.year

        seasons_data = [
            ('spring', year, date(year, 3, 1), date(year, 5, 31),
             date(year, 2, 1), date(year, 2, 28)),
            ('summer', year, date(year, 6, 1), date(year, 8, 15),
             date(year, 5, 1), date(year, 5, 31)),
            ('fall', year, date(year, 9, 1), date(year, 11, 30),
             date(year, 8, 1), date(year, 8, 31)),
            ('winter', year + 1, date(year + 1, 1, 5), date(year + 1, 3, 15),
             date(year, 12, 1), date(year, 12, 31)),
        ]

        seasons = {}
        for name, yr, start, end, reg_open, reg_close in seasons_data:
            season, created = Season.objects.get_or_create(
                name=name,
                year=yr,
                defaults={
                    'start_date': start,
                    'end_date': end,
                    'registration_open': reg_open,
                    'registration_close': reg_close
                }
            )
            seasons[f'{name}_{yr}'] = season
            if created:
                self.stdout.write(f'  Created season: {season}')

        # Create Sample Leagues
        leagues_data = [
            ('North Dallas Youth Basketball', 'Basketball', 'North Dallas', f'fall_{year}', 'Junior', 40, 75),
            ('North Dallas Teen Basketball', 'Basketball', 'North Dallas', f'fall_{year}', 'Teen', 30, 100),
            ('Austin Soccer League', 'Soccer', 'Austin Central', f'fall_{year}', 'Intermediate', 50, 85),
            ('Houston Football', 'Football', 'Houston Heights', f'fall_{year}', 'Junior', 36, 65),
            ('Denver Youth Baseball', 'Baseball', 'Denver Metro', f'spring_{year}', 'Intermediate', 45, 90),
            ('Phoenix Football', 'Football', 'Phoenix East', f'fall_{year}', 'Teen', 24, 70),
            ('Dallas Tiny Tots Soccer', 'Soccer', 'South Dallas', f'fall_{year}', 'Tiny Tots', 30, 50),
            ('Austin Tennis Academy', 'Tennis', 'Austin Central', f'fall_{year}', 'High School', 20, 120),
        ]

        for name, sport, region, season, age_group, max_part, fee in leagues_data:
            league, created = League.objects.get_or_create(
                name=name,
                defaults={
                    'sport': sports[sport],
                    'region': regions[region],
                    'season': seasons[season],
                    'age_group': age_groups[age_group],
                    'max_participants': max_part,
                    'fee': fee,
                    'status': 'open',
                    'description': f'Join our {sport.lower()} league for homeschool students in the {region} area!',
                    'schedule_info': 'Practices: Tuesdays and Thursdays 4-6 PM\nGames: Saturdays 9 AM - 12 PM'
                }
            )
            if created:
                self.stdout.write(f'  Created league: {name}')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
