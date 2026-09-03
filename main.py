import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pandas as pd

load_dotenv()

class CarAdvisor:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        # Данные из статьи Auto.ru
        self.cars_data = [
            {
                "name": "Toyota Land Cruiser 200",
                "year": 2012,
                "engine": 4.5,
                "transmission": "АКПП",
                "frame": True,
                "price": 2000000,
                "pros": ["Культовый статус", "Комфорт", "Надёжность"],
                "cons": ["Дорогой ремонт", "Расход топлива"]
            },
            {
                "name": "Mitsubishi Pajero IV", 
                "year": 2014,
                "engine": 3.0,
                "transmission": "АКПП",
                "frame": True,
                "price": 1500000,
                "pros": ["Отличная управляемость", "Надёжная подвеска"],
                "cons": ["Устаревший дизайн", "Жёсткая подвеска"]
            },
            {
                "name": "Kia Mohave",
                "year": 2013,
                "engine": 3.0,
                "transmission": "АКПП", 
                "frame": True,
                "price": 1700000,
                "pros": ["Просторный салон", "Дизельный мотор"],
                "cons": ["Редкость запчастей", "Слабая антикоррозийная защита"]
            }
        ]
    
    def filter_cars(self, max_year=2010, max_engine=4.0):
        """Фильтрует автомобили по критериям"""
        result = []
        for car in self.cars_data:
            if (car["year"] <= max_year and 
                car["engine"] <= max_engine and 
                car["frame"] and 
                car["transmission"] == "АКПП"):
                result.append(car)
        return result
    
    def get_recommendation(self, user_request):
        """Генерирует рекомендацию на основе запроса пользователя"""
        prompt = PromptTemplate(
            input_variables=["request", "cars"],
            template="""Ты эксперт по автомобилям. Пользователь спрашивает: {request}
            
            Доступные варианты: {cars}
            
            Дай конкретную рекомендацию с объяснением почему именно эта машина подходит."""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        cars_str = "\n".join([f"- {car['name']}: {car['engine']}л, {car['year']}г" for car in self.cars_data])
        
        return chain.run(request=user_request, cars=cars_str)

if __name__ == "__main__":
    advisor = CarAdvisor()
    
    # Пример использования
    filtered = advisor.filter_cars(max_year=2010, max_engine=4.0)
    print("Подходящие автомобили:")
    for car in filtered:
        print(f"- {car['name']} ({car['engine']}л, {car['year']}г)")
    
    # Генерация рекомендации
    recommendation = advisor.get_recommendation("ищу рамник не старше 2010 года до 4 литров на автомате")
    print("\nРекомендация:")
    print(recommendation)
auto.ru Авто.ру: купить, продать и обменять машину
