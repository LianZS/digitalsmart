import datetime
from typing import Dict
from django.db.models import Max, aggregates
from .models import PredictParamer, ScenceManager, ScenceFlow


class Predict():
    """
    人流预测模型
    """

    def __init__(self):
        pass

    def predict(self, pid) -> Dict:

        try:
            # 非节假日
            paramer = PredictParamer.objects.get(pid=pid, flag=0)
        except Exception as e:
            return {
                "future_time": [],  # 未来时间序列
                "future_data": []  # 预测值
            }
        hpower = paramer.hpower
        hconstant = paramer.hconstant
        spower = paramer.spower
        sconstant = paramer.sconstant
        lpower = paramer.lpower
        lconstant = paramer.lconstant
        mconstant = paramer.mconstant
        ddate = datetime.datetime.now()
        # 这句非常重要，因为如果它为1的话，说明预测的时间间隔为半小时,否则为5分钟
        type_flag = ScenceManager.objects.get(pid=pid).type_flag
        today = int(str(ddate.date()).replace("-", ""))
        # 最近的时间
        lasttime = ScenceFlow.objects.filter(pid=pid, ddate=today).values("ttime").aggregate(Max("ttime"))['ttime__max']
        if type_flag == 0:
            # 预测起始时间
            start_future_time = datetime.datetime(ddate.year, ddate.month, ddate.day, lasttime.hour,
                                                  int(lasttime.minute / 5) * 5,
                                                  0)
            # 时间间隔为5分钟
            time_inv = datetime.timedelta(minutes=5)
            # 预测时间序列
            ttime_range = [str((start_future_time + time_inv * i).time()) for i in
                           range(1, 288 - lasttime.hour * 12 - int(lasttime.minute / 5))]
            x_pos = [x for x in range(lasttime.hour * 12 + int(lasttime.minute / 5) + 1, 289)]

        else:
            time_inv = datetime.timedelta(minutes=30)
            # 预测起始时间
            start_future_time = datetime.datetime(ddate.year, ddate.month, ddate.day, lasttime.hour,
                                                  int(lasttime.minute / 30) * 30,
                                                  0)
            ttime_range = [str((start_future_time + time_inv * i).time()) for i in
                           range(1, 48 - lasttime.hour * 2 - int(lasttime.minute / 30))]
            x_pos = [x for x in range(lasttime.hour * 2 + int(lasttime.minute / 30), 49)]

            # 流量预测
        y_pos = [
            int(hconstant * pow(x, hpower) + sconstant * pow(x, spower) + lconstant * pow(x, lpower) + mconstant)
            for x
            in
            x_pos]
        return {
            "future_time": ttime_range,  # 未来时间序列
            "future_data": y_pos  # 预测值
        }
