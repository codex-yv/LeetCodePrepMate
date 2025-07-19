import os
import csv

def getDataByCompany():
    base_dir = os.path.dirname(__file__)
    folder_path = os.path.join(base_dir, '..', 'companies')

    s = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            company_name = os.path.splitext(filename)[0]  # e.g., "Google.csv" -> "Google"
            company_questions = []

            file_path = os.path.join(folder_path, filename)
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    try:
                        q_data = {
                            "id": int(row["ID"]),
                            "question": row["Title"].strip(),
                            "frequency": float(row["Frequency"]),
                            "difficulty": row["Difficulty"].strip().lower(),
                            "acceptance": row["Acceptance"],
                            "link": row["Leetcode Question Link"].strip()
                        }
                        company_questions.append(q_data)
                    except (ValueError, KeyError) as e:
                        print(f"Skipping row in {filename} due to error: {e}")
            
            s[company_name] = company_questions

    return s

class FindDataByCompany:
    def __init__(self):
        self.data_ldict : list[dict]
        self.totalq : int
        self.easy : int
        self.medium : int
        self.hard : int
        self.only_hard : list[dict]
        self.only_easy : list[dict]
        self.only_medium : list[dict]

    def findDataByCompany(self, data:dict = None, cname:str = None):
        if data is None or cname is None:
            return 101
        try:
            self.data_ldict = data[cname]
            self.totalq = len(self.data_ldict)
            e = 0
            m = 0
            h = 0
            for Dict in self.data_ldict:
                if Dict["difficulty"] == "easy":
                    e+=1
                elif Dict["difficulty"] == "medium":
                    m+=1
                elif Dict["difficulty"] == "hard":
                    h+=1
            
            self.easy = e
            self.medium = m
            self.hard = h

        except KeyError:
            return 404
    
    def dropDownList(self, data:dict = None, cname:list = None):
        if len(cname) !=0:
            self.data_list = data.keys()
            self.drop_down_list = []

            for comp in self.data_list:
                self.Add = True
                for char in cname:
                    if char.lower() not in comp:
                        self.Add = False
                        break

                if self.Add is True:
                    self.drop_down_list.append(comp)

            return self.drop_down_list
        else:
            return []
        
    def sortedDifficulty(self, data:list[dict]):

        sorted_hard = []
        sorted_medium = []
        sorted_easy = []

        for details in data:
            try:
                if details["difficulty"] == "hard":
                    sorted_hard.append(details)
                elif details["difficulty"] == "medium":
                    sorted_medium.append(details)
                elif details["difficulty"] == "easy":
                    sorted_easy.append(details)
                else:
                    return 101
            except KeyError:
                return 101
            
            self.only_easy = sorted_easy
            self.only_medium = sorted_medium
            self.only_hard = sorted_hard
