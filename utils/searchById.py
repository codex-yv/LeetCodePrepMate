# s = {1:{"Companies_List":[{"Company":"c1", "frequency":0.322323 }], "acceptance":32, "difficulty":"Medium", "Link":"https://"}}
s2 = {"company_name":[{"id":1, "question":"q1", "frequency": 0.2323, "difficulty":"medium", "acceptance":45, "link":"https" }]}

import os
import csv

def getDatabyId():
    base_dir = os.path.dirname(__file__)
    folder_path = os.path.join(base_dir, '..', 'companies')

    s = {}

    # Process each CSV file
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            company_name = os.path.splitext(file_name)[0]  # e.g., 'google' from 'google.csv'

            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    qid = row['ID']
                    title = row['Title']
                    acceptance_str = row['Acceptance']
                    frequency_str = row['Frequency']
                    difficulty = row['Difficulty']
                    link = row['Leetcode Question Link']

                    # Clean and convert fields
                    acceptance = float(acceptance_str.strip('%')) if acceptance_str else 0
                    frequency = float(frequency_str) if frequency_str else 0

                    # If this is a new ID, add its full structure
                    if qid not in s:
                        s[qid] = {
                            "Companies_List": [],
                            "acceptance": acceptance,
                            "difficulty": difficulty,
                            "question": title,
                            "Link": link
                        }

                    # Always add the company info to the list
                    s[qid]["Companies_List"].append({
                        "company_name": company_name,
                        "frequency": frequency
                    })
    
    return s

class FindDataByID:
    def __init__(self):
        self.acceptance: float
        self.difficulty:str
        self.question: str
        self.link: str
        self.companies: list[dict]
        self.total: int

    def findDatabyId(self, k:str = None, s:dict = None):
        if k is None:
            return 101
        try:
            self.data = s[k]
            self.companies = self.data["Companies_List"]
            self.acceptance = self.data["acceptance"]
            self.question = self.data["question"]
            self.difficulty = self.data["difficulty"]
            self.link = self.data["Link"]
            self.total = len(self.companies)
        except KeyError:
            return 404
        
