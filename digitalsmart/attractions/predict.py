import datetime
from .models import PredictParamer


class Predict():
    def __init__(self):
        pass

    def predict(self, pid):
        ddate = datetime.datetime.now()
        ttime = ddate.time()
        # 预测起始时间
        start_future_time = datetime.datetime(ddate.year, ddate.month, ddate.day, ttime.hour, int(ttime.minute / 5) * 5,
                                              0)
        # 时间间隔为5分钟
        time_inv = datetime.timedelta(minutes=5)
        # 预测时间序列
        ttime_range = [start_future_time + time_inv * i for i in
                       range(1, 288 - ttime.hour * 12 - int(ttime.minute / 5))]
        x_pos = [x for x in range(ttime.hour * 12 + int(ttime.minute / 5) + 1, 289)]
        paramer = PredictParamer.objects.get(pid=pid)
        hpower = paramer.hpower
        hconstant = paramer.hconstant
        spower = paramer.spower
        sconstant = paramer.sconstant
        lpower = paramer.lpower
        lconstant = paramer.lconstant
        mconstant = paramer.mconstant
        # 流量预测
        y_pos = [hconstant * pow(x, hpower) + sconstant * pow(x, spower) + lconstant * (x, lpower) + mconstant for x in
                 x_pos]
