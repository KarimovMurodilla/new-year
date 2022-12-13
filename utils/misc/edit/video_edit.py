import os


class VideoEdit():
    def __init__(self):
        # For many child
        self.many_child_wishes = {
            'obey_parents': 'K_Wishes_01.mp4',
            'good_to_eat': 'K_Wishes_02.mp4',
            'study_well': 'K_Wishes_03.mp4',
            'find_new_friends': 'K_Wishes_04.mp4',
            'read_more_books': 'K_Wishes_05.mp4',
        }

        # For one child
        self.name_m = {
            'Александр': 'M_Name_095.mp4', 
            'Алексей': 'M_Name_096.mp4', 
            'Альберт': 'M_Name_097.mp4', 
            'Толик': 'M_Name_098.mp4', 
            'Андрей': 'M_Name_099.mp4', 
            'Антон': 'M_Name_100.mp4', 
            'Акадий': 'M_Name_101.mp4',  
            'Арсений': 'M_Name_102.mp4', 
            'Артем': 'M_Name_103.mp4', 
            'Артемий': 'M_Name_104.mp4', 
        }

        self.name_w = {
            'Агафия': 'W_Name_001.mp4', 
            'Аглая': 'W_Name_002.mp4', 
            'Агния': 'W_Name_003.mp4', 
            'Азалия': 'W_Name_004.mp4', 
            'Акулина': 'W_Name_005.mp4', 
            'Алефтина': 'W_Name_006.mp4', 
            'Александра': 'W_Name_007.mp4', 
            'Алина': 'W_Name_008.mp4', 
            'Ала': 'W_Name_009.mp4', 
            'Анастасия': 'W_Name_010.mp4'
        }
    
        self.ages = {
            1: 'Age_01.mp4',
            2: 'Age_02.mp4',
            3: 'Age_03.mp4',
            4: 'Age_04.mp4',
            5: 'Age_05.mp4',
            6: 'Age_06.mp4',
            7: 'Age_07.mp4',
            8: 'Age_08.mp4',
            9: 'Age_09.mp4',
            10: 'Age_10.mp4',
            11: 'Age_11.mp4',
            12: 'Age_12.mp4',
            13: 'Age_13.mp4',
            14: 'Age_14.mp4',
        }

        self.hobbies = {
            'read': 'Hobbies_01.mp4',
            'paint': 'Hobbies_02.mp4',
            'walk': 'Hobbies_03.mp4',
            'do_sport': 'Hobbies_04.mp4',
            'watch_cartoons': 'Hobbies_05.mp4',
            'eat_sweets': 'Hobbies_06.mp4',
            'sing': 'Hobbies_07.mp4',
            'play_music': 'Hobbies_08.mp4',
            'play_games': 'Hobbies_09.mp4',
            'dance': 'Hobbies_10.mp4',
        }

        self.wishes = {
            'obey_parents': 'Wishes_01.mp4',
            'good_to_eat': 'Wishes_02.mp4',
            'study_well': 'Wishes_03.mp4',
            'find_new_friends': 'Wishes_04.mp4',
            'read_more_books': 'Wishes_05.mp4',
        }


    def generate_video_for_many_child(self, file_name, chat_id):
        with open('staticfiles/videos/all/files.txt', 'w', encoding='utf-8') as f:
            f.write(
                'file K_01_constant.mp4\n'
                f'file {self.many_child_wishes.get(file_name)}\n'
                'file K_02_constant.mp4'
            )

        os.system(
            f"ffmpeg -y -f concat -i staticfiles/videos/all/files.txt -c copy staticfiles/videos/final/{chat_id}.mp4"
        )    


    def generate_video_for_one_child(self, chat_id, name, male, age, hobbies, wishes):
        with open('staticfiles/videos/all/files.txt', 'w', encoding='utf-8') as f:
            if male == 'man':
                f.write(
                    'file M_01_constant.mp4\n'
                    f'file {self.name_m.get(name)}\n'
                    'file M_02_constant.mp4\n'
                    f'file {self.ages.get(age)}\n'
                    'file M_03_constant.mp4\n'
                    f'file {self.hobbies.get(hobbies)}\n'
                    'file M_04_constant.mp4\n'
                    f'file {self.wishes.get(wishes)}\n'
                    'file M_05_constant.mp4'
                )

            elif male == 'woman':
                f.write(
                    'file W_01_constant.mp4\n'
                    f'file {self.name_w.get(name)}\n'
                    'file W_02_constant.mp4\n'
                    f'file {self.ages.get(age)}\n'
                    'file W_03_constant.mp4\n'
                    f'file {self.hobbies.get(hobbies)}\n'
                    'file W_04_constant.mp4\n'
                    f'file {self.wishes.get(wishes)}\n'
                    'file W_05_constant.mp4'
                )

        os.system(
            f"ffmpeg -y -f concat -i staticfiles/videos/all/files.txt -c copy staticfiles/videos/final/{chat_id}.mp4"
        )