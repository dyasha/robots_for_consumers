import datetime as dt

import xlwt
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from robots.models import Robot
from waitlist.send_messages import SMessage

from .serializers import RobotSerializer


class APIRobot(APIView):
    """Класс Робота API."""

    def post(self, request):
        """Создание робота."""
        serializer = RobotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            SMessage.send_message(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportRobot:
    """Класс Робота для экспорта в файл."""

    WEEK = dt.datetime.now().date() - dt.timedelta(weeks=1)

    @staticmethod
    def index(request):
        """Страница для загрузки."""
        return render(request, "robots/export_to_xls.html")

    @staticmethod
    def read_robots():
        """Чтение данных из БД."""
        robots = list(
            Robot.objects.values("model", "version")
            .annotate(Count("model"))
            .filter(created__gt=ExportRobot.WEEK)
        )
        return robots

    @staticmethod
    def export_robots_xls(request):
        """Экспорт данных о роботах."""
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=robots.xls"
        wb = xlwt.Workbook(encoding="utf-8")
        robots = ExportRobot.read_robots()
        model_sheets = {}
        per = 1
        for robot in robots:
            model = robot["model"]

            if model in model_sheets:
                ws = model_sheets[model]
            else:
                ws = wb.add_sheet(f"{model}-{per}")
                per += 1
                model_sheets[model] = ws

                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ["Модель", "Версия", "Количество за неделю"]
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                font_style = xlwt.XFStyle()

            row_num += 1
            ws.write(row_num, 0, robot["model"], font_style)
            ws.write(row_num, 1, robot["version"], font_style)
            ws.write(row_num, 2, robot["model__count"], font_style)
        wb.save(response)
        return response
